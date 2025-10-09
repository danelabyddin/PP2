
def generate_squares(n):
    for i in range(n + 1):
        yield i ** 2

print("Squares up to N:")
for val in generate_squares(5):
    print(val, end=" ")
print("\n")




def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input("Enter number: "))
print(",".join(str(i) for i in even_numbers(n)))




def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

print("Numbers divisible by 3 and 4:")
for num in divisible_by_3_and_4(50):
    print(num, end=" ")
print("\n")



def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

print("Squares from 3 to 7:")
for val in squares(3, 7):
    print(val, end=" ")
print("\n")




def countdown(n):
    while n >= 0:
        yield n
        n -= 1

print("Countdown from 5:")
for i in countdown(5):
    print(i, end=" ")
print("\n")
