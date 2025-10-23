import os

path = '.'

dirs = [d for d in os.listdir(path) if os.path.isdir(d)]
files = [f for f in os.listdir(path) if os.path.isfile(f)]

print("Directories:", dirs)
print("Files:", files)
print("All:", os.listdir(path))

