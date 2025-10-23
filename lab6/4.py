import time
import math

num = int(input())
ms = int(input())

time.sleep(ms / 1000)
print("Square root of", num, "after", ms, "miliseconds is", math.sqrt(num))
