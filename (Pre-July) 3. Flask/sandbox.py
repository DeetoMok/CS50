#Taking in an input
#name = input()
from pyclbr import Class

name = "Daryl"
#f is to print in format String. I this case, the variable "name"
print(f"Hello, {name}!")

# initiating a variable does not require u to specify the data type
i = 28
f = 2.8
b = False
n = None

# Conditional statements
x = 28

if x > 0:
    print("x is positive")
elif x < 0:
    print("x is negative")
else:
    print("x is zero")

#Python Tuple
coordinates = (10.0,20.0)


#List
# Note items in the list do not have to be of the same type
names = ["Alice", "Bob", "Charlie"]

#Loops
for i in range(5):
    print(i)

for name in names:
    print(name)

# Set is unordered set
s = set()
s.add(1)
s.add(3)
s.add(5)
s.add(3)

print(s)

# Dictionary is unordered hash map
ages = {"Alice": 22, "Bob": 27}
ages["Charlie"] = 30
ages["Alice"] += 1

print(ages)

#defining a function
def square(x):
    return x * x

# older way of format
for i in range(10):
    print("{} squared is {}".format(i, square(i)))
    print(f"{i}, {square(i)}")

# modules
# from (fileName) import (functionName)

# Separating a main function from other functions so that importing of specific functions
# is possible

def main():
    for i in range(10):
        print("{} squared is {}".format(i, square(i)))
        print(f"{i}, {square(i)}")

if __name__ == "__main__":  #if I am currently running this particular file...
    main()
