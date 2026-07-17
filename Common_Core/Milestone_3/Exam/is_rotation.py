from collections import deque


def is_rotation(arr1: list, arr2: list) -> bool:
    a = deque(arr1)
    b = deque(arr2)
    i = 0

    if len(arr1) != len(arr2):
        return False
    if not arr1 and not arr2:
        return True
    while i < len(arr1):
        if a == b:
            return True
        else:
            a.rotate(1)
            i = i + 1

    return False


print(is_rotation([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]))
print(is_rotation([1, 2, 3, 4, 5], [5, 1, 2, 3, 4]))
print(is_rotation([1, 2, 3], [3, 2, 1]))
