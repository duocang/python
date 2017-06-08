import os
from multiprocessing import Process

print('Process (%s) start...' % os.getpid())

# 子进程永远返回0，而父进程返回子进程的ID
# fork()调用一次，返回两次
pid = os.fork()
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid())) # 子进程只需要调用getppid()就可以拿到父进程的ID
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))

import os
from multiprocessing import Process

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))
# Process类来代表一个进程对象
# 只需要传入一个执行函数和函数的参数，创建一个Process实例，用start()方法启动
if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()    # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步
    print('Child process end.')

# 如果要启动大量的子进程，可以用进程池的方式批量创建子进程
from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(5)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close() # 调用join()之前必须先调用close()
    p.join() # 对Pool对象调用join()方法会等待所有子进程执行完毕
    print('All subprocesses done.')

# subprocess模块可以让我们非常方便地启动一个子进程，然后控制其输入和输出
    import subprocess

    print('$ nslookup www.python.org')
    r = subprocess.call(['nslookup', 'www.python.org'])
    print('Exit code:', r)

# 以Queue为例，在父进程中创建两个子进程，一个往Queue里写数据，一个从Queue里读数据
from multiprocessing import Process, Queue
import os, time, random
# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

if __name__ == '__main__':
    # 父进程创建Queue，并传给各个子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入
    pw.start()
    # 启动子线程pr，读取
    pr.start()
    # 等待pw结束
    pw.join()
    # pr进程里是死循环，无法等待期结束，只能强制终止
    pr.terminate()