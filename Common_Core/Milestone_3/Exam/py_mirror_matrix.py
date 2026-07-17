def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
    for lista in matrix:
        lista.reverse()
    
    return matrix

print(mirror_matrix([[1,2,3],[4,5,6]]))
print(mirror_matrix([[1,2],[3,4],[5,6]]))
print(mirror_matrix([[7]]))
print(mirror_matrix([[1,2,3,4]]))
print(mirror_matrix([[-1,-2],[-3,-4]]))