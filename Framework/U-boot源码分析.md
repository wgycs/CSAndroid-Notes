>Bootloader 完成了Linux系统启动前的硬件初始化，并将跳到C执行入口，进行firmware的初始化部分。这里主要分析汇编部分。

<!--more-->


U-boot 启动过程属于多阶段类型。第一阶段完成CPU体系结构初始化，通常由汇编完成。第二阶段实现较为复杂的功能如实现初始化硬件、内存映射、TFTP传输，串口调试，内核参数传递等，通常由C语言实现。
### 1. 第一阶段代码分析
第一阶段的源文件包括CPU初始化相关以及开发板初始化相关分别对应/cpu/arm920t/start.S和board/\*\*\*/lowlevel_init.S文件。
#### 1.1. 硬件初始化
完成对CPU正常工作所必须初始化工作，如时钟、工作模式、MMU等。

```C
reset:
	/*
	 * 设置CPU 工作在超级保护模式（SVC32）
	 */
     mrs r0,cpsr
　　	bic	r0,r0,#0x1f
　　	orr	r0,r0,#0xd3
　　	msr	cpsr,r0
　　	ldr     r0, =pWTCON /*关闭看门狗*/
　　	mov     r1, #0x0
  	 str     r1, [r0]
   .....
bl	cpu_init_crit /*跳转到该标签设置CPU寄存器MMU Cache等*/
```

#### 1.2 初始化SDRAM控制器
准备Bootloader第二阶段代码RAM空间。

```C
lowlevel_init:
    ldr     r0, =SMRDATA /*13个寄存器值存放地址*/
    ldr	r1, _TEXT_BASE
    sub	r0, r0, r1      /*地址变换*/
    ldr	r1, =BWSCON	/* Bus Width Status Controller */
    add     r2, r0, #13*4   /*SMRDATA 末尾地址*/
    0:                          /*循环读取设置*/
    ldr     r3, [r0], #4
    str     r3, [r1], #4
    cmp     r2, r0
    bne     0b

　　	/* everything is fine now */
    mov	pc, lr
    .ltorg
　　/* the literal pools origin */
SMRDATA:
　　 .word ....

```

#### 1.3 设置堆栈
```C
stack_setup:
    ldr	r0, _TEXT_BASE	/*代码段地址之前作为堆栈 */
    sub	r0, r0, #CFG_MALLOC_LEN/*留给 malloc 动态分配*/
    sub	r0, r0, #CFG_GBL_DATA_SIZE /*存放全局变量 */

#ifdef CONFIG_USE_IRQ
    sub	r0, r0, #(CONFIG_STACKSIZE_IRQ+CONFIG_STACKSIZE_FIQ)
  	/*IRQ和FIQ申请堆栈*/
#endif
    sub	sp, r0, #12		/* 留下12字节的abord异常空间*/
```


#### 1.4复制Bootloader第二阶段程序到RAM空间
```C
relocate:				/* 将U-boot复制到RAM空间*/
    adr	r0, _start		/* 当前代码地址作为源地址给r0 */
    ldr	r1, _TEXT_BASE/*代码段链接地址作为目标地址给r1 */
    cmp     r0, r1         /* don't reloc during debug */
    beq     clear_bss    /*测试是否在RAM中调试，否则继续复制*/
    ldr	r2, _armboot_start /*启动地址*/
    ldr	r3, _bss_start  /*BSS段起始地址 即 代码段结束地址*/
    sub	r2, r3, r2		/* 代码段大小给 r2*/
    bl  CopyCode2Ram	/*Nand启动时(位于bord/boot_init.c )
                           跳转复制函数 r0: source, r1: dest, r2: size*/
    add	r2, r0, r2	/* r2 <- source end address*/
copy_loop: /*Nor flash 启动循环复制*/
    ldmia	r0!, {r3-r10}/*copy from source address[r0] */
    stmia	r1!, {r3-r10}  /* copy to target address [r1]  */
    cmp	r0, r2		/*until source end addreee [r2]  */
ble	copy_loop
```

#### 1.5 跳转到C入口

跳转之前清除堆栈空间，然后PC指针跳转到/lib_arm/board.c中的start_armboot( )函数开始执行bootloader的第二阶段代码。
```C
ldr	pc, _start_armboot
_start_armboot:	.word start_armboot
```


### 2.第二阶段代码分析
Bootloader第二阶段完成工作从lib_arm/board.c中的start_armboot( )函数开始执行，也即是第一阶段跳转到的地址。从这部分开始下面全是由C编写完成，分析起来较为容易，不做过多介绍，依次完成的主要工作：

- size = flash_init ();
- nand_init();		/*  go init the NAND  */
- env_relocate (); /*  initialize environment  */
- devices_init ();	/* get the devices list going. */
- jumptable_init (); /*  初始化跳转列表  */
- console_init_r ();	/*   fully init console as a device   */
- enable_interrupts ();/*  中断使能  */
- board_late_init ();
- eth_initialize(gd->bd);/*  初始化网口  */
- 在main_loop ()中死循环，等待用户交互。

```C
for (;;)
{
  main_loop ();
}
```