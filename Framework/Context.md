### 问题描述

Context 是什么的？

有哪些组件有Context? 

这些组件和Context什么关系？ 

不同的Context有什么区别？



先看一张类图：



![Context继承关系](image/Context继承关系.png)



#### 1. Context是什么？

看源码中的注释讲的非常清楚，不需要过多解释。简单说就是访问Android系统资源的媒介。

```java
/**
* Interface to global information about an application environment.  This is
* an abstract class whose implementation is provided by
* the Android system.  It allows access to application-specific resources and classes, as well as
* up-calls for application-level operations such as launching activities,
* broadcasting and receiving intents, etc.
*/
```



