print('''
=======================================================================
\t\t\tPROGRAM DIAGNOSIS      
=======================================================================      
      ''')
ulang = int(input("Masukkan jumlah data pasien  : "))

namaPasien = []
umurInput = []
tinggiInput = []

for i in range(ulang):
    print('''
    =======================================================================
    \t\t\tFORM DATA PASIEN      
    =======================================================================      
      ''')
    namaInput = input('Masukkan Nama Pasien      : ')
    umurInput = input('Masukkan Umur Pasien      : ')
    tinggiInput = int(input('masukkan Tinggi Pasien  : '))

    print('''
    =======================================================================
    \t\t\tFORM DATA GEJALA      
    =======================================================================      
        ''')  
      
    gejala = []

    while True:
        gejalaInput = input('Masukkan gejala yang dialami : ')
        gejala.append(gejalaInput)
        print('---------------------------------------------------------------------------------')
        ulang = input('Apakah masih ada gejala nya [Y/T] : ')
        print()
        
        if ulang.lower() == 'n':  # menerima 'y' atau 'Y'
            print('Terimahkasih Sudah mengisi gejala anda :) ')
            break
        elif ulang.lower() == 'y':
            print('Silahkan isi kembali gejala anda ')
        else:
            print('Mohon maaf hanya bisa mengisi [Y/T]')
            continue
        

print('\nGejala yang dimasukkan:')
for x in range(len(gejala)):
    print(gejala[x])
        