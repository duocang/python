from contextlib import contextmanager, closing
from urllib.request import urlopen

# 实现上下文管理是通过__enter__和__exit__这两个方法实现的
class Query(object):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print('Begin')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print('Error')
        else:
            print('End')

    def query(self):
        print('Query info about %s...' % self.name)

with Query('Bob') as q:
    q.query()


class Query(object):
    def __init__(self, name):
        self.name = name

    def query(self):
        print('Query info about %s...', self.name)

@contextmanager
def create_query(name):
    print('Begin')
    q = Query(name)
    yield q
    print('End')
# @contextmanager这个decorator接受一个generator，
# 用yield语句把with ... as var把变量输出出去
with create_query('Bob') as q:
    q.query()

# 我们希望在某段代码执行前后自动执行特定代码
@contextmanager
def tag(name):
    print("<%s>" % name)
    yield
    print("</%s>" % name)

with tag("h1"):
    print("heloo")
    print("wrold!")

# 1. with语句首先执行yield之前的语句，因此打印出<h1>；
# 2. yield调用会执行with语句内部的所有语句，因此打印出hello和world；
# 3. 最后执行yield之后的语句，打印出</h1>。

with closing(urlopen('https://www.python.org')) as page:
    for line in page:
        print(line)