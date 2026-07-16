from collections import deque


def twist_sequence(arr: list[int],
                   k: int) -> list[int]:

    d = deque(arr)
    d.rotate(k)
    return list(d)


print(twist_sequence([1, 2, 3, 4, 5], 2))
print(twist_sequence([1, 2, 3], 1))
print(twist_sequence([1, 2, 3, 4], 0))
print(twist_sequence([1, 2, 3], 5))
print(twist_sequence([], 3))
print(twist_sequence([1, 2, 3], 7))
