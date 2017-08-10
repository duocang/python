# -*- coding: utf-8 -*-

import os
from os.path import isfile, join
import re

myPath = '/Users/song/OneDrive/尚学堂_高淇_java300集视频教程/尚学堂_高淇_java300集第三季（208-300）'


# onlyfiles = [ f for f in listdir(myPath) if isfile(join(myPath,f)) ]


for file in os.listdir(myPath):

    newFile = re.sub('_尚学堂_高淇_java300集最全视频教程_', "_", file)
    newFile = re.sub('【', "", newFile)
    newFile = re.sub('】', "", newFile)
    newFile = re.sub('手写', "", newFile)
    os.rename(os.path.join(myPath, file), os.path.join(myPath, newFile))
    print(file)