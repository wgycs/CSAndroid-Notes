### FutureTask是什么？
FutureTask是一个可取消的异步计算。FutureTask实现了RunnableFuture接口，间接实现了Future和Runnable接口。在Future的基本实现中，提供了开始和取消一个计算的方法，同时可以查询计算是否完成并获取到计算结果。 仅当完成计算之后才能获取到计算结果，否则get方法将阻塞，直到计算完成。 计算完成之后这个计算将不能够重启或者取消，除非调用RunAndReset方法。
Runnable的实现，赋予了FutureTask包裹Runnable或Callable的能力，因此FutureTask可以被提交到Executor中执行。

```java
interface RunnableFuture<V> extends Runnable, Future<V>{}
class FutureTask<V> implements RunnableFuture<V>{}
```

#### FutureTask的状态转换
FutureTask任务的运行状态，最初为NEW。运行状态仅在set、setException和cancel方法中转换为终端状态。在完成过程中，状态可能呈现出瞬时值INTERRUPTING(仅在中断运行程序以满足cancel(true)的情况下)或者COMPLETING(在设置结果时)状态时。从这些中间状态到最终状态使用 cheaper ordered/lazy writes（无锁同步CAS）策略， 原因是这些状态值是固定不可修改的。

 * NEW -> COMPLETING -> NORMAL
 * NEW -> COMPLETING -> EXCEPTIONAL
 * NEW -> CANCELLED
 * NEW -> INTERRUPTING -> INTERRUPTED

### FutureTask实现
这个类在实现上jdk 1.8 版本前后版本实现方式有些不同，之前使用的策略是AbstractQueuedsynchronizer也就是和ReentrantLock、ThreadPoolExecutor中的worker策略相同。 1.8版本是使用Usafe包中的Compare-And-Swap（CAS)特性实现。 

