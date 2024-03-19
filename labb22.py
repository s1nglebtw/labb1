import itertools
s = 49**10 + 7**30 - 49
s_base = ""
while s > 0:
    s_base = str(s % 7) + s_base
    s //= 7
count = len([int(d) for d in str(s_base) if d == "6"])
print(count)
