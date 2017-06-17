#-*- coding:utf-8 -*-

def consumer():
    status = True
    while True:
        n = yield status
        print("我拿到了{}!".format(n))
        if n == 3:
            status = False

def producer(consumer):
    n = 5
    while n > 0:
        # yield给主程序返回消费者的状态
        yield consumer.send(n)
        n -= 1

if __name__ == '__main__':
    c = consumer()  # 函数中存在yield语句，python将其当做generator，返回一个generator object
    c.send(None)    # 将consumer这个generator中的语句推进到第一个yield出现的地方。故，consumer中的stauts=True和while True被执行。
    p = producer(c) # 定义producer生成器，传入消费者生成器，以此来通信。
    for status in p:# 循环运行producer和获取它yield来回状态。
        if status == False:
            print("我只要3，4，5就ok")
            break
    print("程序结束")

# 现在我们要让生产者发送1，2，3，4，5给消费者，消费者接受数字，返回状态给生产者。
# 当数字等于3时，会返回一个错误的状态。

# 现在程序进入producer里面，我们直接看yield consumer.send(n)，生产者调用了消费者的send方法
# 把n发送到consumer（即c），在consumer中的n=yield status，n拿到的是生产者发送的数字，同时，
# consumer用yield的方式把状态（status）返回给生产者。注意，此刻producer的consumer.send()
# 调用返回的就是consumer中的yield的status。生产者马上将status返回给调度它的主程序，主程序
# 判断对错。

# generator.send(n)的作用：把n发送fenerator(生成器）中的yield的赋值语句中，同时返回generator中的yield的变量。
# send() 方法必须在生成器运行后并挂起才能使用，也就是 yield 至少被执行一次。

# generator总是生成值，一般是迭代的序列
# coroutine关注的是消耗值，是数据(data)的消费者
# coroutine不会与迭代操作关联，而generator会
# coroutine强调协同控制程序流，generator强调保存状态和产生数据

# 相似的是，它们都是不用return来实现重复调用的函数/对象，都用到了yield(中断/恢复)的方式来实现。