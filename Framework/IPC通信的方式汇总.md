# Linux 中常用的跨进程通信方式

## 进程通信的一般步骤

Client  -- 序列化  --> 进程间通信机制  ---> 反序列化  --> Server

要求： 性能好、 使用方便、 安全

<img src="./image/一般进程通信流程.png" style="zoom:50%;" />

##  Binder

1. 是CS架构，方便易用。
2. 仅需要一次内存拷贝
3. 安全，在内核态中添加安全认证识别机制
4. 组成：  ServiceManager 、 Binder驱动 、Client 、 Services

<img src="./image/Binder组成机制.png" style="zoom: 50%;" />



5. 分层结构  Proxy、 BinderProxy、 BpBinder -- > Binder驱动 ----> BBinder --> Binder -->Stub



<img src="./image/Binder分层结构.png"  style="zoom:50%;" />



启动Binder机制过程：

1. 打开Binder驱动
2. 文件描述符进行mmap内存映射。
3. 启动Binder线程，注册到Binder驱动，进入Looper循环。





ServiceManager Binder 驱动Id 是 0， 去其他方获取，需统一通过ServiceManager拿取。



这里和网络通信非常相像。

ServiceMnager 是DNS解析。

Binder协议是有确认机制的，类似TCP协议：

<img src="./image/Binder请求协议.png"  style="zoom:50%;" />







## 管道

1. 半双工的通信方式，若想实现全双工，则需要一对描述符。pipe(fds)
2. 一般在父子进程使用
3. 数据量小的跨进程通信

两次拷贝

使用到管道的组件：

Looper



<img src="./image/管道使用方式.png"   style="zoom:50%;" />



## Socket

1. 全双工，可读可写
2. 在两个无亲缘关系的两个进程之间
3. 传输数据流不能太大 

两次拷贝



使用Socket的组件

Zygote   --> AMS 通信

## 



## 共享内存

1. 快  不需要多次拷贝
2. 进程之间无需亲缘关系
3. 数据流较大的传输



使用共享内存地方：

MemoryFile -> SharedManery

创建文件描述符  --> 申请内存空间  -->  Map 拷贝



图片传输相关





## 信号

1. 单向， 无确认机制
2. 只能发信号，不能传参数
3. 只需知道PID即可发信号，可群发信号。 
4. Root权限，或UID相同可发信号



信号的使用：

杀进程：

```java
  public static final void killProcess(int pid) {
        sendSignal(pid, SIGNAL_KILL);
  }
```

Zygote  关注子进程退出流程：

```c++
static void SetSignalHandlers() {
  struct sigaction sig_chld = {};
  sig_chld.sa_handler = SigChldHandler;

  if (sigaction(SIGCHLD, &sig_chld, nullptr) < 0) {
    ALOGW("Error setting SIGCHLD handler: %s", strerror(errno));
  }

  struct sigaction sig_hup = {};
  sig_hup.sa_handler = SIG_IGN;
  if (sigaction(SIGHUP, &sig_hup, nullptr) < 0) {
    ALOGW("Error setting SIGHUP handler: %s", strerror(errno));
  }
}
```





























