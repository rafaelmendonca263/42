def find_max_triplet(numbers: list[int]) -> int:
    numbers = sorted(numbers)
    
    temp_pos = numbers[len(numbers) - 3] * numbers[len(numbers) - 2] * numbers[len(numbers) - 1]
    temp_neg = numbers[0] * numbers[1] * numbers[len(numbers) - 1]
    
    if temp_neg > temp_pos:
        res = temp_neg
    else:
        res = temp_pos
    return res
        
print(find_max_triplet([1, 2, 3, 4]))
print(find_max_triplet([-10, -10, 5, 2]))
print(find_max_triplet([-1, -2, -3, -4]))
