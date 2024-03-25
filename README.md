# Information_query_near_the_scenic_spot

## 基于 selenium 访问高德地图获取景点附近美食或酒店信息

### 需求

根据景点名称或地址查询周围美食或酒店信息。《个人练习使用，在其他环境使用可能存在意想不到的bug》

### 想法

使用景点名称或地址（经纬度）在高德地图上查找位置，再在查找出来的页面中的<em>“附近”</em>链接查找<em>“美食”</em>获取相关列表。

### 解决过程

高德地图查询附近列表后，显示的是<strong>动态网页</strong>，通过查询获得相关信息正确网页后，再次访问新网页，出现滑块验证码，所以使用selenium解决验证码问题，获取需要的数据。

---

## 版本

### 1.0.1
> 更新时间：2023.8.29

使用selenium自动化操作浏览器访问高德地图网页，查询相关信息。\
途中遇到滑块验证码拦截，通过selenium模拟人工操作通过验证码，同时，携带已登录高德地图的相关<em><strong>cookie</strong></em>信息，以跳过通过验证码之后需要登录高德地图的情况。

#### 存在问题

1. 现已完成数据获取，通过协程的方式获取到大量数据。但是数量太多，高德地图访问会被拒绝，疑似被服务器检测到爬虫行为，封了IP。
2. 使用selenium操作浏览器时，浏览器可视化界面会出现。若设置为<strong>无头模式</strong>，会被检测出爬虫行为，无法通过验证码。

### 1.0.2
> 更新时间: 2023.9.5

更新移动滑块功能的代码，使得移动效率提高。\
修改通过验证码后验证是否通过的代码，使得验证效率提高。

#### 已解决问题

> 1 高德网站针对于查询周围功能，貌似设置了数量限制，非个人可以解决。

#### 存在问题

1. 修改后的移动滑块时间变短，但是通过率降低。
2. 验证通过验证码部分，保证了程序多次尝试，但是并没有提高成功获取数据的成功率。
