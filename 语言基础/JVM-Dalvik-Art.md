### Android虚拟机和Java虚拟机的不同

1. JVM 

   虚拟机实现相对简单，运行java字节码。 

   JVM是基于栈的，必须包含push和pop指令移动变量。

   执行速度较寄存器Dalvik更慢。

   // 执行 a = 1;b = 2; c = (a+b) * 5;

   

   ![img](https://upload-images.jianshu.io/upload_images/1716536-c0fd628c5c299775.gif?imageMogr2/auto-orient/strip|imageView2/2/w/420/format/webp)

2. Dalvik

   支持JIT(Just In Time,即时编译)技术

   运行Dalvik字节码，并打包成Dex可执行文件，相对java字节码体积更小。

   基于寄存器免去了pop和push的麻烦，减少了指令总数。即时指令条数和移动次数都低于JVM虚拟机。

   // 执行 a = 1;b = 2; c = (a+b) * 5;

   ![img](https://upload-images.jianshu.io/upload_images/1716536-ae4fc34ec35ad15f.gif?imageMogr2/auto-orient/strip|imageView2/2/w/460/format/webp)

   

   

3. ART

   使用AOT(Ahead Of Time，预编译)技术

   应用安装过程中dex中的字节码将被编译成本地机器码，使用将直接执行本地机器码。

   优点：系统更流畅、性能更高，更省电。

   缺点：应用安装时间长，且更占存储空间。

