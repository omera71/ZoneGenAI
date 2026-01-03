# 1D List (list biasa)
simple_list = [1, 2, 3, 4, 5]
print("1D List:", simple_list  )

# 2D List (list of lists)
matrix_2d = [
    [1, 2, 3],     # Baris 0
    [4, 5, 6],     # Baris 1  
    [7, 8, 9]      # Baris 2
]
print("2D List:", matrix_2d)

# 3D List (list of lists of lists)
cube_3d = [
    [   # Layer 0
        [1, 2, 3],
        [4, 5, 6]
    ],
    [   # Layer 1
        [7, 8, 9],
        [10, 11, 12]
    ]
]

print("3D List:", cube_3d)

# Nested list dengan tipe data berbeda
mixed_nested = [
    [1, 2.5, "hello"],      # Baris 0: int, float, string
    [True, None, [1, 2]],   # Baris 1: bool, None, list
    [{"key": "value"}]      # Baris 2: dictionary
]
print("Mixed Nested List:", mixed_nested)
