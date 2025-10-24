import os
path = '.'
dirs = []
files = []

for item in os.listdir(path):
    if os.path.isdir(item):
        dirs.append(item)
    else:
        files.append(item)

print(dirs)
print(files)
print(os.listdir(path))
