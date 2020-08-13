[TOC]


[官方Cmake语法原文](https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#organization)
## Cmake工具
- cmake  交叉编译系统生成工具
- ctest  自动化测试工具
- cpack  自动化打包工具 可以生成各种格式的安装程序和源码包



## Cmake 语法
相比于make的规则，输入文件有指定的命名规则即为`Makefile`. \
Cmake 输入文件是以Cmake语法编写的，以`CmakeLists.txt命`名或以`.cmake`扩展名的文件.为了尽可能的跨平台使用的7-bit ASCII 字符编写，使用UTF-8编码。

### 1. 多级依赖目录树和配置文件配置
- 使用`add_subdirectory()`函数，添加同样包含`CmakeList.txt`,Cmake进行编译时，会在build相应的目录下生成输出文件.
- 通用资源或配置可以添加`<script>.cmake`,以模块的形式进行加载，相应的加载函数为`include()`.
- 单独运行配置文件,使用`-P`选项 如：`cmake -P <script>.cmake`

### 2. 命令调用

#### 命令格式
命令调用是方法名加圆括号的形式，括号内的参数以空格或换行符分割开。方法命名不区分大小写。

```cmake
line_ending  ::=  line_comment? newline
space        ::=  <match '[ \t]+'>
newline      ::=  <match '\n'>
separation   ::=  space | line_ending
```

#### 三种参数格式支持

命令调用支持三种语法格式，分别是引用格式、未引用格式、lua长括号语法。\
未引用格式所有 空格` `、`(`、`)`、`#`、`"`、`\`都应该使用转译符`\`进行注释\
实例如下：
```cmake
#引用语法（quoted argument ）
message(STATUS "config is called syntax 1 ")
#未引用语法（unquoted argument）
message(STATUS config\ is\ called\ syntax\ 2)
#长括号语法（Bracket Argument）
message(STATUS [==[config is called syntax 3]==])

#result
cmake -P ../app/config.cmake
-- config is called syntax 1
-- config is called syntax 2
-- config is called syntax 3

```
#### 变量引用
引用变量格式为`${<variable>}`，可以在引用格式或未引用格式中使用。支持变量的嵌套，由内而外的解析`${outer_${inner_variable}_variable}`。

#### 注释
注释应该以`#`开头，支持lua长括号语法\
```cmake
# this is a Comment

#[=[ lua long bracket syntax Comment]=]  #可多行
```

### 3. 控制语句
控制语句主要分为以下几类：
- 条件语句
- 循环语句
- 宏、函数定义
- 变量、环境变量
- 列表


#### 条件语句
使用`if()`/`elseif()`/`else()`/`endif()` 命令分割代码块完成条件控制。

```Cmake
if(<condition>)
  <commands>
elseif(<condition>) # optional block, can be repeated
  <commands>
else()              # optional block
  <commands>
endif()
```

#### 循环语句
使用`foreach()`/`endforeach()` / `while()`/`endwhile()` 来划分代码块用以在循环中执行。类似于其他语言使用 `break()`提前结束循环， 使用 `continue()` 函数提前开始下一个迭代过程。
```Cmake
#foreach 遍历循环
foreach(<loop_var> <items>)
  <commands>
endforeach()

#while条件循环
while(<condition>)
  <commands>
endwhile()
```

#### 宏、函数定义
使用 `macro()`/`endmacro()`, and `function()`/`endfunction()` 命令定义宏或者函数，在后面作为新的命令调用相应代码块。

#### 变量、环境变量
变量和环境变量类型都是字符串类型，使用`set()`和`unset()`命令令进行定义和撤销变量，但是其他命令可以更新变量值。注意，变量名不同于命令是区分大小写的，理论上名命可以是任意字符，但是只推荐使用`-`和`_`作为分隔符。\
环境变量的区别在于，作用域是当前Cmake进程，设置和引用时要增加`ENV`标记.

```Cmake
#变量设置
set(<variable> <value>... CACHE <type> <docstring> [FORCE])
#变量引用
${<variable>}

#环境变量设置
set(ENV{<variable>} [<value>])
#环境变量引用
$ENV{<variable>}
```

#### 列表
列表是以`;`区分开的字符串，而且大多数的命令并不会自动转译掉`;`，因此可以扁平化嵌套列表.
```Cmake
set(x a "b;c") # sets "x" to "a;b;c", not "a;b\;c"
```