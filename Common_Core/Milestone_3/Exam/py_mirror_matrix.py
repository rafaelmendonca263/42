def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    for lista in matrix:
        lista.reverse()
    return matrix
