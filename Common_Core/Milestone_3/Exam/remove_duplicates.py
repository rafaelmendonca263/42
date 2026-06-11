def remove_duplicates(numbers):
    res = []
    for num in numbers:
        if num not in res:
            res.append(num)
    return res
