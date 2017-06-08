import time, threading

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