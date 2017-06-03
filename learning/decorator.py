import logging
# 装饰器
# https://foofish.net/python-decorator.html
# 本质上，decorator就是一一个返回函数的高阶函数。
def use_logging(func):

    def wrapper():
        logging.warning("%s is running" % func.__name__)
        return func()   #把 foo 当做参数传递进来时，执行func()就相当于执行foo()
    return wrapper

def foo():
    print('i am foo')

foo = use_logging(foo)  #因为装饰器 use_logging(foo) 返回的时函数对象 wrapper，这条语句相当于  foo = wrapper
foo()                   # 执行foo()就相当于执行 wrapper()

# 语法糖
def use_logging(func):

    def wrapper():
        logging.warning("%s is running" % func.__name__)
        return func()
    return wrapper

@use_logging
def foo():
    print("i am foo")

foo()

# *args, **kwargs
# 如果我foo需要参数怎么办？
def foo(name):
	print("i am %s" % name)

def use_logging(func):
	# 我们可以在定义wrapper函数的时候指定参数
    def wrapper(name):
		logging.warning("%s is running" % func.__name__)
		return func(name)
    return wrapper

# 若装饰器不知道foo有多少个参数时，我们可以使用*args来代替
def use_logging(func):
    def wrapper(*args, **kwargs):         # 还支持关键字参数
		logging.warning("%s is running" % func.__name__)
		return func(*args, **kwargs)
    return wrapper
# 带不定个数参数和关键字参数的foo函数
def foo(name, age=None, height=None):
    print("I am %s, age %s, height %s" % (name, age, height))
import logging


# 带参数的装饰器
def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warning("%s is running" % func.__name__)
            elif level == "info":
                logging.info("%s is running" % func.__name__)
            return func(*args)
        return wrapper

    return decorator

@use_logging(level="warn")
def foo(name='foo'):
    print("i am %s" % name)

foo()

# 类装饰器
# 使用类装饰器主要依靠类的__call__方法，当使用@形式将装饰器附加到函数上时，会调用此方法。
class Foo(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        print ('class decorator runing')
        self._func()
        print ('class decorator ending')

@Foo
def bar():
    print ('bar')

bar()

# 装饰器的顺序
#@a
#@b
#@c
#def f ():
#    pass
#它的执行顺序是从里到外，最先调用最里层的装饰器，最后调用最外层的装饰器，它等效于
#f = a(b(c(f)))

# 装饰器
def logged(func):
    def with_logging(*args, **kwargs):
        print (func.__name__ )     # 输出 'with_logging'
        print (func.__doc__  )     # 输出 None
        return func(*args, **kwargs)
    return with_logging

# 函数
@logged
def f(x):
   """does some math"""
   print(x + x * x)
#不难发现，函数 f 被with_logging取代了，当然它的docstring，__name__就
# 是变成了with_logging函数的信息了。好在我们有functools.wraps，wraps
# 本身也是一个装饰器，它能把原函数的元信息拷贝到装饰器里面的 func 函数中，这
# 使得装饰器里面的 func 函数也有和原函数 foo 一样的元信息了。
f(12)

logged(f)   #Out[26]: <function __main__.logged.<locals>.with_logging>


from functools import wraps
def logged(func):
	#wraps本身也是一个装饰器，它能把原函数的元信息拷贝到装饰器里面的
	# func 函数中，这使得装饰器里面的 func 函数也有和原函数 foo 一样的元信息了
    @wraps(func)
    def with_logging(*args, **kwargs):
        print (func.__name__  )    # 输出 'f'
        print (func.__doc__   )    # 输出 'does some math'
        return func(*args, **kwargs)
    return with_logging

@logged
def f(x):
   """does some math"""
   return x + x * x
f(2)
logged(f)   # Out[29]: <function __main__.f>
