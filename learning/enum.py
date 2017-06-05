from enum import unique, Enum

import enum
import enum

@unique # 装饰器可以帮助我们检查保证没有重复值。
class WeekDay(Enum):
	Sun = 0  # Sun的value被设定为0
	Mon = 1
	Tue = 2
	Wed = 3
	Thu = 4
	Fri = 5
	Sat = 6

day1 = WeekDay.Mon
print(day1)