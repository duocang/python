
# @proterty装饰器就是负责把一个方法变成属性调用
class Student(object):
	@property
	def score(self):
		return self._score # 一个下划线开头的变量外部可以访问，但是约定不要随意访问
	@score.setter   # @property 本身又创建了另一个装饰器，负责把一个setter方法变成属性。
	def score(self, value):
		if not isinstance(value, int):
			raise ValueError('score must be an integer!')
		if value < 0 or value > 100:
			raise ValueError('score must between 0 ~ 100!')
		self._score = value

# @property可以只定义读属性，不定义setter方法的写属性
class Student(object):
	@property   # 把一个getter方法变成属性，只需要加上@property就可以了
	def birth(self):
		return self._birth

	@birth.setter   # 另一个装饰器@score.setter，负责把一个setter方法变成属性赋值
	def birth(selfs, value):
		selfs.birth = value

	@property
	def age(self):
		return 2017 - self.birth
	# 上面的birth是可读写属性，而age就是一个只读属性