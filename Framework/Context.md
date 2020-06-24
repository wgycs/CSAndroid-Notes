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





#### 2. 几个关键函数说明Context的设置流程

```java
 @Override
 public Activity handleLaunchActivity(ActivityClientRecord r,
            PendingTransactionActions pendingActions, Intent customIntent) {
     // ... 
    performLaunchActivity(r, customIntent);
 }

// ActivityThread.java
private Activity performLaunchActivity(ActivityClientRecord r, Intent customIntent) {
    // 创建Base Context对象
	ContextImpl appContext = createBaseContextForActivity(r);  // --> ContextImpl.createActivityContext
    // 获取classLoader 创建Activity对象
    java.lang.ClassLoader cl = appContext.getClassLoader();
    activity = mInstrumentation.newActivity(cl, component.getClassName(), r.intent);
    // 创建Application
    Application app = r.packageInfo.makeApplication(false, mInstrumentation);
    // 调用Attach，
    activity.attach(appContext, this, getInstrumentation(), r.token,
                        r.ident, app, r.intent, r.activityInfo, title, r.parent,
                        r.embeddedID, r.lastNonConfigurationInstances, config,
                        r.referrer, r.voiceInteractor, window, r.configCallback,
                        r.assistToken);

}


//1. Application Context 设置流程
public Application makeApplication(boolean forceDefaultAppClass,
            Instrumentation instrumentation) {
	ava.lang.ClassLoader cl = getClassLoader();
    // 
    app = mActivityThread.mInstrumentation.newApplication(cl, appClass, appContext);
    
    
    ContextImpl appContext = ContextImpl.createAppContext(mActivityThread, this);
}


//1. Application Context 设置流程
public Application newApplication(ClassLoader cl, String className, Context context)
            throws InstantiationException, IllegalAccessException, 
            ClassNotFoundException {
        Application app = getFactory(context.getPackageName())
                .instantiateApplication(cl, className);
        app.attach(context);
        return app;
}

//2.  Activity 的Context 设置流程
//Activity.java
final void attach(Context context, ActivityThread aThread,...)
{
    // 设置Base Context对象
    attachBaseContext(context);  
    
    ...
    mWindow = new PhoneWindow(this, window, activityConfigCallback);
    ...
}


// ContextWrapper.java   -->  extends Context
protected void attachBaseContext(Context base) {
    if (mBase != null) {
        throw new IllegalStateException("Base context already set");
    }
    mBase = base;
}
```



