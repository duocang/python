import time,threading

# 新线程执行的代码
# 任何进程默认就会启动一个线程，称为主线程
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)

# 银行存款
balance = 0

def change_it(n):
    # 先存后取，结果应该为0
    global balance
    blance = balance + n
    balance = balance - n

def run_thread(n):

    for i in range(100000):
        change_it(n)

t1 = threading.Thread(target=run_thread, args = (5, ))
t2 = threading.Thread(target=run_thread, args = (8, ))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)

balance = 0
lock = threading.Lock()

def run_thread2(n):
    for i in range(100000):
        # 先要获取锁:
        lock.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()
t1 = threading.Thread(target=run_thread2, args = (5, ))
t2 = threading.Thread(target=run_thread2, args = (8, ))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)




exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, self.counter, 5)
        print ("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()
thread1.join()  # 主线程结束了，子线程还在运行。如果需要主线程等待子线程执行完毕再退出，可是使用线程的join方法
thread2.join()
print ("退出主线程")
# 1 join方法的作用是阻塞主进程（挡住，无法执行join以后的语句），专注执行多线程。
# 2 多线程多join的情况下，依次执行各线程的join方法，前头一个结束了才能执行后面一个。
# 3 无参数，则等待到该线程结束，才开始执行下一个线程的join。
# 4 设置参数后，则等待该线程这么长时间就不管它了（而该线程并没有结束）。不管的意思就是可以执行后面的主进程了
