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


