# Spider Learning
Chatting on web spiders...

## 爬虫的基本知识
爬虫是通过向网站服务器发送请求来获取响应，并通过解析响应来获取所需信息的工具。

## 爬虫基本技术入门
首先，根据笔者的习惯，推荐各位使用`Python`作为编写爬虫的语言，因为`Python`的库环境丰富，安装方便简单，对新手较为友好。
请各位使用`Windows`系统的同学们选择以下两种方式中的一种来进行实验环境的搭配。
### Bash on Windows
请各位同学去`Windows`的软件商城搜索`Ubuntu`并下载，来建立`Windows`上的`Linux`环境

随后启动`Ubuntu`，在命令行中顺次输入以下内容：
```
sudo apt update
sudo apt upgrade
sudo apt install python3 python3-pip
pip3 install requests beautifulsoup4
```
以上命令将完成`Linux`环境下的`Python3`爬虫环境配置。
### Pycharm
请各位同学去百度搜索`Pycharm`并去官方网站下载该程序

依次点选`File`->`New`->`Python File`，建立一个新的`Python`脚本

依次点选`File`->`Settings...`->`Project: ***.py`->`Project Interpreter`

于右边`Project Interpreter`下拉菜单中选择`Python 3.6`，如果没有`Python 3.6`，请选择`Show All...`，在弹出选项卡右边点击`+`，在新的选项卡中找到解释器的路径，并添加。（可能有些同学并没有`Python 3.6`环境，请在网上搜索“在`Windows`中安装`Python 3.6`环境”的方法）

于`Settings`一级菜单中选择新添加的解释器环境，之后点击右边的`+`

在最上方的搜索栏中搜索：`requests`和`beautifulsoup4`，并点击左下角的按钮安装环境包

一路`确定`返回编辑器界面，此时点击右上角的`|>`按钮即可用解释器环境去运行脚本

## 爬虫的要点讲解
### 首先观察网站结构

在`Chrome`浏览器中按`F12`按钮调出`开发者视图`

在要提取的信息上点击鼠标右键，选择`检查`

这将会在`开发者视图`中选中所选取的元素，这就是我们要提取的对象

### 通过`requests`库来获取请求
```
r = requests.get('url', headers=your_headers)
```
其中`headers`需要进行设置，否则请求很大概率会被对方后端拒绝

在`开发者视图`的`Networks`选项卡中任意点选一个`GET`请求

将`Request Header`中的`User-Agent`，`Referer`和`Cookie`copy下来

放进`headers`字典中，即完成了`headers`的配置

### 通过`BeautifulSoup`来解析`Response`

值得赞美的`BeautifulSoup`支持多种`parser`，不过对于像豆瓣网这样成型，规范的网站，基础的`parser`就已经够用

将`Response`放入`BeautifulSoup`中进行解析
```
soup = BeautifulSoup(r.text)
```
这样就得到了整个网站的全部结构，之后对具体想要了解的对象进行解析即可。

## 后注
本代码仓库将开源笔者编写的爬虫程序，供大家参考。
