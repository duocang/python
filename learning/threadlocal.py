import threading

# 可以理解为全局变量local_school是一个dict，
# 不但可以用local_school.student，还可以绑定其他变量，
# 如local_school.teacher等等。
# 创建全局ThreadLocal对象
local_school = threading.local()


# 每个属性如local_school.student都是线程的局部变量，
# 可以任意读写而互不干扰，也不用管理锁的问题，ThreadLocal内部会处理
def process_student():
    # 获取当前线程关联的student
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()


t1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target=process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()

# ThreadLocal解决了参数在一个线程中各个函数之间互相传递的问题