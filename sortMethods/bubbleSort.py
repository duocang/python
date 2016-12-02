def bubble(list):
	for i in range(len(list)):
		for j in range( len(list)-1-i):
			if list[j] > list[j+1]:
				list[j], list[j+1] = list[j+1], list[j]
#if name == 'main':
list1 = [2,3,4,32,1,34,5,10]
bubble(list1)
print(list1)