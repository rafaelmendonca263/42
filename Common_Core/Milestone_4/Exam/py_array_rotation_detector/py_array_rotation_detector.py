def array_rotation_detector(arr1: list, arr2: list) -> bool:
    if len(arr1) != len(arr2):
        return False
    if len(arr1) == 0:
        return True
    if arr1[0] in arr2:
        index = arr2.index(arr1[0])
        rotated_arr2 = arr2[index:] + arr2[:index]
        return rotated_arr2 == arr1


print(array_rotation_detector([1, 2, 3, 4, 5], [4, 5, 1, 2, 3])) # True
print(array_rotation_detector([1, 2, 3, 4, 5], [5, 1, 2, 3, 4])) # True
print(array_rotation_detector([1, 2, 3], [3, 2, 1])) # False
print(array_rotation_detector([1, 2], [1, 2, 3])) # False
print(array_rotation_detector([], [])) # True