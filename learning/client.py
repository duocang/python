
# !/usr/bin/env python3
# coding=utf-8
from multiprocessing.managers import BaseManager

class commBase(BaseManager):
    pass

# 接收端只需要注册两个与调度端相同的网络接口函数名称即可
commBase.register("send_msg")
commBase.register("receive_msg")

# 调度端IP（如果想使用同一台计算机测试，可以改成127.0.0.0，这样就是自己发自己接）
ip_address = "127.0.0.1"

# 调度端IP，端口，验证码
commMgr = commBase(address=(ip_address, 20081), authkey=b"wangxuesong")
try:
    # 连接
    commMgr.connect()

    # 实例化接口函数
    send = commMgr.send_msg()
    receive = commMgr.receive_msg()

    # 从调度端send_msg()接口get消息，然后将结果返回给调度端的receive_msg() 接口
    for x in range(5):
        print("开始从'%s'读取消息..." % ip_address)
        n = send.get(True)
        print("开始计算:%d*%d" % (n, n))
        r = "%d*%d=%d" % (n, n, n * n)
        receive.put(r)
except Exception:
    print("连接失败。")
else:
    print("计算完成...")
