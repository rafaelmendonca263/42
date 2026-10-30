
def merge_sorted_lists(lists: list[list[int]]) -> list[int]:
    merged_list = []
    for lista in lists:
        merged_list.extend(lista)

    n = len(merged_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if merged_list[j] > merged_list[j + 1]:
                merged_list[j], merged_list[j + 1] = merged_list[j + 1], merged_list[j]
    return merged_list

print(merge_sorted_lists([[1, 3, 5], [2, 4, 6]]))  # Expected: [1, 2, 3, 4, 5, 6]
print(merge_sorted_lists([[1, 5, 9], [2, 3, 8], [4, 6, 7]]))  # Expected: [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(merge_sorted_lists([[5], [1, 3], [2, 4]]))  # Expected: [1, 2, 3, 4, 5]
print(merge_sorted_lists([[1, 1, 2], [2, 3, 3]]))  # Expected: [1, 1, 2, 2, 3, 3]
print(merge_sorted_lists([[], [1, 2, 3]]))  # Expected: [1, 2, 3]
print(merge_sorted_lists([[]]))  # Expected: []
print(merge_sorted_lists([[-5, -1, 0], [-3, 2, 4]]))  # Expected: [-5, -3, -1, 0, 2, 4]
print(merge_sorted_lists([[10], [10], [10]]))  # Expected: [10, 10, 10]