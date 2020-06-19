## Ashmem（Anonymous Shared Memory）

Android 特有的内存共享机制，可以将指定的物理内存分别映射到各个进程自己的虚拟地址空间中，从而方便的实现进程间内存共享。

和Android Memory Killer 机制相似，实现由一个驱动完成（kernel/drivers/staging/android/ashmem.c）.



同样的逻辑我们看下驱动的注册也就是Load的时候会调用的：

```c
module_init(ashmem_init);
module_exit(ashmem_exit);

static int __init ashmem_init(void) {
    // 注册杂项设备驱动， 会在dev生成对应的文件节点 "dev/ashmem/"
	ret = misc_register(&ashmem_misc);
    // 通过register_shrinker注册到系统的shrinker_list中，这样在kswapd或者try_to_free_pages就有可能调到ashmem_shrinker
    // 和 Low Memory Killer 相似
    register_shrinker(&ashmem_shrinker);
}

```

### 1 . 内存的映射
内存哪里来？
怎么实现进程间通信的？
ashmem扮演什么角色？

注册杂项设备的时候，注册了这么一个处理对象。定义了驱动名称、设备号以及 一个处理函数指针结构体ashmem_fops；

```c
static struct miscdevice ashmem_misc = {
	.minor = MISC_DYNAMIC_MINOR,
	.name = "ashmem",
	.fops = &ashmem_fops,
};
//fops  --->  ashmem_fops

static const struct file_operations ashmem_fops = {
	.owner = THIS_MODULE,
	.open = ashmem_open,
	.release = ashmem_release,
	.read = ashmem_read,
	.llseek = ashmem_llseek,
	.mmap = ashmem_mmap,
	.unlocked_ioctl = ashmem_ioctl,
#ifdef CONFIG_COMPAT
	.compat_ioctl = compat_ashmem_ioctl,
#endif
};
```

其中包括了`open`、`release`基本操作，还包括了读取`mmap`以及`ioctl`操作。



### 2. 内存的释放
```c
//用于扫描释放需要释放的对象
//  使用LRU算法管理内存， 释放不使用的内存， 直到释放到nr_to_scan为空
static unsigned long
ashmem_shrink_scan(struct shrinker *shrink, struct shrink_control *sc)
{
	struct ashmem_range *range, *next;
	unsigned long freed = 0;

	/* We might recurse into filesystem code, so bail out if necessary */
	if (!(sc->gfp_mask & __GFP_FS))
		return SHRINK_STOP;

	if (!mutex_trylock(&ashmem_mutex))
		return -1;
	// 这里使用了LRU算法
	list_for_each_entry_safe(range, next, &ashmem_lru_list, lru) {
		loff_t start = range->pgstart * PAGE_SIZE;
		loff_t end = (range->pgend + 1) * PAGE_SIZE;

		range->asma->file->f_op->fallocate(range->asma->file,
				FALLOC_FL_PUNCH_HOLE | FALLOC_FL_KEEP_SIZE,
				start, end - start);
		range->purged = ASHMEM_WAS_PURGED;
		lru_del(range);
		// 释放
		freed += range_size(range);
		if (--sc->nr_to_scan <= 0)
			break;
	}
	mutex_unlock(&ashmem_mutex);
	return freed;
}
```


###  3. 应用实例 MemoryFile
