## 1、MediaPlayer的使用

要完成播放动作要做哪些事情？

1. 创建播放器
2. 将资源设置到MediaPlayer中，资源可以是url、文件、uri等
3. 设置显示的位置
4. 设置声音播放
5. 状态控制，如开始播放、停止、暂停、设置播放状态等



这也就是我们**使用MediaPlayer**的一般步骤：

```java
SurfaceHolder holder = surfaceView.getHolder();
// surface 创建完成设置句柄到MediaPlayer
mPlayer = MediaPlayer.create(MainActivity.this,
        Uri.parse("http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4"));

//原废弃接口 mPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC);
//AudioAttributes是一个封装音频各种属性的类
AudioAttributes.Builder attrBuilder = new AudioAttributes.Builder();
//设置音频流的合适属性
attrBuilder.setLegacyStreamType(AudioManager.STREAM_MUSIC);
// 必须在prepare之前调用
mPlayer.setAudioAttributes(attrBuilder.build());
//设置显示视频显示在SurfaceView上
mPlayer.setDisplay(holder);    
// 开始播放
mPlayer.start();
```



但是**MediaPlayer是怎么工作的**？

要完成播放我们至少有几件事情要做呢？

1.  如果不是一个文件怎么拿到文件？ 比如现在是一个url，怎么进行播放呢？
2. 拿到文件怎么解码？
3. 解码出的音频怎么播放？
4. 解码的帧数据怎么渲染？
5. 怎么进度控制？





## 2、 MediaPlayer 状态周期



在分析前面问题之前我们先弄清楚MediaPlayer是怎么创建和状态切换的。

看官方图：

