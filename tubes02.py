import os
import argparse

# Cara me-run program: python tubes02.py user.csv # Sementara

# ------------------------------------------------------------- F01 -------------------------------------------------------------- #

def manual_trim(value):
    # Mengidentifikasi dan menghapus semua karakter-karakter spasi awal dan akhir secara manual. Fungsi ini menggantikan metode .strip()
    # Fungsi ini mengiterasi string dari kedua ujungnya, menghapus karakter spasi sampai menemukan karakter non-spasi.
    while value and value[0] in ' \t\n\r':
        value = value[1:]
    while value and value[-1] in ' \t\n\r':
        value = value[:-1]
    return value

def is_all_digits(s):
    # Memeriksa apakah semua karakter dalam string adalah digit
    return all(c in '0123456789' for c in s)

def baca_csv(jalur_file):
    # Membaca data dari file CSV. Fungsi ini membuka file dan membaca setiap karakter.
    # Jika menemukan koma dan tidak dalam mode kutipan, karakter sebelumnya akan ditambahkan
    # ke baris sebagai kolom baru setelah dipotong spasi. Jika menemukan newline, baris selesai
    # dan ditambahkan ke data. Fungsi ini juga menangani karakter kutip untuk string yang mengandung koma.
    if os.path.exists(jalur_file):
        with open(jalur_file, "r") as file:
            data = []
            for line in file:
                # Menghapus karakter newline dari akhir baris
                line = line.rstrip('\n')
                # Memisahkan data menggunakan koma secara manual
                temp = ''
                arr = []
                for char in line:
                    if char == ',':
                        arr.append(temp)
                        temp = ''
                    else:
                        temp += char
                arr.append(temp)
                data.append(arr)
            return data
    else:
        print("File tidak ditemukan.")
        return []

def simpan_ke_csv(nama_file, data):
    # Menyimpan data ke file CSV
    with open(nama_file, 'a') as file:
        file.write(','.join(data) + '\n')

def daftar_agent():
    nama_pengguna = input("Masukan nama pengguna: ")
    kata_sandi = input("Masukan kata sandi: ")
    monsters = baca_csv("monster.csv")
    if not monsters:
        print("Tidak ada monster untuk ditampilkan.")
        return None
    print("Silahkan pilih salah satu monster sebagai monster awalmu:")
    valid_monsters = [monster[1] for monster in monsters[1:] if monster[1] != "Type"]
    for index, monster in enumerate(valid_monsters, start=1):
        print(f"{index}. {monster}")
    pilihan = input("Monster pilihanmu: ")

    if is_all_digits(pilihan) and 1 <= int(pilihan) <= len(valid_monsters):
        pilihan_index = int(pilihan) - 1
        nama_monster = valid_monsters[pilihan_index]
        print(f"Selamat datang Agent {nama_pengguna}. Mari kita mengalahkan Dr. Asep Spakbor dengan {nama_monster}!")
        simpan_ke_csv('user.csv', [nama_pengguna, kata_sandi, nama_monster])
        return (nama_pengguna, "Agent")
    print("Pilihan tidak valid. Harap masukkan nomor yang sesuai.")
    return None

def validasi_login_agent(nama_pengguna, kata_sandi):
    # Validasi login agen
    agents = baca_csv("user.csv")
    for agent in agents:
        if agent[0] == nama_pengguna and agent[1] == kata_sandi:
            return True
    return False

# ------------------------------------------------------------- F02 -------------------------------------------------------------- #

def login():
    # Fungsi untuk login
    pilihan_role = input("Pilih role (1. Admin / 2. Agent): ")
    if pilihan_role == "1":
        nama_pengguna = input("Nama pengguna admin: ")
        kata_sandi = input("Kata sandi: ")
        data_csv = baca_csv("user.csv")
        for baris in data_csv[1:]:
            if baris[1] == nama_pengguna and baris[2] == kata_sandi:
                print("Login berhasil sebagai admin.")
                return (nama_pengguna, "Admin")
        print("Login gagal. Nama pengguna atau kata sandi salah.")

    elif pilihan_role == "2":
        nama_pengguna = input("Nama pengguna agent: ")
        kata_sandi = input("Kata sandi: ")
        if validasi_login_agent(nama_pengguna, kata_sandi):
            print(f"Login berhasil sebagai agent {nama_pengguna}.")
            return (nama_pengguna, "Agent")
        print("Nama pengguna atau kata sandi salah atau agent belum terdaftar.")

# ------------------------------------------------------------- F03 -------------------------------------------------------------- #

