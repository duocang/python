# -*- coding: utf-8 -*-

import os
from os.path import isfile, join
import re

myPath = '/Users/song/OneDrive/java/尚学堂/尚学堂高淇java300集(181-200)'


# onlyfiles = [ f for f in listdir(myPath) if isfile(join(myPath,f)) ]


for file in os.listdir(myPath):
    newFile = re.sub('_服务器', "", file)
    newFile = re.sub('【', "", newFile)
    newFile = re.sub('】', "", newFile)
    newFile = re.sub('手写', "", newFile)
    os.rename(os.path.join(myPath, file), os.path.join(myPath, newFile))
    print(file)
    print(newFile)