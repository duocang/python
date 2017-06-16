import threading
import time

def job1():
    global A, lock
    lock.acquire()
    for i in range(10):
        A += 1
        print('job1', A)
    lock.release()

def job2():
    global A, lock
    lock.acquire()
    for i in range(10):
        A += 10
        print('job2', A)
    lock.release()

# 死锁
# 有锁就可以方便的处理线程同步问题，可是多线程的复杂度和难以调试的根源也来自于线程的锁。

mutex_a = threading.Lock()
mutex_b = threading.Lock()

class MyThread(threading.Thread):
    def task_a(self):
        if mutex_a.acquire():   # Acquire a lock, blocking or non-blocking.
            print('thread %s ges mutex a' %self.name)
            time.sleep(1)
            if mutex_b.acquire():
                print('thread %s gets mutex b' % self.name)
                mutex_b.release()
            mutex_a.release()

    def task_b(self):
        if mutex_b.acquire():
            print('thread %s ges mutex a' % self.name)
            time.sleep(1)
            if mutex_a.acquire():
                print('thread %s gets mutex b' % self.name)
                mutex_a.release()
            mutex_b.release()

    def run(self):
        self.task_a()
        self.task_b()

def main():
    print ("Start main threading")
    threads = [MyThread() for i in range(2)]
    for t in threads:
        t.start()
    print ("End Main threading")

# 线程需要执行两个任务，两个任务都需要获取锁，然而两个任务先得到锁后，
# 就需要等另外锁释放。

if __name__ == '__main__':
    lock = threading.Lock()
    A = 0
    t1 = threading.Thread(target=job1)
    t2 = threading.Thread(target=job2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("everyting ends")
    main()

