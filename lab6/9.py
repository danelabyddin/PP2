file = input()

with open(file, 'r') as f:
    lines = f.readlines()
    print("Number of lines:", len(lines))
