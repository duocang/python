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
	    a, b = 1, 1
	    for x in range(n):
		    a, b = b, a + b
	    return a
f = Fib()
for n in f:
	print(n)
f[0]