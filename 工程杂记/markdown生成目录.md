如何为 Markdown 文件（即 .md 格式的文件）自动生成目录呢？下面给大家介绍两种方法：

- Visual Studio Code + Markdown TOC 扩展
- Pandoc 命令

## 1. Visual Studio Code + TOC 扩展

Visual Studio Code (VS Code) 是一个由微软开发的，同时支持 Windows、Linux 和 macOS 操作系统的开源文本编辑器。它支持调试，内置了 Git 版本控制功能，同时也具有开发环境功能，例如代码补全、代码片段、代码重构等。

![img](https:////upload-images.jianshu.io/upload_images/4193138-0ac91713edb6a4a7.png?imageMogr2/auto-orient/strip|imageView2/2/w/394/format/webp)

如果你对 VS Code 的图标感兴趣，可以参考这篇文章：[The Icon Journey](https://link.jianshu.com?t=https://code.visualstudio.com/blogs/2017/10/24/theicon)

VS Code 编辑器支持用户自定义配置，例如改变主题颜色、键盘快捷方式、编辑器属性和其他参数。另外，还支持扩展程序，并在编辑器中内置了扩展程序管理的功能。

![img](https:////upload-images.jianshu.io/upload_images/4193138-808b6d9522cf7aa7.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

VS Code 支持的扩展

到底如何使用 VS Code + TOC 扩展为 Markdown 文件自动生成目录呢？具体操作步骤如下：

**1. 下载和安装 Visual Studio Code。**

下载地址：[https://code.visualstudio.com/download](https://link.jianshu.com?t=https://code.visualstudio.com/download)

![img](https:////upload-images.jianshu.io/upload_images/4193138-adf8bd3f917865d5.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

安装成功后，双击图标打开，显示如下：

![img](https:////upload-images.jianshu.io/upload_images/4193138-aa57e1ffcda43de6.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

**2. 单击 VS Code 的扩展图标，在搜索框搜索 `Markdown TOC` 并安装。**

![img](https:////upload-images.jianshu.io/upload_images/4193138-4a0a4677160544ca.png?imageMogr2/auto-orient/strip|imageView2/2/w/1068/format/webp)

VS Code-extension-icon

此扩展长这样：

![img](https:////upload-images.jianshu.io/upload_images/4193138-0b1ed79270f50f69.jpeg?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

安装成功后，点击左侧扩展图标，可查看已安装的扩展。如下图所示：

![img](https:////upload-images.jianshu.io/upload_images/4193138-573abb69a55ea00d.png?imageMogr2/auto-orient/strip|imageView2/2/w/1164/format/webp)

**3. 点击菜单栏的`文件` -> `打开`，打开需要生成目录的 .md 格式的文件。**

以如下 FAQ.md 文件为例：

![img](https:////upload-images.jianshu.io/upload_images/4193138-d9622a30fc7fb945.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

在 MacDown 中的显示

FAQ.md 在 VS Code 中打开后显示如下：

![img](https:////upload-images.jianshu.io/upload_images/4193138-4e260f07c5e684e3.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

**4. 将光标移至需要插入目录的位置，右键单击 `Markdown TOC: Insert/Update [^M T]`，目录即自动插入。**

![img](https:////upload-images.jianshu.io/upload_images/4193138-19b7614fb5a36539.png?imageMogr2/auto-orient/strip|imageView2/2/w/1084/format/webp)

显示效果如下：

![img](https:////upload-images.jianshu.io/upload_images/4193138-287a411dcc2e1531.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

**5. 单击右上角的预览图标，可查看目录的显示效果。**

![img](https:////upload-images.jianshu.io/upload_images/4193138-e2b03fb3eae3af53.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

预览图标

显示效果如下：

![img](https:////upload-images.jianshu.io/upload_images/4193138-58839acb24f70530.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

**注**：为保持文档整洁，删除目录首尾的如下字符：



```xml
<!-- TOC -->
<!-- /TOC -->
```

**6. 保存，关闭文件。**

## 2. Pandoc 命令

Pandoc 是由 John MacFarlane 开发的标记语言转换工具，可实现不同标记语言间的格式转换，堪称该领域中的“瑞士军刀”。Pandoc 使用 Haskell 语言编写，以命令行形式实现与用户的交互，可支持多种操作系统。

如何使用 pandoc 命令为 Markdown 文件自动生成目录呢？仍以 FAQ.md 文件为例，具体操作步骤如下：

**1. 下载和安装 pandoc。**

下载地址：[https://github.com/jgm/pandoc/releases](https://link.jianshu.com?t=https://github.com/jgm/pandoc/releases)

![img](https:////upload-images.jianshu.io/upload_images/4193138-75dce2d059f24a58.png?imageMogr2/auto-orient/strip|imageView2/2/w/1174/format/webp)

关于安装，可参考：[https://pandoc.org/installing.html](https://link.jianshu.com?t=https://pandoc.org/installing.html)

**2. 打开终端，输入 `pandoc --version` 确认 pandoc 已成功安装。**

此命令返回结果如下图所示：

![img](https:////upload-images.jianshu.io/upload_images/4193138-f1af4e369696683f.jpeg?imageMogr2/auto-orient/strip|imageView2/2/w/1140/format/webp)

**3. 依次使用以下命令，转到 FAQ.md 文件所在的目录。**

- `pwd`：查看查看当前目录路径，“printing working directory” 的缩写。
- `ls`：查看目录列表，“list segment” 的缩写。
- `cd`：转到某目录下，是 “change directory” 的缩写。

具体使用举例：

![img](https:////upload-images.jianshu.io/upload_images/4193138-bf094c03870a92c7.png?imageMogr2/auto-orient/strip|imageView2/2/w/1140/format/webp)

或者，如果你清楚地知道文档所在目录，可以使用如下简化的操作：

![img](https:////upload-images.jianshu.io/upload_images/4193138-b1d313c2b3eddf9e.jpeg?imageMogr2/auto-orient/strip|imageView2/2/w/806/format/webp)

详细的使用说明可参阅：[https://pandoc.org/getting-started.html#step-3-changing-directories](https://link.jianshu.com?t=https://pandoc.org/getting-started.html#step-3-changing-directories)

**4. 输入以下命令，即可自动生成目录。**



```undefined
pandoc -s --toc --toc-depth=4 FAQ.md -o FAQ.md
```

**注**：pandoc 默认生成三级目录。以上述命令为例，如果使用如下命令则只会生成三级目录：



```css
pandoc -s --toc FAQ.md -o FAQ.md
```

而我想让 FAQ.md 这篇文档生成四级目录，所以加了个参数 `--toc-depth`，并将其值设置为 4。大家可根据具体需求进行设置。

**5. 打开 .md 文档，查看目录。**

命令已成功为 FAQ.md 文件生成了目录，显示如下：

![img](https:////upload-images.jianshu.io/upload_images/4193138-e309f080f21841f6.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

![img](https:////upload-images.jianshu.io/upload_images/4193138-d99498300462f4f5.png?imageMogr2/auto-orient/strip|imageView2/2/w/1180/format/webp)

如果你想了解 pandoc 的更多功能和参数使用，可参考 pandoc 官网的文档：[https://pandoc.org/MANUAL.html](https://link.jianshu.com?t=https://pandoc.org/MANUAL.html)

## Afterword

以上两种方法，我更常用的是 Visual Studio Code 中的 Markdown TOC 扩展，因为操作起来既方便又直观。有需求的小伙伴赶快试一试吧！
