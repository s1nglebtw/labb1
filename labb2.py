import itertools
letters = ['X', 'Z', 'A', 'B', 'C', 'D', 'E']
positions = 4
possible_combinations = len(list(itertools.product(letters[:2], repeat=2))) * len(list(itertools.product(letters[2:], repeat=2)))
count = (possible_combinations)
print("Количество различных кодовых слов, которые может использовать Олег:", count)
