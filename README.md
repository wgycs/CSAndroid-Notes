## 说明



这里梳理了Android进阶的笔记，供奋斗在Android道路上的队友参考，我学习历程以及目标方向，其中涉及到的书籍和视频教程的笔记等内容，后续整理将逐步在此更新。

# :star:技能点 

-----

## 语言基础  :star2:

> C/ C++


> NDK


> Java
### 参考资料

* **《Java Concurrency In Practice》** 

* **《深入理解JAVA虚拟机》**

  


## 网络基础 

* **现任明教教主 -《*TCP*/*IP详解*卷1:协议》** 
  * 1.网络通信原理TCP/IP 和 UDP
  * 2.路由过程详解
  * 3.socket 通信TCP粘包和拆包
  * 4.Http 请求过程



##  Android  Framework :arrow_up_small: 

### 参考资料

* **慕课---风语： [剖析Framework 冲击Android高级职位](https://coding.imooc.com/class/chapter/340.html#Anchor)**   (完成)   --> [:notebook:](#Framework)
  * 1.系统启动流程
  * 2.进程间通信机制原理和优缺点
  * 3.线程间通信方式深入理解
  * 4.Activity和Service的启动流程
  * 5.UI体系相关内容，如Vsync机制、surface原理等
*  **罗升阳 ---《Android系统源代码情景分析 》**
*  **林学森 --- 《深入理解 Android内核设计思想》**



### :heavy_check_mark: 知识点

* 操作系统基础
  * Android 同步机制
  * 操作系统内存管理基础
  * Ashmem匿名共享内存机制实现原理
* Android 进程/线程的内存优化
* Android启动原理
* 组件运行状态管理机制AMS
* 窗口和界面显示管理器WMS
* View体系
* Android音频系统追溯
* 系统播放器MediaPlayer/AwesomePlayer/NuPlayer
* OpenGL图像渲染和优化
* Android安全机制解析
* Android应用程序编译和打包



## Android优化进阶 :1st_place_medal:

### 绘制优化

### 内存优化

存储优化

稳定性优化

耗电优化

网络优化

应用瘦身



## Android 音视频直播技术  :video_camera:



| 流程 | 内容                                              |
| ---- | ------------------------------------------------- |
| 采集 | 音频：openSL ES  <br />视频：surfaceTexture、 YUV |
| 编码 | H264、H265、MediaCodec                            |
| 传输 | TCP/UDP                                           |
| 解码 | H264、H265                                        |
| 渲染 | OpenGL、默认渲染                                  |



> ijkplayer  基于ffmpeg的移动平台视频播放器     [**:b:站 Github**](https://github.com/bilibili/ijkplayer)





> FFmpeg    参考使用实例   [:a: FFmpegAndroid](https://github.com/xufuji456/FFmpegAndroid)

### :heavy_check_mark: 知识点

* 音视频基础原理

* 视频编解码网络传输原理

* AAC音频格式和转换

* H.264编码压缩算法

*  H. 264 视频数据格式解码

* 硬件编解码H. 264 

* FFmpeg 跨平台开发




> webRTC



## OpenGL  :triangular_flag_on_post:





## 图像处理技术



## 人脸识别方向



## 设计思想

* **《软件构架实践》**
* 弗农（美） --《实现领域驱动设计》




## 思想框架
* **《金字塔原理》**

* **《毛泽东选集》**
* 《矛盾论》
  * 《实践论》






# :black_nib:笔记 

----



##  网络基础 


* [ARP_ICMP.md](./网络基础/ARP_ICMP.md)
* [HTTP.md](./网络基础/HTTP.md)
* [UDP.md](./网络基础/UDP.md)


## Framework

* [Activity启动流程.md](./Framework/Activity启动流程.md)
* [Activity的显示原理.md](./Framework/Activity的显示原理.md)
* [Android启动机制汇总与对比.md](./Framework/Android启动机制汇总与对比.md)
* [IPC通信的方式汇总.md](./Framework/IPC通信的方式汇总.md)
* [Provider跨进程通信.md](./Framework/Provider跨进程通信.md)
* [U-boot源码分析.md](./Framework/U-boot源码分析.md)
* [UI线程的启动.md](./Framework/UI线程的启动.md)
* [Vsync原理.md](./Framework/Vsync原理.md)
* [zygote理解.md](./Framework/zygote理解.md)
* [应用Service启动流程.md](./Framework/应用Service启动流程.md)
* [应用进程启动.md](./Framework/应用进程启动.md)
* [添加系统服务.md](./Framework/添加系统服务.md)
* [系统启动.md](./Framework/系统启动.md)

## 应用优化


* [AOP框架Aspectjx使用.md](./应用优化/AOP框架Aspectjx使用.md)
* [内存优化.md](./应用优化/内存优化.md)
* [单例模式.md](./应用优化/单例模式.md)
* [启动优化.md](./应用优化/启动优化.md)
* [绘制原理.md](./应用优化/绘制原理.md)


## 信息安全

* [个人信息安全APP治理存在问题.md](./信息安全/个人信息安全APP治理存在问题.md)



## 工程杂记

* [AOSP工程同步笔记](./工程杂记/获取AOSP工程步骤.md)

