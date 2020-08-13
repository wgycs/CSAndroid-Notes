# Visual VM 


### Visual VM安装
Visual VM 工具在JDK目录中可以找到，如`jdk1.8.0_65\bin`目录下。


### Visual VM插件安装


### 插件安装报错

`无法连接到visualVM插件中心2，因为https://visualvm.github.io../updates.xml.gz`

在visualVM 工具->插件选项中，点击可用插件，检查最新版本时，出现无法连接到visualVM插件中心2，因为https://visualvm.github.io../updates.xml.gz 

#### 解决步骤：
1.打开网址：https://visualvm.github.io/pluginscenters.html
2.在右侧选择JDK版本
3.选择之后会打开相应的插件中心，复制CatalogURL
4.打开visualVM，工具->插件->设置，然后把刚才的网址粘贴进去。







### 参考资料：
https://www.cnblogs.com/baby123/p/11551626.html