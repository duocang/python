from random import random
from time import clock
from matplotlib import pyplot as plt
import numpy as np
# 首先构造一个正方形和一个1/4单位圆
# 在边长为1的正方形方框内随机抛点，统计落在圆弧内的点所在比例。随着点的数量增加，
# 这个比例会愈发接近四分之一圆的面积与正方形面积之比，即pi/4
# 使用python的random库产生随机数

plt.figure(figsize=(9,9))
X = np.linspace(-1, 1, 256,endpoint=True)
C = np.sqrt(1-X**2)
plt.plot(X, C, color="b", linewidth=6, linestyle=":", label="e^(-(2x)^2)")
ax = plt.gca()
ax.fill(X,C,color='#EFB582' , alpha=0.25)
n=2**5
hist=0
clock()
for i in range(1,n):
    x,y=random(),random()
    dist=np.sqrt(x**2+y**2)
    plt.scatter(x,y, s=45, alpha=.4, marker='o')
    if dist<=1.0:
        hist=hist+1
pi=4*(hist/n)
print('pi is %s'%pi)
print('elaspe is %ss'%clock())


plt.xticks(fontsize=20)
plt.yticks(fontsize=20)


plt.xlim(0,1.0)
plt.ylim(0,1.0)

plt.show()