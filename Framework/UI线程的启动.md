UI 线程和主线程相同？



UI线程在Activity attach的时候被创建。

ViewRootImpl 在onresume之后创建， 在没创建之前调用了。



Activity UI线程就是主线程

View  UI线程是ViewRootImpl 创建所在的线程

