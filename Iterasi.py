#Iterasi Nested List
# Contoh data: nilai siswa per mata pelajaran
nilai_siswa = [
    # MTK  FIS  KIM  BIO
    [85,  90,  78,  92],  # Siswa 1
    [76,  88,  95,  84],  # Siswa 2  
    [92,  79,  88,  90]   # Siswa 3
]

# Method 1: Nested for loops
print("=== Method 1: Nested For Loops ===")
for i in range(len(nilai_siswa)):           # Iterasi baris
    print(f"Siswa {i+1}: ", end="")
    for j in range(len(nilai_siswa[i])):    # Iterasi kolom
        print(f"{nilai_siswa[i][j]} ", end="")
    print()

# Method 2: Direct iteration
print("\n=== Method 2: Direct Iteration ===")
for siswa in nilai_siswa:
    print(f"Nilai: {siswa}")

# Method 3: enumerate() untuk dapatkan index
print("\n=== Method 3: Dengan enumerate ===")
for idx, siswa in enumerate(nilai_siswa):
    print(f"Siswa {idx+1}: Rata-rata = {sum(siswa)/len(siswa):.2f}")