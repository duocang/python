# to understand what yield does, you must understand what generators are.
# And before generators come iterables.

#       Iterables
# when you carete a list, you can read its items one by one. Reading its items one by
# one is callled iteration.

mylist = [1, 2,3 ]
for i in mylist:
    print(i)
# mylist is an iterable. When you use a list comprehension, you create a list, and so an iterable:
mylist = [x*x for x in range(3)]
for i in mylist:
    print(i)

#       Generators
# generators are iterators, but you can only iterate over them once. It's because
# they do not store all the values in memory, they generate values on the fly:
# 不创建完整的list，而是不断推算后续元素
myGenerator = (x*x for x in range(3))
for i in myGenerator:
    print(i)
# It is just the same except you used () instead of []. BUT, you cannot perform
# for i in myGenerator a second time since generators can only  be used once:
# they calculate 0, then forget about it and calculate 1, and end calculdating
# 4, one by one.


#               yieled
# yield is a keyword that is used like return, except the function will return a generator
def createGenerator():
    myList = range(3)
    for i in myList:
        yield i*i
mygenerator = createGenerator() # create a generator
print(mygenerator) # mygenerator is an object!
for i in mygenerator:
    print(i)
# To master yield, you must understand that when you call the function, the code you have
# written in the functiojno body does not run. THe function only returns the generator
# object, this is a bit tricky:-)
#The first time the for calls the generator object created from your function,
#it will run the code in your function from the beginning until it hits yield,
# then it'll return the first value of the loop. Then, each other call will run
# the loop you have written in the function one more time, and return the next value,
# until there is no value to retu-rn.

#           魔法
# 当一个生成器函数调用yield时，生成器函数的状态会被冻结，所有的变量的值都会被保存下来，下一行要执行代码的位置也会被记录下来，
# 直到下一次调用next()。一旦next()再次被调用，生成器函数会从上一次离开的地方开始。如果永远不调用，yield保存的状态会被无视。
