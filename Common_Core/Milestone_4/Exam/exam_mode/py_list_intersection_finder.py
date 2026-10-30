def list_intersection_finder(lists: list[list[int]]) -> list[int]:



print(list_intersection_finder([[1, 2, 3], [2, 3, 4], [2, 3, 5]]))  # Expected: [2, 3]
print(list_intersection_finder([[1, 2, 3, 4], [2, 4, 6, 8], [4, 8, 12]]))  # Expected: [4]
print(list_intersection_finder([[1, 1, 2, 3], [1, 2, 2, 3], [1, 2, 3, 3]]))  # Expected: [1, 2, 3]
print(list_intersection_finder([[1, 2, 3], [4, 5, 6]]))  # Expected: []
print(list_intersection_finder([]))  # Expected: []
print(list_intersection_finder([[1, 2, 3], []]))  # Expected: []
print(list_intersection_finder([[5]]))  # Expected: [5]