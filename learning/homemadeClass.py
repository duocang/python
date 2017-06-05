class Student(object):
	def __init__(self, name):
	    self.name = name

# Implement __repr__ for any class you implement. This should be second nature.
# Implement __str__ if you think it would be useful to have a string version
# which errs on the side of more readability in favor of more ambiguity.

	def __str__(self):  # goal is to be readable
		return 'Student object (name: %s)' % self.name

	def __repr__(self): # goal is to be unambiguous
		return 'Student object (name: %s)' % self.name
s = Student('Michael')
s

class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100000: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值

    def __getitem__(self, n):
	    if isinstance(n, int):  # n是索引
		    a, b = 1, 1
		    for x in range(n):
			    a, b = b, a + b
		    return a
	    if isinstance(n, slice):  # n是切片
		    start = n.start
		    stop = n.stop
		    if start is None:
			    start = 0
		    a, b = 1, 1
		    L = []
		    for x in range(stop):
			    if x >= start:
				    L.append(a)
			    a, b = b, a + b
		    return L

f = Fib()
for n in f:
	print(n)
f[0]
f[0:5]

class Chain(object):

    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__

Chain().status.user.timeline.list

class Chain(object):
    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        if path == 'users':
	        # Chain().users返回的是一个函数,函数参数是一个str,函数本身又可以返回一个Chain对象。
	        # 其他调用Chain属性情况均返回一个Chain对象
            return lambda name: Chain('%s/%s' % (self._path, name))
        else:
            return Chain('%s/%s'%(self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__

print(Chain().users('wang'))

# 上面那个代码不够健壮，如果遇到
# Chain().users('michael').group('student').repos
# 就无法处理，需要在getattr函数中添加逻辑代码。
class Chain(object):

    def __init__(self, path='GET '):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

	# 对实例进行直接调用就好比对一个函数进行调用一样，
    # 所以你完全可以把对象看成函数，把函数看成对象，
    # 因为这两者之间本来就没啥根本的区别。
    def __call__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__

print(Chain().users('wang').name('xuesong'))

class Student(object):
    def __init__(self, name):
	    self.name = name
    def __call__(self):
	    print('My name is %s.' % self.name)
s = Student('Michael')
s() # self参数不要传入
# My name is Michael.
