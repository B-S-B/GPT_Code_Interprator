def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Calculate the factorial of a number
num = 5
result = factorial(num)

# Print the result
print(result)