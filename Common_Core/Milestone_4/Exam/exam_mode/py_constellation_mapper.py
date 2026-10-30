def constellation_mapper(stars: list[tuple[int, int]], dim: int) -> list[str]:



print(constellation_mapper([(0, 0), (1, 1), (2, 2)], 3))  # Expected: ['*..', '.*.', '..*']
print(constellation_mapper([(1, 1), (0, 1), (2, 1), (1, 0), (1, 2)], 3))  # Expected: ['.*.', '***', '.*.']
print(constellation_mapper([], 2))  # Expected: ['..', '..']
print(constellation_mapper([(0, 0), (0, 0), (1, 1)], 2))  # Expected: ['*.', '.*']
print(constellation_mapper([(0, 0), (5, 5)], 3))  # Expected: ['*..', '...', '...']
print(constellation_mapper([(1, 0), (1, 1), (1, 2)], 3))  # Expected: ['...', '***', '...']
