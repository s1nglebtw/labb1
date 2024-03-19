import itertools
def finder(n):
    numbers = [1 , n]
    i = 2
    while i*i <= n:
        if n % i == 0:
            numbers.append(i)
            if i != n//i:
                numbers.append(n//i)
        i += 1
    numbers.sort()
    return numbers
for n in range(312614 , 312651):
    numbers = finder(n)
    if len(numbers) == 6:
        print(*numbers)
