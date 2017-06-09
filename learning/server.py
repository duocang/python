# 导入managers子模块中的BaseManager类，这个类封装了一些常用的网络传输和接口方法

from multiprocessing.managers import BaseManager
import queue,time,random

# 初始化两个queue消息列队，一个用于传输，一个用于接收
sendMsg = queue.Queue()
receiveMsg = queue.Queue()

# 新建一个类，继承BaseManager的所有方法和属性
class commBase(BaseManager):
    pass

# 使用BaseManager类的register方法，生成两个接口函数，
# 名为"send_msg"和"receive_msg"，使用callable参数，
# 将这两个接口函数关联到不同的queue对象上（相当于定义了两个返回queue的网络接口函数）
commBase.register("send_msg", callable=lambda: sendMsg)
commBase.register("receive_msg", callable=lambda: receiveMsg)

# 监听本地的20086端口，验证码为"wangxuesong"
# (在接收端需要配置相同的验证码才能连接到这台机器的20086端口)
commMgr = commBase(address=("127.0.0.1", 20081), authkey=b"wangxuesong")

#启动网络监听（此时会在系统中发现127.0.0.1:20086端口处于监听状态）
commMgr.start()

# 获得上面创建的接口函数对象（queue对象）
send = commMgr.send_msg()
receive = commMgr.receive_msg()


# 随机生成5个1~1000以内的数字，将它们放到进程中的queue网络接口消息列队中
for x in range(5):
    n=random.randint(1,1000)
    print("将整数'%s'放入待发送的消息列队..."%n)
    send.put(n)

# 之后这个程序将被阻塞，在20086端口上等待消息的返回
print("等待计算结果返回...")
for x in range(5):
    r=receive.get(True)
    print(r)

#关闭接口，释放资源
commMgr.shutdown()
print("End")


# Queue之所以能通过网络访问，就是通过QueueManager实现的
# 由于QueueManager管理的不止一个Queue，所以，要给每个
# Queue的网络调用接口起个名字，比如get_task_queue

