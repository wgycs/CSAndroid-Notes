## 关于`黄油计划（Project Buffer）`

Android 4.1 版本进行的UI流畅性优化， 重构了Android显示系统。其中包括三个核心元素：

1. **Vsync**： （Vertical Synchronization ， 垂直同步机制） 是一种定时中断机制，包括软件和硬件两种生成方式。

2. **双缓冲机制**： 包括两个Framebuffer，分别是Front Buffer和Back Buffer, 前者用于渲染显示，Back 用于预绘制，而后两者交换。

   ​					 引入第三个buffer ----> Triple Buffer , 利用空闲的CPU时间。

3. **Choreography** ：调度单元，管理用户注册的回调并完成调度策略。



