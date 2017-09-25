# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import json

a = np.linspace(0, 2 * np.pi, 50)
b = np.sin(a)
print a
print b

plt.plot(a, b)
mask = b >= 0
plt.plot(a[mask], b[mask], "bo")
mask = (b >= 0) & (a <= np.pi /2)
plt.plot(a[mask], b[mask], "go",)
plt.show()

x = np.linspace(0, 2 * np.pi, 50)
plt.subplot(2, 1, 1)
plt.plot(x, np.sin(x), 'r')
plt.subplot(2, 1, 2)
plt.plot(x, np.cos(x), 'g')
plt.show()

x = np.random.rand(1000)
y = np.random.rand(1000)
size = np.random.rand(1000) * 50
colour = np.random.rand(1000)
plt.scatter(x,y,size, colour)
plt.colorbar()

plt.show()

x = np.random.rand(1000)
plt.hist(x,50)
plt.show()

path = "/Users/xuesong/OneDrive/pydata/ch02/usagov_bitly_data2012-03-16-1331923249.txt"
open(path).readline()
