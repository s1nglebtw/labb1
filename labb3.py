def is_palindrome(s):
    if len(s) <= 1:
        return True
    elif s[0] != s[-1]:
        return False
    else:
        return is_palindrome(s[1:-1])
s1 = [12321]
s2 = "spam"
print(is_palindrome(s1))
print(is_palindrome(s2))

def is_palindrome(d):
    return d == d[::-1]
d1 = [12321]
d2 = "spam"
print(is_palindrome(d1))
print(is_palindrome(d2))
