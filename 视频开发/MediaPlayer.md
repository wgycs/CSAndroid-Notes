## 1、MediaPlayer的使用



```java
// 获取surface的句柄
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

mPlayer.setDisplay(holder);    //设置显示视频显示在SurfaceView上
// 开始播放
mPlayer.start();
```



## 2、 MediaPlayer 状态周期

![img](https://upload-images.jianshu.io/upload_images/10190436-784f671f475cbc7c.gif?imageMogr2/auto-orient/strip|imageView2/2/w/665/format/webp)



> 注解： 图中椭圆代表MediaPlayer驻留的状态，弧代表播放控制切驱动MediaPlayer进行状态过度。  两种箭头类型，单箭头表示同步函数调用，双箭头表示异步函数调用。



过程解析：

1、 MediaPlayer调用`create()`完成实例创建 ，此时处于**Idle** 状态 ， 调用`release()`进入**End** 状态。



## MediaPlayer实例创建

```java
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
        // 准备进入Idle 状态
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



// 构造函数
public MediaPlayer() {
    super(new AudioAttributes.Builder().build(),
          AudioPlaybackConfiguration.PLAYER_TYPE_JAM_MEDIAPLAYER);

    // 在对应线程创建 Handler 
    // 用于管理状态周期
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
    // mHandlerThread = new HandlerThread("MediaPlayerMTPEventThread",Process.THREAD_PRIORITY_FOREGROUND);
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