
import asyncio
import time
from datetime import datetime
# 协程是运行在单线程当中的并发
# 协程相比线程的一大优势就是省去了多线程之间的切换开销

def consumer():
    r = ''
    while True:
        n = yield r
        print("what is n here", n)
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)

# consumer函数式一个generator, 把一个consumer传入produce后：
# 1. 首先调用c.send(None)启动生成器
# 2. 然后，一旦产生了东西，通过c.send(n)切换到consumer执行
# 3. consumer通过yield拿到消息，处理，又通过yield把结果传回
# 4. produce拿到consumer处理的结果，继续生产吓一跳消息
# 5. produce决定不生产了，通过c.close()关闭consumer，整个过程结束。
# 整个流程无锁，由一个线程执行，produce和consumer协作完成任务，所以称为“协程”，而非线程的抢占式多任务。

# 使用同步 sleep 方法的代码
async def custom_sleep():
    print('SLEEP', datetime.now())
    time.sleep(1)

async def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print('Task {}: Compute factorial({})'.format(name, i))
        await custom_sleep()
        f *= i
    print('Task {}: factorial({}) is {}\n'.format(name, number, f))


start = time.time()
loop = asyncio.get_event_loop()

tasks = [
    asyncio.ensure_future(factorial("A", 3)),
    asyncio.ensure_future(factorial("B", 4)),
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

end = time.time()
print("Total time: {}".format(end - start))

# 使用异步 Sleep  的代码：

import asyncio
import time
from datetime import datetime


async def custom_sleep():
    print('SLEEP {}\n'.format(datetime.now()))
    # 当使用异步模式的时候（每次调用  await asyncio.sleep(1) ），进程控制权会返回到主程序的消息循环里，
    # 并开始运行队列的其他任务（任务Ａ或者任务Ｂ）。
    await asyncio.sleep(1)

async def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print('Task {}: Compute factorial({})'.format(name, i))
        await custom_sleep()
        f *= i
    print('Task {}: factorial({}) is {}\n'.format(name, number, f))


start = time.time()
loop = asyncio.get_event_loop()

tasks = [
    asyncio.ensure_future(factorial("A", 3)),
    asyncio.ensure_future(factorial("B", 4)),
]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

end = time.time()
print("Total time: {}".format(end - start))