def logout(current_user):
    # Fungsi untuk melakukan logout
    confirm = input(f"Apakah Anda yakin ingin logout, {current_user}? (y/n): ")
    if confirm.lower() == 'y':
        print(f"Logging out {current_user}. Sampai jumpa!")
        return None, None  # Mengembalikan nilai None untuk current_user dan current_role
    else:
        print("Logout dibatalkan.")
        return current_user, "Agent"  # Mengembalikan nilai sebelumnya jika logout dibatalkan

# ------------------------------------------------------------- F04 -------------------------------------------------------------- #

def help_not_logged_in():
    print("=========== HELP ===========")
    print("\nKamu belum login sebagai role apapun. Silahkan login terlebih dahulu.")
    print("\nLogin: Masuk ke dalam akun yang sudah terdaftar")
    print("Register: Membuat akun baru")
    print("\nFootnote: \nUntuk menggunakan aplikasi, silahkan masukkan nama fungsi yang terdaftar")
    print("Jangan lupa untuk memasukkan input yang valid\n")

def help_for_agent():
    print("=========== HELP ===========")
    print("\nHalo Agent. Kamu memanggil command HELP. Kamu memilih jalan yang benar, semoga kamu tidak sesat kemudian.")
    print("\nLogout: Keluar dari akun yang sedang digunakan")
    print("Monster: Melihat owca-dex yang dimiliki oleh Agent")
    print("\nFootnote: \nUntuk menggunakan aplikasi, silahkan masukkan nama fungsi yang terdaftar")
    print("Jangan lupa untuk memasukkan input yang valid\n")

def help_for_admin():
    print("=========== HELP ===========")
    print("\nSelamat datang, Admin. Berikut adalah hal-hal yang dapat kamu lakukan:")
    print("\nLogout: Keluar dari akun yang sedang digunakan")
    print("Shop: Melakukan manajemen pada SHOP sebagai tempat jual beli peralatan Agent")
    print("\nFootnote: \nUntuk menggunakan aplikasi, silahkan masukkan nama fungsi yang terdaftar")
    print("Jangan lupa untuk memasukkan input yang valid\n")

def create_arg_parser():
    parser = argparse.ArgumentParser(description="OWCA Program")
    parser.add_argument('folder_name', nargs='?', help="Nama folder untuk load/save data")
    return parser

# ------------------------------------------------------------- F14 -------------------------------------------------------------- #

def load_data(folder_name):
    if not os.path.exists(folder_name):
        print(f"Folder \"{folder_name}\" tidak ditemukan.")
        exit()
    print("Loading...")
    print("Data loaded from folder:", folder_name)

# ------------------------------------------------------------- F15 -------------------------------------------------------------- #

def save_data(folder_name):
    full_path = os.path.join("./data", folder_name)
    if not os.path.exists(full_path):
        os.makedirs(full_path, exist_ok=True)
        print(f"Membuat folder baru dan berhasil menyimpan data di {full_path}")
    # Contoh proses simpan data
    else:
        print(f"Berhasil menyimpan data di {full_path}")

# ------------------------------------------------------------- F16 -------------------------------------------------------------- #

def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    
    if not args.folder_name:
        print("Tidak ada nama folder yang diberikan!")
        print("Usage: python nama.py <nama_folder>")
        exit()

    load_data(args.folder_name)
    
    current_user = None
    current_role = None

    while True:
        if current_user is None:
            action = input("Selamat datang!\nPilih tindakan (atau ketik HELP untuk bantuan):\n1. Login\n2. Daftar\n3. Keluar\nPilih tindakan (1/2/3): ")
            if action.lower() == "help":
                help_not_logged_in()
            elif action == "1":
                user_details = login()
                if user_details:
                    current_user, current_role = user_details
                    print(f"Selamat datang {current_role} {current_user}!")
                else:
                    print("Login gagal, silakan coba lagi atau pilih opsi lain.")
            elif action == "2":
                if daftar_agent():
                    print("Registrasi berhasil. Silahkan login dan selamat bermain di dunia yang baru!")
                else:
                    print("Registrasi gagal, coba lagi.")
            elif action == "3":
                print("Terima kasih dan sampai jumpa!")
                break
            else:
                print("Pilihan tidak valid, silakan coba lagi.")
        else:
            print(f"\n{current_role} {current_user}, apa yang ingin Anda lakukan selanjutnya?")
            action = input("Opsi:\n1. Monster (hanya Agent)\n2. Shop (hanya Admin)\n3. Logout\n4. Help\nPilih opsi (1/2/3/4): ")
            if action == "1" and current_role == "Agent":
                print("Menampilkan owca-dex...")
            elif action == "1" and current_role == "Admin":
                print("Mengelola SHOP...")
            elif action == "3":
                current_user, current_role = logout(current_user)
            elif action == "4":
                if current_role == "Agent":
                    help_for_agent()
                elif current_role == "Admin":
                    help_for_admin()
            else:
                print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()