>Usafe包？
>sun.misc.Unsafe 是sun公司的一个未开源的组件包，提供了些可以绕开JVM的一些方法，其中就包含了同步相关的一些方法。比如monitorEnter(),tryMonitorEnter(),monitorExit(),compareAndSwapInt(),putOrderedInt()。 
>
>什么是CAS？
>CAS是CPU提供的 用于解决多线程并行情况下使用锁造成性能损耗 的机制。
>
>如此优秀的特性，是不是尽情用就好了，当然不会尽善尽美，首先在Unsafe包中所有操作绕开了JVM意味着不会有人替你管理内存。 而且CAS会引入ABA问题。 更多内容请参考资料[[1]](http://mishadoff.com/blog/java-magic-part-4-sun-dot-misc-dot-unsafe/)

毋庸置疑根据前面描述的特性，FutureTask至少有一个cancel(), V get() 的public方法。

```java
public boolean cancel(boolean mayInterruptIfRunning) {
        if (!(state == NEW &&
              U.compareAndSwapInt(this, STATE, NEW,
                  mayInterruptIfRunning ? INTERRUPTING : CANCELLED)))
            return false;
        try {    // in case call to interrupt throws exception
            if (mayInterruptIfRunning) {
                try {
                    Thread t = runner;
                    if (t != null)
                        t.interrupt();
                } finally { // final state
                    U.putOrderedInt(this, STATE, INTERRUPTED);
                }
            }
        } finally {
            finishCompletion();
        }
        return true;
    }

 /**
     * @throws CancellationException {@inheritDoc}
     */
    public V get() throws InterruptedException, ExecutionException {
        int s = state;
        if (s <= COMPLETING)
            s = awaitDone(false, 0L);
        return report(s);
    }


```
cance()方法很好理解，就做量两件事1. 还能不能取消了，要不要终止线程取消。 2. 设置对应的状态。
get()方法是去获取执行结果，但是现在如果没执行完呢？ 前面说如果没执行完会阻塞等待，显然这是` s = awaitDone(false, 0L);`干的事情。

好像也不复杂。 对喽，稍微复杂的点地方在怎么去处理这个等待，怎么正确的同步处理状态。

```java
/**
     * Awaits completion or aborts on interrupt or timeout.
     *
     * @param timed true if use timed waits
     * @param nanos time to wait, if timed
     * @return state upon completion or at timeout
     */
    private int awaitDone(boolean timed, long nanos)
        throws InterruptedException {
		// 下面的代码巧妙的实现了一下目标：
		// 每次请求到来的时候获取下精确的纳秒时间 nanoTime. （纳秒随机开始可能获取到负数）
		// 因此针对不同的值不同处理。
		// 被意外唤醒那么等一会。
        // The code below is very delicate, to achieve these goals:
        // - call nanoTime exactly once for each call to park
        // - if nanos <= 0L, return promptly without allocation or nanoTime
        // - if nanos == Long.MIN_VALUE, don't underflow
        // - if nanos == Long.MAX_VALUE, and nanoTime is non-monotonic
        //   and we suffer a spurious wakeup, we will do no worse than
        //   to park-spin for a while
        long startTime = 0L;    // Special value 0L means not yet parked
        WaitNode q = null;
        boolean queued = false;
        for (;;) {
            int s = state;
            if (s > COMPLETING) {
                if (q != null)
                    q.thread = null;
                return s;
            }
            else if (s == COMPLETING)
                // We may have already promised (via isDone) that we are done
                // so never return empty-handed or throw InterruptedException
                Thread.yield();
            else if (Thread.interrupted()) {
                removeWaiter(q);
                throw new InterruptedException();
            }
            else if (q == null) {
                if (timed && nanos <= 0L)
                    return s;
                q = new WaitNode();  //用户方传入等待和时间两个参数 且时间>0 创建等待节点
            }
            else if (!queued)
                queued = U.compareAndSwapObject(this, WAITERS,
                                                q.next = waiters, q);
            else if (timed) {        // 等待 传入参数nanos
                final long parkNanos;
                if (startTime == 0L) { // first time
                    startTime = System.nanoTime();
                    if (startTime == 0L)
                        startTime = 1L;
                    parkNanos = nanos;
                } else { 
                    long elapsed = System.nanoTime() - startTime;
                    if (elapsed >= nanos) {
                        removeWaiter(q);
                        return state;
                    }
                    parkNanos = nanos - elapsed;
                }
                // nanoTime may be slow; recheck before parking 
                if (state < COMPLETING)
                    LockSupport.parkNanos(this, parkNanos);
            }
            else
                LockSupport.park(this);
        }
    }

```

这一堆看着是很长，发现注释只有一句话。
`Awaits completion or aborts on interrupt or timeout.`
这个函数就干了这个事情， 等完成、等取消、等取消、等超时。 有人可能会说胡说，明明只有三个return。
`throw new InterruptedException();`这不是还有一个抛出异常。
然后removeWaiter()又做了什么？

```java
 	/**
     * Tries to unlink a timed-out or interrupted wait node to avoid
     * accumulating garbage.  Internal nodes are simply unspliced
     * without CAS since it is harmless if they are traversed anyway
     * by releasers.  To avoid effects of unsplicing from already
     * removed nodes, the list is retraversed in case of an apparent
     * race.  This is slow when there are a lot of nodes, but we don't
     * expect lists to be long enough to outweigh higher-overhead
     * schemes.
     */
    private void removeWaiter(WaitNode node) {
        if (node != null) {
            node.thread = null;
            retry:
            for (;;) {          // restart on removeWaiter race
                for (WaitNode pred = null, q = waiters, s; q != null; q = s) {
                    s = q.next;
                    if (q.thread != null)
                        pred = q;
                    else if (pred != null) {
                        pred.next = s;
                        if (pred.thread == null) // check for race
                            continue retry;
                    }
                    else if (!U.compareAndSwapObject(this, WAITERS, q, s))
                        continue retry;
                }
                break;
            }
        }
    }
```




### FutureTask使用案例

```java
ExecutorService service = Executors.newSingleThreadExecutor();
FutureTask<String> futureTask = new FutureTask<>(new Callable<String>() {
     @Override
     public String call() throws Exception {
         return "futureTask say HelloWorld!!!";
     }
});
service.execute(futureTask);
System.out.println(futureTask.get());

```






####参考资料
[1] [Unsafe : http://mishadoff.com/blog/java-magic-part-4-sun-dot-misc-dot-unsafe/](http://mishadoff.com/blog/java-magic-part-4-sun-dot-misc-dot-unsafe/)
[2] [synchronized 实现方式 : https://blog.csdn.net/qq_36520235/article/details/81176536](https://blog.csdn.net/qq_36520235/article/details/81176536)
[3] [objectMonitor.hpp 源码 :  https://hg.openjdk.java.net/jdk8u/jdk8u/hotspot/file/da3a1f729b2b/src/share/vm/runtime/objectMonitor.hpp](https://hg.openjdk.java.net/jdk8u/jdk8u/hotspot/file/da3a1f729b2b/src/share/vm/runtime/objectMonitor.hpp)
[4] [usafe https://blog.csdn.net/zyzzxycj/article/details/89877863](https://blog.csdn.net/zyzzxycj/article/details/89877863)

