# 一、AspectJX介绍

​	面向切面编程的思想给开发带来了崭新的思路，Aspectjx是一个基于AspectJ并在此基础上扩展出来可应用于Android开发平台的AOP框架，可作用于java源码，class文件及jar包，同时支持kotlin的应用。

# 二、AspectJX 环境依赖
## AspectJX最新版本
`com.hujiang.aspectjx:gradle-android-plugin-aspectjx:2.0.10`

## gradle plugin version
version   :   `com.android.tools.build:gradle:3.6.1`
配置路径：project->build.gradle

```groovy
dependencies {
        classpath 'com.android.tools.build:gradle:3.6.1'
    }
```

## gradle version
`gradle-5.6.4-all.zip`

配置路径：`gradle/wrapper/gradle-wrapper.properties`



# 三、AspectJX 配置步骤

## 1.  在项目根目录的build.gradle中插入AspectJX

```groovy
dependencies {
    	//...
        classpath 'com.android.tools.build:gradle:3.6.1'
        classpath 'com.hujiang.aspectjx:gradle-android-plugin-aspectjx:2.0.10'
}
```



## 2. 在AspectJ 代码Model中增加aspectjrt依赖

```groovy
dependencies {
	//...
    implementation 'org.aspectj:aspectjrt:1.9.5'
}
```



##  3.在主工程（app）的build.gradle 中增加依赖

```groovy
//增加 aspectjx 插件
apply plugin: 'android-aspectjx'

// 增加aspectj module依赖
dependencies {
	//...
    api project(':aspect')
}
```



## 4. 在aspect Module中创建AspectJ的java文件 

```java
//1. 增加Aspect注解声明AOP工程文件
@Aspect
public class AspectJxAOP {

    private static final String TAG = "AspectJxAOP";

    // 添加方法 AspectJ Language 的注解，过滤对应方法
    @Before("execution(* com.wgycs.aoptest.MainActivity+.on**(..))")
    public void onActivityMethodBefore(JoinPoint joinPoint) throws Throwable {
        MethodSignature methodSignature = (MethodSignature) joinPoint.getSignature();
        Method method = methodSignature.getMethod();
        Log.d(TAG, "onActivityMethodBefore: " + method.getName());
    }
}
```



app工程中的MainActivity代码如下：

```java
public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    @Override
    protected void onResume() {
        super.onResume();
    }
}
```



## 运行结果

```
4008-4008/com.wgycs.aoptest D/AspectJxAOP: onActivityMethodBefore: onCreate
4008-4008/com.wgycs.aoptest D/AspectJxAOP: onActivityMethodBefore: onResume
```



# 四、AspectJ 语法

主要参考官方文档：

https://www.eclipse.org/aspectj/doc/released/progguide/language.html












