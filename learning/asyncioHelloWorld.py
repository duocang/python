import asyncio

@asyncio.coroutine      # 把generator标记为coroutine类型，再把coroutine扔进EventLoop中执行
def hello():
    print("Hello World!")
    # 异步调用asyncio.sleep(1)
    r = yield from asyncio.sleep(1)
    print("Hello again!")

# 获取EventLoop
loop = asyncio.get_event_loop()
# 执行coroutine
loop.run_until_complete(hello())
loop.close()

# hello()会首先打印出hello world!，然后，yield from语法可以让我们方便地调用另一个generator。
# 由于asyncio.sleep()也是一个coroutine，所以线程不会等待asyncio.sleep()，而是直接中断
# 并执行下一个消息循环。


