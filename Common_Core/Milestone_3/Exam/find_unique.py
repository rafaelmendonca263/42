def find_unique(nums: list[int]) -> int:
    dict = set()
    
    for num in nums:
        if num in dict:
            dict.remove(num)
        else:
            dict.add(num)
    
    return dict.pop()

print(find_unique([2, 2, 1])) # 1
print(find_unique([4, 1, 2, 1, 2])) # 4
print(find_unique([7])) # 7