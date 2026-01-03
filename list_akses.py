#2. Akses Element (Indexing)
matrix = [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
]

# Akses element tunggal
print(matrix[0][0])    # 10 (baris 0, kolom 0)
print(matrix[1][2])    # 60 (baris 1, kolom 2)
print(matrix[2][1])    # 80 (baris 2, kolom 1)

# Akses seluruh baris
print(matrix[0])       # [10, 20, 30] (baris 0)
print(matrix[1])       # [40, 50, 60] (baris 1)

# Negative indexing
print(matrix[-1][-1])  # 90 (baris terakhir, kolom terakhir)
print(matrix[-2][0])   # 40 (baris kedua dari akhir, kolom 0)