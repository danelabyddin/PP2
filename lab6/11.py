import string

for letter in string.ascii_uppercase:
    with open(letter + ".txt", "w") as f:
        f.write("This is file " + letter + ".txt")
print("Files created.")
