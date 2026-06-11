def find_pairs(numbers, target):
    res = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                res.append((numbers[i], numbers[j]))
            else:
                continue
    return sorted(list(set(res)))


print(find_pairs([1, 1, 2, 3], 4))
