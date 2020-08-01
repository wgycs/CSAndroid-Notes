

## 问题描述：

HashMap 为什么要以2^n 作为，`(2^n - 1) & hash`  可以在保证下标不溢出的情况下 ，尽量使得散列函数在哈希桶中均匀分布。





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





### 参考资料

https://www.cnblogs.com/Young111/p/11519952.html?utm_source=gold_browser_extension

https://blog.csdn.net/qq_40574571/article/details/97612100