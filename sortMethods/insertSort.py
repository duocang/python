# insert the number into suitable place of a sorted list, until finish all
def insertSort(list):
	if list != None:
		if len(list) == 1:
			pass
		else:
			for i in range(1,len(list)):#start with second item.
				temp = list[i]
				for j in range(i):
					if list[j] > list[i]:
						for k in range(i, j,-1):
							list[k] = list[k-1]
						list[j] = temp
#if name == 'main':
list1 = [2,3,4,32,1,34,5,10]
insertSort(list1)
print(list1)