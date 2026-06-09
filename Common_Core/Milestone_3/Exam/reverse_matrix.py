
def reverse_matrix(matrix):
    res = []
    for listas in matrix:
        res.append(list(reversed(listas)))
    return list(reversed(res))


""" matriz = [
    [1, 2, 3],
    [4, 5, 6]
]

print(reverse_matrix(matriz))
 """
