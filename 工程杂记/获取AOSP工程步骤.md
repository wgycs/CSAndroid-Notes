## 1. 环境准备

1.  windows下载安装Cygwin环境，[Cygwin官网](https://cygwin.com/index.html)

   安装可直接使用默认配置，最后一步选择国内源比如 163源

2.  安装SourceInsight 代码阅读器



## 2. 下载repo工具并配置

### repo下载

```bash
mkdir ~/bin
PATH=~/bin:$PATH
curl -sSL  'https://gerrit-googlesource.proxy.ustclug.org/git-repo/+/master/repo?format=TEXT' |base64 -d > ~/bin/repo
chmod a+x ~/bin/repo
```





### 编辑repo更换REPO_URL地址

```bash
可以编辑 ~/bin/repo，把 REPO_URL 一行替换成下面的：
REPO_URL = 'https://gerrit-googlesource.proxy.ustclug.org/git-repo'
```



## 3. 选择特定版本初始化仓库

```bash
repo init -u git://mirrors.ustc.edu.cn/aosp/platform/manifest -b android-10.0.0_r1
```

注：[版本列表](http://mirrors.ustc.edu.cn/aosp/platform/manifest.git/refs/heads/)

```bash
android-10.0.0_r1                                  06-Sep-2019 00:38                  41
android-10.0.0_r10                                 05-Nov-2019 21:47                  41                              
```



## 4. 运行同步代码

```bash
repo sync
```