![img](https://upload-images.jianshu.io/upload_images/10190436-784f671f475cbc7c.gif?imageMogr2/auto-orient/strip|imageView2/2/w/665/format/webp)



> 注解： 图中椭圆代表MediaPlayer驻留的状态，弧代表播放控制切驱动MediaPlayer进行状态过度。  两种箭头类型，单箭头表示同步函数调用，双箭头表示异步函数调用。



过程解析：

1、 MediaPlayer调用`create()`完成实例创建 ，此时处于**Idle** 状态 ， 调用`release()`进入**End** 状态。

2、调用`SetDataSource()`完成播放器初始化，由**Idle**状态转为**Initialized**状态







### 2.1 MediaPlayer实例创建

```java
// MediaPlayer 提供了一个组合方法，一次性到达就绪（Prepared）状态。 
// 其实 这也就是我们使用MediaPlayer的流程。
//  ---> Idle ---> Initialized ---> Prepared   ---> 后面可以启动了
public static MediaPlayer create(Context context, Uri uri, SurfaceHolder holder,
        AudioAttributes audioAttributes, int audioSessionId) {

    try {
        // 创建了实例对象
        MediaPlayer mp = new MediaPlayer();
        final AudioAttributes aa = audioAttributes != null ? audioAttributes :
            new AudioAttributes.Builder().build();
        // 构建并为MediaPlayer设置一个 AudioAttributes， 用于音频处理
        mp.setAudioAttributes(aa);
        // AudioSystem中获取并设置声音的会话ID
        // ----  使用示例
        //int s = AudioSystem.newAudioSessionId();
        //create(context, uri, holder, null, s > 0 ? s : 0);
        // ----
        mp.setAudioSessionId(audioSessionId);
        // 设置媒体资源， url 。可以是文件也可以是HTTP地址
        mp.setDataSource(context, uri);
        if (holder != null) {
            // 设置surface的操纵句柄， 处理其在Canvas上作画的效果和动画、大小、像素等
            mp.setDisplay(holder);
        }
        // 同步准备的方法 还有一个异步的prepareAsync()   ，进入Prepared 状态
        // 主要是这里非常耗时 ，同步的方法会一直阻塞到能够播放为止。
        mp.prepare();
        return mp;
    } catch (IOException ex) {
        Log.d(TAG, "create failed:", ex);
        // fall through
    } catch (IllegalArgumentException ex) {
        Log.d(TAG, "create failed:", ex);
        // fall through
    } catch (SecurityException ex) {
        Log.d(TAG, "create failed:", ex);
        // fall through
    }

    return null;
}



// 这个函数只完成了准备操作，到达Idle状态。
public MediaPlayer() {
    super(new AudioAttributes.Builder().build(),
          AudioPlaybackConfiguration.PLAYER_TYPE_JAM_MEDIAPLAYER);

    // 在对应线程创建 Handler 
    // 用于管理状态周期，优先创建子线程Handler，实在没有就只能用主线程了
    Looper looper;
    if ((looper = Looper.myLooper()) != null) {
        mEventHandler = new EventHandler(this, looper);
    } else if ((looper = Looper.getMainLooper()) != null) {
        mEventHandler = new EventHandler(this, looper);
    } else {
        mEventHandler = null;
    }
	// 时间数据容器，内部有独立线程 
    // ----
    // mHandlerThread = new         HandlerThread("MediaPlayerMTPEventThread",Process.THREAD_PRIORITY_FOREGROUND);
    // ----
    // 用户管理播放进度  并发送消息给mEventHandler;   scheduleNotification -->  mEventHandler
    mTimeProvider = new TimeProvider(this);
    // 输入数据流 管理数组
    mOpenSubtitleSources = new Vector<InputStream>();

    /* Native setup requires a weak reference to our object.
         * It's easier to create it here than in C++.
         */
    native_setup(new WeakReference<MediaPlayer>(this));
	// 获取应用权限管理系统服务（Application Operations）通信Binder句柄
    // IBinder b = ServiceManager.getService(Context.APP_OPS_SERVICE);
    // mAppOps = IAppOpsService.Stub.asInterface(b);
    baseRegisterPlayer();
}
```



### 2.2 MediaPlayer的初始化状态转变

setDataSource有很多重载方法：分别对应了uri、文件、文件描述符、MediaDataSource
```java
public void setDataSource(@NonNull Context context, @NonNull Uri uri)
public void setDataSource(String path)
public void setDataSource(FileDescriptor fd, long offset, long length)
public void setDataSource(MediaDataSource dataSource)
```

后面三种相对比较单一，我们看一个比较典型的uri方式的`setDataSource()`

```java
    
/* @param context the Context to use when resolving the Uri
*  @param uri the Content URI of the data you want to play
*  @param headers the headers to be sent together with the request for the data
*                The headers must not include cookies. Instead, use the cookies param.
*  @param cookies the cookies to be sent together with the request
* 这几个参数分别是   上下文、uri，跟随请求一起发送的header和cookies
*/
public void setDataSource(@NonNull Context context, @NonNull Uri uri,
            @Nullable Map<String, String> headers, @Nullable List<HttpCookie> cookies)
            throws IOException {
       // --- ↓ 
       if (context == null) {
            throw new NullPointerException("context param can not be null.");
        }

        if (uri == null) {
            throw new NullPointerException("uri param can not be null.");
        }

        if (cookies != null) {
            CookieHandler cookieHandler = CookieHandler.getDefault();
            if (cookieHandler != null && !(cookieHandler instanceof CookieManager)) {
                throw new IllegalArgumentException("The cookie handler has to be of CookieManager "
                        + "type when cookies are provided.");
            }
        }
       //---  ↑  上面这些都是异常校验 不说了 
    
        // 这里是使用由易到难的策略，去筛检到的这个uri是什么类型  -->
    
        // The context and URI usually belong to the calling user. Get a resolver for that user
        // and strip out the userId from the URI if present.
        final ContentResolver resolver = context.getContentResolver();
        final String scheme = uri.getScheme();
        final String authority = ContentProvider.getAuthorityWithoutUserId(uri.getAuthority());
		// --> 这里先看是不是普通的文件 scheme ？
        if (ContentResolver.SCHEME_FILE.equals(scheme)) {
            setDataSource(uri.getPath());
            return;
        // --> 是设置中content类型的资源？
        } else if (ContentResolver.SCHEME_CONTENT.equals(scheme)
                && Settings.AUTHORITY.equals(authority)) {
            // Try cached ringtone first since the actual provider may not be
            // encryption aware, or it may be stored on CE media storage
            final int type = RingtoneManager.getDefaultType(uri);
            final Uri cacheUri = RingtoneManager.getCacheForType(type, context.getUserId());
            final Uri actualUri = RingtoneManager.getActualDefaultRingtoneUri(context, type);
            if (attemptDataSource(resolver, cacheUri)) {
                return;
            } else if (attemptDataSource(resolver, actualUri)) {
                return;
            } else {
                setDataSource(uri.toString(), headers, cookies);
            }
    	// ---> 那可能就不是一个已知的类型
        } else {
            // Try requested Uri locally first, or fallback to media server
            // 这里还是先看是不是本地的文件，如果还不是，那么没办法了，只能走下面的方法，向媒体服务器汇报。
            if (attemptDataSource(resolver, uri)) {
                return;
            } else {
                // --- 其他都无能为力，只能这个来处理了
                setDataSource(uri.toString(), headers, cookies);  // ----> 最终是下面的实现
            }
        }
    }




@UnsupportedAppUsage
    private void setDataSource(String path, String[] keys, String[] values,
            List<HttpCookie> cookies)
            throws IOException, IllegalArgumentException, SecurityException, IllegalStateException {
        final Uri uri = Uri.parse(path);
        final String scheme = uri.getScheme();
        if ("file".equals(scheme)) {
            path = uri.getPath();
        } else if (scheme != null) {
            // 发现没有文件，只能请求了。 调用的是C++中的方法
            // handle non-file sources
            nativeSetDataSource(
                // 这里很关键  创建和MediaHTTPService通信Binder句柄  // (new MediaHTTPService(cookies)).asBinder()
                // 后面只能交给媒体服务去处理了
                MediaHTTPService.createHttpServiceBinderIfNecessary(path, cookies),
                path,
                keys,
                values);
            
            return;
        }

        final File file = new File(path);
        try (FileInputStream is = new FileInputStream(file)) {
            setDataSource(is.getFD());
        }
    }
```

#### 番外篇

这里是怎么调到native层的呢？ 

我们看一个关键函数 `JNI_OnLoad()`, 这个函数在动态库被加载的时候调用到。

` System.loadLibrary("lib_media");`

然后会调用runtime的注册函数，registerNativeMethods。 这时就会把native层的函数和java层函数完成一个绑定。

```java

 private native void nativeSetDataSource(
        IBinder httpServiceBinder, String path, String[] keys, String[] values)
        throws IOException, IllegalArgumentException, SecurityException, IllegalStateException;

jint JNI_OnLoad(JavaVM* vm, void* /* reserved */)
{
     if (register_android_media_MediaPlayer(env) < 0) {
        ALOGE("ERROR: MediaPlayer native registration failed\n");
        goto bail;
    }
    ...
}


static int register_android_media_MediaPlayer(JNIEnv *env)
{
    return AndroidRuntime::registerNativeMethods(env,
                "android/media/MediaPlayer", gMethods, NELEM(gMethods));
}

// JNINativeMethod 结构体，对应的分别是

// java 函数名称
// 函数参数和返回值类型签名  
// native 层函数指针
static const JNINativeMethod gMethods[] = {
    {
        "nativeSetDataSource",
        "(Landroid/os/IBinder;Ljava/lang/String;[Ljava/lang/String;[Ljava/lang/String;)V",
        (void *)android_media_MediaPlayer_setDataSourceAndHeaders
    }
    
    ...
}
```



#### nativeSetDataSource 的 c++层实现 

android_media_MediaPlayer_setDataSourceAndHeaders

```java

static void
android_media_MediaPlayer_setDataSourceAndHeaders(
        JNIEnv *env, jobject thiz, jobject httpServiceBinderObj, jstring path,
        jobjectArray keys, jobjectArray values) {

    sp<MediaPlayer> mp = getMediaPlayer(env, thiz);
    if (mp == NULL ) {
        jniThrowException(env, "java/lang/IllegalStateException", NULL);
        return;
    }

    if (path == NULL) {
        jniThrowException(env, "java/lang/IllegalArgumentException", NULL);
        return;
    }

    const char *tmp = env->GetStringUTFChars(path, NULL);
    if (tmp == NULL) {  // Out of memory
        return;
    }
    ALOGV("setDataSource: path %s", tmp);
   // ---- ↑ 异常判断
    String8 pathStr(tmp);
    env->ReleaseStringUTFChars(path, tmp);
    tmp = NULL;

    // We build a KeyedVector out of the key and val arrays
    KeyedVector<String8, String8> headersVector;
    if (!ConvertKeyValueArraysToKeyedVector(
            env, keys, values, &headersVector)) {
        return;
    }

    // 数据准备和转换
    sp<IMediaHTTPService> httpService;
    if (httpServiceBinderObj != NULL) {
        // 通过Binder机制将httpServiceBinderObj返回给binder
        //就是根据传进来的Java对象找到对应的C++对象，这里的参数obj,可能会指向两种对象：Binder对象或者BinderProxy对象。
        sp<IBinder> binder = ibinderForJavaObject(env, httpServiceBinderObj);
        httpService = interface_cast<IMediaHTTPService>(binder);
    }

    status_t opStatus =
        //调用 c++ 层MediaPlayer setDataSource
        mp->setDataSource(
                httpService,
                pathStr,
                headersVector.size() > 0? &headersVector : NULL);

    process_media_player_call(
            env, thiz, opStatus, "java/io/IOException",
            "setDataSource failed." );
}

```

[ibinderForJavaObject()  与 javaObjectForIBinde() 参考](https://www.cnblogs.com/zhangxinyan/p/3487866.html)



到这这里还没结束，真正的实现都在MediaPlayer.cpp 中，这里维护了所有调度状态，比如设置完`setDataSource()` 将player状态设置为Initialized。完成MediaPlayerService进行绑定和请求发送，当然这肯定是基于Binder机制的。

```c++
//MediaPlayer 设置状态为Initialized
mCurrentState = MEDIA_PLAYER_INITIALIZED;
//MediaPlayer 获取mediaplayerService。
binder = sm->getService(String16("media.player"));
```



#### C++ 层MediaPlayer数据初始化

```cpp

status_t MediaPlayer::setDataSource(
        const sp<IMediaHTTPService> &httpService,
        const char *url, const KeyedVector<String8, String8> *headers)
{
    ALOGV("setDataSource(%s)", url);
    status_t err = BAD_VALUE;
    if (url != NULL) {
        
        // 获取MediaPlayerService的服务
        const sp<IMediaPlayerService> service(getMediaPlayerService());
        if (service != 0) {
            // MediaPlayerService 创建 IMediaPlayer Client对象
            sp<IMediaPlayer> player(service->create(this, mAudioSessionId));
            if ((NO_ERROR != doSetRetransmitEndpoint(player)) ||
                // 1. 调用MediaPlayerService client 的setDataSource方法
                // 2. 涉及到 MediaPlayerFactory 创建不同的播放器类型
                // 3. sm->getService(String16("media.extractor")); 获取音视频分离器 media.extractorextractor 
                //    分离容器中的视频track和音频track
                // 4. 绑定对应的 OMX service 和 Codec2 service
                //
                (NO_ERROR != player->setDataSource(httpService, url, headers))) {
                player.clear();
            }
            err = attachNewPlayer(player);
        }
    }
    return err;
}

```

### 2.3 MediaPlayer 就绪状态

`prepare()`





