## 基本语法

### 特性

1.  类型检测和推断，能够实现自动类型转换。同时可以使用`is`运算符检测表达式的类型。

2. NULL 检查机制（空安全设计），有两种处理方式，字段后加!!像Java一样抛出空异常，另一种字段后加?可不做处理返回值为 null或配合?:做空判断处理

   ```kotlin
   //类型后面加?表示可为空
   var age: String? = "23" 
   //抛出空指针异常
   val ages = age!!.toInt()
   //不做处理返回 null
   val ages1 = age?.toInt()
   //age为空返回-1
   val ages2 = age?.toInt() ?: -1
   ```



### 变量

1. 可变变量

   ```kotlin
   var <标识符> : <类型> = <初始化值>
   ```

2. 不可变变量

   ```kotlin
   val <标识符> : <类型> = <初始化值>
   ```

   实例：
   ```kotlin
   val a: Int = 1  /* 注释与java相同*/
   val b = 1       // 系统自动推断变量类型为Int
   val c: Int      // 如果不在声明时初始化则必须提供变量类型
   c = 1           // 明确赋值
   
   
   var x = 5        // 系统自动推断变量类型为Int
   x += 1           // 变量可修改
   ```



### 函数定义

1. `fun`  关键字，参数格式为  参数名：类型，返回值在后方，例如：

   ```kotlin
   // public 方法则必须明确写出返回类型
   public fun sum(a: Int, b: Int): Int {   // Int 参数，返回值 Int
       return a + b
   }
   
   // 私有函数可让类型自动推断 简写为 
   
   fun sum(a:int , b:Int) = a + b;
   ```

2.  无返回类型 Unit （类似Java 中的void），且可省略，不区分public

   ```kotlin
   fun printSum(a: Int, b: Int): Unit { 
       print(a + b)
   }
   
   //==>
   fun printSum(a:Int, b:Int) {
       print(a + b)
   }
   ```

3.  `vararg` 关键字 可变参数函数

   ```kotlin
   // 传递多个Int 参数 
   fun vars(vararg v:Int){
       for(vt in v){
           print(vt)
       }
   }
   
   // 测试
   fun main(args: Array<String>) {
       vars(1,2,3,4,5)  // 输出12345
   }
   ```

4. 匿名函数  lambda表达式

   ```kotlin
   // 测试
   fun main(args: Array<String>) {
       // 定义函数sumLambda   参数为Int, Int  返回和
       val sumLambda: (Int, Int) -> Int = {x,y -> x+y}
       println(sumLambda(1,2))  // 输出 3
   }
   ```

### 字符串

1. `$` 表示  变量名 或者   变量值

2. `$varName` 表示变量值

3. `${varName.fun()} `  表示变量方法返回值 

   ```kotlin
   var a = 1
   // 模板中的简单名称：
   val s1 = "a is $a" 
   
   a = 2
   // 模板中的任意表达式：
   val s2 = "${s1.replace("is", "was")}, but now is $a"
   ```





