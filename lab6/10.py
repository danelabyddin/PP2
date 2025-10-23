data = ['apple', 'banana', 'strawbery']

with open('fruits.txt', 'w') as f:
    for item in data:
        f.write(item + '\n')

print("List written to file")
