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

实际上Handler也是按照这个思路进行，并有更多优秀的思考。



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



消息怎么调度的？  Looper.loop()

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
    final MessageQueue queue = me.mQueue;


    for (;;) {
        Message msg = queue.next(); // might block
        if (msg == null) {
            // No message indicates that the message queue is quitting.
            return;
        }
        
        
    }
}

// MessageQueue.java
Message next() {
        // Return here if the message loop has already quit and been disposed.
        // This can happen if the application tries to restart a looper after quit
        // which is not supported.

}

```

