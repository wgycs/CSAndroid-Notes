## 问题：

线程间通信机制是什么？怎么完成线程间通信的？

由什么组成？ 

调度策略是什么样的？消息循环机制，消息分发机制？

为什么这么设计？





## 1. 线程间通信机制Handler

1. Handler 是典型的生产者-消费者模型。是线程之间进行通信的媒介。

2. 线程之间内存是不共享的，那么怎么完成的线程间通信？

   设计通信机制的思路：

   进行消息封装  ---- 拿到目标线程句柄  --- 发送消息 --- 目标线程进行消息调度（优先级、异步、阻塞？）
   
   

实际上Handler也是按照这个思路进行，并有更多优秀的思考。比如消息池机制、消息屏障、IdleHandler、epoll等



首先看Handler的创建过程：

```java
public Handler(@Nullable Callback callback, boolean async) {
        if (FIND_POTENTIAL_LEAKS) {
            final Class<? extends Handler> klass = getClass();
            // 是匿名类 或 成员类 或 局部类    ，但字段修饰符不是静态的时候， 有可能引起内存泄露。
            if ((klass.isAnonymousClass() || klass.isMemberClass() || klass.isLocalClass()) &&
                    (klass.getModifiers() & Modifier.STATIC) == 0) {
                Log.w(TAG, "The following Handler class should be static or leaks might occur: " +
                    klass.getCanonicalName());
            }
        }
		// 获取Looper    如果当前线程没有Looper 抛出异常。  
        //  1. 因为没有Looper 就执行不了下面mQueue的初始化
        //  2. 没有Looper将无法完成消息调度
        mLooper = Looper.myLooper();
        if (mLooper == null) {
            throw new RuntimeException(
                "Can't create handler inside thread " + Thread.currentThread()
                        + " that has not called Looper.prepare()");
        }
    	//这句。。   mQueue 是跨线程的句柄、
    	// 如果不能初始化 也就不能传递消息
        mQueue = mLooper.mQueue;
        mCallback = callback;
        mAsynchronous = async;
    }
```



消息是怎么封装的？



```java
public final class Message implements Parcelable {
    // 执行等待时长， 在MessageQueue中，以此为依据排序
    public long when;
	// 发送的数据
    /*package*/ Bundle data;
	// 目标线程的 Handler对象，用于发送 和 处理消息  跨线程
    /*package*/ Handler target;
    // Message Pool 消息池，回收和复用Message对象  MAX_POOL_SIZE = 50; 
    private static Message sPool;
}
```



消息怎么调度的？    Looper.loop()

```java
/**
* Run the message queue in this thread. Be sure to call
* {@link #quit()} to end the loop.
*/
public static void loop() {
    // sThreadLocal.get();
    final Looper me = myLooper();
    if (me == null) {
        throw new RuntimeException("No Looper; Looper.prepare() wasn't called on this thread.");
    }
    // 从本地线程的ThreadLocal 中找到Looper对象，  并从其中拿到 MessageQueue
    // 那这个Looper对象是什么时候放进去的呢？ 没错就是 Looper.prepare()  
    // sThreadLocal.set(new Looper(quitAllowed));  
    //  这也就是子线程不调用 prepare 就不能创建Handler、也不能运行Looper.loop()
    final MessageQueue queue = me.mQueue;


    for (;;) {
        // 如果没有消息这里不会返回
        Message msg = queue.next(); // might block
        // 返回null 这里会退出循环
        if (msg == null) {
            // No message indicates that the message queue is quitting.
            return;
        }
        
        logging.println(">>>>> Dispatching to " + msg.target + " " +
                        msg.callback + ": " + msg.what);
        
        // 非空的消息 执行分发操作
        try {
                msg.target.dispatchMessage(msg);
            } finally {
               
            }
        logging.println("<<<<< Finished to " + msg.target + " " + msg.callback);
        
        // 放回消息池
        msg.recycleUnchecked();
    }
}

// Looper 并没有实际的调度，那么问题就在于这个next什么时候返回了。
// 所以这个调度测量也就是next的返回策略。
// MessageQueue.java
Message next() {
        // Return here if the message loop has already quit and been disposed.
        // This can happen if the application tries to restart a looper after quit
        // which is not supported.
    // 消息不为空  但是Target是 null , 这说明什么问题？ 
    //  可以看下这个函数实现    private int postSyncBarrier(long when) {}
    // 在Post这个名字SyncBarrier的消息的时候没有赋值msg.target
    // 这就是我们所说的消息屏障。
    for (;;) {
        // 这里进入休眠，下次什么时候唤醒呢？
        // 1. 
        // boolean enqueueMessage(Message msg, long when) {}
        // 这个函数里面nativeWake(mPtr)  ， 添加消息的时候会对messageQueue排序顺便会检查要不要唤醒
        // 这些条件(p == null || when == 0 || when < p.when) 满足，并且当前是阻塞状态，就会调用nativeWake(mPtr) 
        // 这肯定不是唯一的唤醒方式，否则如果一直没有消息进来不是要死在这里了。。
        
        // 2. 
        // Looper.cpp-->Looper::pollOnce()
        // 这里面使用了epoll机制， 超时返回。
        nativePollOnce(ptr, nextPollTimeoutMillis);
        // 消息屏障
        if (msg != null && msg.target == null) {
            // Stalled by a barrier.  Find the next asynchronous message in the queue.
            do {
                prevMsg = msg;
                msg = msg.next;
                // 消息屏障存在的情况  就会搜索msgQueue中的isAsynchronous 异步消息，拿出来执行  。 直到队列末尾
            } while (msg != null && !msg.isAsynchronous());
        }
        
        // 到这基本流程就结束了 
        // 但是还有一个IdleHandler机制

}

```

[nativePollOnce 函数讲解细节 ](https://www.kancloud.cn/alex_wsc/android-deep3/416265)