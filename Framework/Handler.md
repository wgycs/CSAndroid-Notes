## Handler问题思考？

线程间通信机制是什么？怎么完成线程间通信的？

由什么组成？ 

调度策略是什么样的？消息循环机制，消息分发机制？

为什么这么设计？





## 1. 线程间通信机制Handler

1. Handler 是典型的生产者-消费者模型。是线程之间进行通信的媒介。

2. 线程之间内存是不共享的，那么怎么完成的线程间通信？

   

   **设计通信机制的思路**：
   
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





## 2. 三种消息类型

1. **同步消息**
2. **异步消息**
3. **消息屏障**



### 同步消息和异步消息

Handler 发送的消息只有`Message`一种，怎么就出现了三种消息类型？

前面分析Handler创建的时候，可以看到最后一个参数是async，这里就注定这个Handler是发送出去同步消息还是异步消息。

```java
public Handler(@Nullable Callback callback, boolean async) {
	/// async
    mAsynchronous = async;
}

// post 方法最终调用到的MessageQueue的入队方法。在这里设置了Message中一个属性  msg.setAsynchronous(true);
private boolean enqueueMessage(@NonNull MessageQueue queue, @NonNull Message msg,
            long uptimeMillis) {
       // 这里必定会设置Target
        msg.target = this;
        msg.workSourceUid = ThreadLocalWorkSource.getUid();
		// 如果是异步的Handler，发出去的消息Message 就会带有 异步标记
    	// 这个标记的 就区分出了两种消息， 同步消息和异步消息。 
        // 什么区别呢？前面调度分析的时候，同步消息会被消息屏障阻塞， 而异步不会。
        if (mAsynchronous) {
            msg.setAsynchronous(true);
      
        }
        return queue.enqueueMessage(msg, uptimeMillis);
    }
```



### 消息屏障

好像只有这两种消息类型，消息屏障又是什么？ 准确的说叫同步消息屏障，也就是说只会阻塞同步消息，通常是和异步消息一起使用。

消息屏障有什么特殊吗？

```java

@TestApi
    public int postSyncBarrier() {
        return postSyncBarrier(SystemClock.uptimeMillis());
    }

    private int postSyncBarrier(long when) {
        // Enqueue a new sync barrier token.
        // We don't need to wake the queue because the purpose of a barrier is to stall it.
        synchronized (this) {
            final int token = mNextBarrierToken++;
            
            
            /// ******注意看这个消息的创建过程
            // 从消息池中拿到了这个消息对象之后，设置了when、 arg1 就加入到消息队列的单链表中了。
            // !!! 没设置 target 。  可以对比上面的 代码  msg.target = this;
            // 什么是消息屏障？  Looper调度的时候，如果发现没有target的消息，那么就是消息屏障了
            final Message msg = Message.obtain();
            msg.markInUse();
            msg.when = when;
            msg.arg1 = token;
			// *********
            
            Message prev = null;
            Message p = mMessages;
            if (when != 0) {
                // 找到时间合适的那个节点
                while (p != null && p.when <= when) {
                    prev = p;
                    p = p.next;
                }
            }
            /// 加入进去
            if (prev != null) { // invariant: p == prev.next
                msg.next = p;
                prev.next = msg;
            } else {
                msg.next = p;
                mMessages = msg;
            }
            // 返回了一个 token  。  实际上就是一个计数
            // 删除的时候就据此token  
            return token;
        }
    }

```



删除消息屏障的过程。

```java
    @TestApi
    public void removeSyncBarrier(int token) {
        // Remove a sync barrier token from the queue.
        // If the queue is no longer stalled by a barrier then wake it.
        synchronized (this) {
            Message prev = null;
            Message p = mMessages;
            // 找到 消息target为空  arg1 是 token的那个Message对象
            while (p != null && (p.target != null || p.arg1 != token)) {
                prev = p;
                p = p.next;
            }
            // 到末尾都没找到那么  就抛出异常了
            if (p == null) {
                throw new IllegalStateException("The specified message queue synchronization "
                        + " barrier token has not been posted or has already been removed.");
            }
            
            // 从节点中删除
            final boolean needWake;
            if (prev != null) {
                prev.next = p.next;
                needWake = false;
            } else {
                mMessages = p.next;
                needWake = mMessages == null || mMessages.target != null;
            }
            
            // 将删除的节点回收，放入消息池中
            p.recycleUnchecked();

            // If the loop is quitting then it is already awake.
            // We can assume mPtr != 0 when mQuitting is false.
            if (needWake && !mQuitting) {
                // 有消息需要唤醒 nativePollOnce的阻塞   epoll_wait() 实现
                nativeWake(mPtr);
            }
        }
    }
```



