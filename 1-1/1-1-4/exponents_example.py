product = 1

base = int(input("Enter the base: "))
exponent = int(input("Enter the exponent: "))

for l in range(exponent):
    product = product * base

print(product)