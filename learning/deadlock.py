
import threading
import time# 死锁
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

    for t in threads:
        t.join()
    print ("End Main threading")

# 线程需要执行两个任务，两个任务都需要获取锁，然而两个任务先得到锁后，
# 就需要等另外锁释放。
if __name__ == '__main__':
    main()