开发awwsom主要用到的那些库：

- jinja2 前端模版引擎。所有的前端页面都是通过jinja2调用模版并渲染得到的。
	- jinja2是一个现代的，设计者友好的python模版语言
- aiohhttp 基于asyncio的异步http框架。此处主要用于实现web服务器，提供单线程多用户高并发支持
- aiomysql mysql的python异步驱动
- asyncio python内置的异步io库。几乎所有的异步io操作都与之有关

如上所示, awesome为了实现对事务的高效处理, 使用了许多异步框架与提供异步IO能力的库. 如果忘了什么是异步IO, 可翻看廖老师之前的教程. 简而言之, 就是当程序需要执行耗时的IO操作时, 只发出IO命令, 并不等待IO结果, 让CPU执行其他任务. 当IO结束时, 再通知CPU处理.
