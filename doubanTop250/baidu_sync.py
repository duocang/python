import socket
from time import time
from selectors import DefaultSelector, EVENT_WRITE

def sync_way():
    for i in range(10):
        sock = socket.socket()
        sock.connect(('www.baidu.com', 80))
        print('connected')
        request = 'GET {} HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n'.format('/s?wd={}'.format(i))
        sock.send(request.encode('ascii'))
        response = b''
        chunk = sock.recv(4096)
        while chunk:
            response += chunk
            chunk = sock.recv(4096)
        print('done!!')



def main():
    start = time()
    sync_way()
    end = time()
    print('Cost {} seconds'.format(end - start))


if __name__ == "__main__":
    main()


# 1.socket连接的建立需要等待，一旦握手建立的时间漫长，就会影响下面的流程正常运行。
# 2.socket接收数据的过程是阻塞式的，等待buffer的过程也是需要一段时间的。
# 3.socket的建立连接-接收过程都是一个一个来的，在没完成一个连接时不能进行其他连接的处理。

# 解决1：不一致等待socket的状态改变，而是让其告知改变。可以使用io复用
#       O复用：预先告知内核，使内核一旦发现进程指定的一个或多个IO条件就绪（输入准备被读取，或描述符能承接更多的输出），它就通知进程。
#       阻塞IO模型： recvfrom->无数据报准备好->等待数据->数据报准备好->数据从内核复制到用户空间->复制完成->返回成功指示
#       IO复用模型： select->无数据报准备好->据报准备好->返回可读条件->recvfrom->数据从内核复制到用户空间->复制完成->返回成功指示
selector = DefaultSelector()

sock = socket.socket()
sock.setblocking(False)
try:
    sock.connect(('www.baidu.com', 80))
except BlockingIOError:
    pass

def connected():
    selector.unregister(sock.fileno())
    print('connected!')


selector.register(sock.fileno(), EVENT_WRITE, connected)


