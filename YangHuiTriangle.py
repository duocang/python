def triangles():
	yield [1]
	b = [1, 1]
	yield b
	c = [1,1]
	i = 3
	while True:
		for j in range(i-2):
			c.insert(j+1, b[j]+b[j+1])
		b = c
		yield c
		c= [1, 1]
		i = i + 1

		

o = triangles()
for i in range(15):
	print(next(o))

# 先构造一个从3开始的奇数序列
# 这是一个生成器，并且是一个无现序列
def _odd_iter():
	n = 1
	while True:
		n = n + 2
		yield n

# 定义一个筛选函数
def _not_divisible(n):
	return lambda x: x % n > 0

# 定义一个生成器，不断返回一个素数
def primes():
	yield 2
	it = _odd_iter()    # 初始序列
	while True:
		n = next(it)    # 返回序列的第一个数
		yield n
		it = filter(_not_divisible(n), it)
# 打印1000以内的素数:
for n in primes():
    if n < 1000:
        print(n)
    else:
        break

def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

f1, f2, f3 = count()