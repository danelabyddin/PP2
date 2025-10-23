import os

path = input()

if os.path.exists(path):
    if os.access(path, os.W_OK):
        os.remove(path)
        print("File deleted")
    else:
        print("No permission to delete this file")
else:
    print("File not found.")
