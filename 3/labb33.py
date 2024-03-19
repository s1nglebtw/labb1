def calculate_x(i):
    if i == 1 or i == 2 or i == 3:
        return 1
    else:
        return calculate_x(i-1) + calculate_x(i-3)
i = 6
result = calculate_x(i)
print(f"x({i}) = {result}")

def calculate_x(i):
    if i == 1 or i == 2 or i == 3:
        return 1
    else:
        x1 = 1
        x2 = 1
        x3 = 1
        result = 0
        for j in range(4, i+1):
            result = x1 + x3
            x1, x2, x3 = x2, x3, result
        return result
i = 6
result = calculate_x(i)
print(f"x({i}) = {result}")
