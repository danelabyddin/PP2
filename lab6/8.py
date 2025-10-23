import os

p = input()

if os.path.exists(p):
    print("Path exists")
    print("Filename:", os.path.basename(p))
    print("Directory:", os.path.dirname(p))
else:
    print("Path does not exist")