## 3. 消息屏障的使用场景

在向Choreography订阅了VSync信号接收消息之后，VSync回调会触发重绘操作。

显然，这次界面刷新的优先级最高，因此使用了消息屏障以阻塞消息队列中不重要的同步消息。并创建一个异步刷新，加入到主线程Loop中的MessageQueue队列中。

**ViewRootImpl.java**

```java
// Post消息屏障到消息队列
@UnsupportedAppUsage
void scheduleTraversals() {
    if (!mTraversalScheduled) {
        mTraversalScheduled = true;
        // 设置消息屏障
        // 这里会返回Token ， 删除的时候会以此为依据进行删除
        mTraversalBarrier = mHandler.getLooper().getQueue().postSyncBarrier();
        mChoreographer.postCallback(
            Choreographer.CALLBACK_TRAVERSAL, mTraversalRunnable, null);
        if (!mUnbufferedInputDispatch) {
            scheduleConsumeBatchedInput();
        }
        notifyRendererOfFramePending();
        pokeDrawLockIfNeeded();
    }
}

// 删除 消息屏障
void unscheduleTraversals() {
        if (mTraversalScheduled) {
            mTraversalScheduled = false;
            //  mTraversalBarrier 拿Token 去MessageQueue中删除屏障
            // 刪除消息屏障
            mHandler.getLooper().getQueue().removeSyncBarrier(mTraversalBarrier);
            mChoreographer.removeCallbacks(
                    Choreographer.CALLBACK_TRAVERSAL, mTraversalRunnable, null);
        }
    }
```





## 4. Handler 延时消息的实现

```java
// 从开始加入消息开始看起
// Handler 中两种消息延迟的方法
// 1. 定时执行
public boolean sendMessageAtTime(@NonNull Message msg, long uptimeMillis) {
    ...
    return enqueueMessage(queue, msg, uptimeMillis);
}
// 2. 延迟执行
public final boolean sendMessageDelayed(@NonNull Message msg, long delayMillis) {
        if (delayMillis < 0) {
            delayMillis = 0;
        }
        return sendMessageAtTime(msg, SystemClock.uptimeMillis() + delayMillis);
}


// uptimeMillis 消息延迟执行的时间点
public boolean sendMessageAtTime(@NonNull Message msg, long uptimeMillis) {
        MessageQueue queue = mQueue;
        if (queue == null) {
            RuntimeException e = new RuntimeException(
                    this + " sendMessageAtTime() called with no mQueue");
            Log.w("Looper", e.getMessage(), e);
            return false;
        }
    	// 在上节三种消息类型 中提到的queueMessage
        // queue.enqueueMessage 方法(msg, uptimeMillis);
        // 这里最终调用的是MessageQueue的 enqueueMessage 方法
        return enqueueMessage(queue, msg, uptimeMillis);
}

// 至此并没有找到为什么Handler 会延迟处理消息，只是在Message的when中增加了一个时间戳。
// 那么就只剩消息队列，和消息调度环节了。
```





```java
boolean enqueueMessage(Message msg, long when) {

            msg.markInUse();
            msg.when = when;
            Message p = mMessages;
            boolean needWake;
    
    		//插入队列  两种情况 
            // 1. 消息队列为空\待插入时间为0\第一条执行的when时间比待插入的时间更长
            if (p == null || when == 0 || when < p.when) {
                // New head, wake up the event queue if blocked.
                //将msg 插入到头部
                msg.next = p;
                mMessages = msg;
                // 插入到头部要唤醒
                needWake = mBlocked;
            // 2. 其他情况
            } else {
                // Inserted within the middle of the queue.  Usually we don't have to wake
                // up the event queue unless there is a barrier at the head of the queue
                // and the message is the earliest asynchronous message in the queue.
                needWake = mBlocked && p.target == null && msg.isAsynchronous();
                Message prev;
                // 找到比当msg 执行时间更晚的消息
                for (;;) {
                    prev = p;
                    p = p.next;
                    if (p == null || when < p.when) {
                        break;
                    }
                    if (needWake && p.isAsynchronous()) {
                        needWake = false;
                    }
                }
                // 插入到查找到的消息位置
                msg.next = p; // invariant: p == prev.next
                prev.next = msg;
            }

           	// 非头部不需要唤醒
    		// We can assume mPtr != 0 because mQuitting is false.
            if (needWake) {
                nativeWake(mPtr);
            }
        }
        return true;
    }
```





## 5. 消息队列设计优势











### 思考问题：

消息唤醒机制   eventFd

Handler中的监控机制设计

