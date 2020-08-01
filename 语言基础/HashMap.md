

## 问题描述：

1. HashMap 为什么要以2^n 作为桶长度？
2. Hash算法是怎么样的？
3. HashMap线程不安全的原因？



## HashMap 为什么要以2^n 作为桶长度？

`(2^n - 1) & hash`  可以在保证下标不溢出的情况下 ，尽量使得散列函数在哈希桶中均匀分布。



```java
 public V put(K key, V value) {
        return putVal(hash(key), key, value, false, true);
    }


final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
                   boolean evict) {

    Node<K,V>[] tab; Node<K,V> p; int n, i;
    if ((tab = table) == null || (n = tab.length) == 0)
   		n = (tab = resize()).length;
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null);
    ...
}
```



## Hash算法是怎么样的？

JDK 1.8 中，是通过 hashCode() 的高 16 位**异或**低 16 位实现的：`(h = k.hashCode()) ^ (h >>> 16)`，使用**异或**算法的原因是尽量保证所有位都能参与运算，进而减少Hash碰撞的产生。



## HashMap线程不安全的原因？

HashMap在多线程操作扩容的情况下，由于扩容算法的实现逻辑会导致，出现环形链。在get的时候会出现死循环空占CPU。

常用的解决思路：

1. Hashtable替换HashMap
2. Collections.synchronizedMap将HashMap包装起来
3. ConcurrentHashMap替换HashMap



## ConcurrentHashMap 比 HashTable 效率要高？



concurrentHashMap相比于HashTable 锁粒度更低。

HashTable 使用一把锁（锁住整个链表结构）处理并发问题，多个线程竞争一把锁，容易阻塞；

ConcurrentHashMap

- JDK 1.7 中使用分段锁（ReentrantLock + Segment + HashEntry），相当于把一个 HashMap 分成多个段，每段分配一把锁，这样支持多线程访问。锁粒度：基于 Segment，包含多个 HashEntry。
- JDK 1.8 中使用 CAS + synchronized + Node + 红黑树。锁粒度：Node（首结点）（实现 Map.Entry）。锁粒度降低了。



## 参考资料

https://www.cnblogs.com/Young111/p/11519952.html?utm_source=gold_browser_extension

https://blog.csdn.net/qq_40574571/article/details/97612100	

https://www.cnblogs.com/andy-zhou/p/5402984.html