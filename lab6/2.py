text = input()

upper = 0
lower = 0

for let in text:
    if let.isupper():
        upper += 1
    elif let.islower():
        lower += 1

print(upper)
print(lower)
