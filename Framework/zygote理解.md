### zygote作用

1. 启动SystemServer
2. 孵化应用进程



### zygote启动流程

init.rc  -->  init进程 -->  fork + execve  ---> zygote



1.  Native层准备进入JAVA层    

   创建JVM虚拟机-->注册JNI基础函数--> 进入java 

2.  Java层

   预加载资源-- >  启动SystemServer(独立进程) --> Loop  循环等待接收Socket消息

​                                       forkSystemServer

### zygote的工作原理

怎么启动进程，怎么进行通信



要点：

1. zygote的作用
2. 启动步骤
3. 怎么孵化进程？  fork + execve  /  fork + handle 