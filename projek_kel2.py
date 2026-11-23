

# ==================================================
# FITUR 1. KONEKSI DATABASE
# ==================================================

import psycopg2
import pandas as pd
import os

def connectDB():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="kuc1ngsql",
            dbname="modul_3"
        )

        cur = conn.cursor()

        return conn, cur

    except Exception as error:
        print("Koneksi database gagal:", error)
        return None, None
#header
def header():
    os.system('cls')
    with open('header.txt', 'r', encoding='utf-8') as file:
        filetxt = file.read()
    print(filetxt)
# ==================================================
# FITUR 2. REGISTRASI AKUN
# ==================================================

def registrasi():
    conn, cursor = connectDB()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        print("\n=== REGISTRASI AKUN ===")

        nama = input("Nama lengkap: ")
        username = input("Username: ")
        password = input("Password: ")
        no_hp = input("Nomor HP: ")

        print("\nPilih jenis akun:")
        print("1. Petani")
        print("2. Pengepul")

        pilihan = input("Pilihan: ")

        if pilihan == "1":
            role = "petani"
        elif pilihan == "2":
            role = "pengepul"
        else:
            print("Pilihan tidak valid.")
            return

        cursor.execute("""
            INSERT INTO users
            (id_user_role, username, password,
             nama_lengkap, no_hp, status_akun)
            VALUES (
                (SELECT id_user_role
                 FROM user_role
                 WHERE nama_role = %s),
                %s, %s, %s, %s, 'aktif'
            )
        """, (role, username, password, nama, no_hp))

        conn.commit()
        print("Registrasi berhasil!")

    except Exception as e:
        conn.rollback()
        print("Registrasi gagal:", e)

    finally:
        cursor.close()
        conn.close()


# ==================================================
# FITUR 3. LOGIN
# ==================================================

def login():
    conn, cursor = connectDB()

    if conn is None:
        return

    try:
        print("\n========== LOGIN SIPANEN ==========")
        username = input("Username: ")
        password = input("Password: ")

        cursor.execute("""
            SELECT
                u.id_user,
                u.nama_lengkap,
                r.nama_role
            FROM users u
            JOIN user_role r
                ON u.id_user_role = r.id_user_role
            WHERE u.username = %s
              AND u.password = %s
        """, (username, password))

        akun = cursor.fetchone()

        if akun is None:
            print("Username atau password salah!")
            return

        id_user = akun[0]
        nama = akun[1]
        role = akun[2].lower().strip()

        print(f"\nSelamat datang, {nama}!")

        # Mengarahkan pengguna sesuai role
        if role == "admin":
            menu_admin(id_user)
            input("Enter untuk melanjutkan....")

        elif role == "petani":
            menu_petani(id_user)
            input("Enter untuk melanjutkan....")

        elif role == "pengepul":
            menu_pengepul(id_user)
            input("Enter untuk melanjutkan....")

        else:
            print("Role pengguna tidak dikenali!")

    except Exception as e:
        print("Login gagal:", e)

    finally:
        cursor.close()
        conn.close()

# ==================================================
# FITUR 4. LOGOUT
# ==================================================

def logout():
    print("\nAnda berhasil logout.")
    print("Terima kasih telah menggunakan SIPANEN.")

# ==================================================
# FITUR 5. MENAMPILKAN JENIS TEH
# ==================================================

def tampilkan_jenis_teh():
    conn, cursor = connectDB()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id_jenis_teh, nama_jenis_teh,
                   deskripsi, satuan
            FROM jenis_teh
            ORDER BY id_jenis_teh
        """)

        data = cursor.fetchall()

        print("\n=== DAFTAR JENIS TEH ===")

        for row in data:
            print("ID:", row[0])
            print("Nama:", row[1])
            print("Deskripsi:", row[2])
            print("Satuan:", row[3])
            print("-------------------------")

    except Exception as e:
        print("Gagal menampilkan jenis teh:", e)

    finally:
        cursor.close()
        conn.close()


# ==================================================
# FITUR 6. MENAMBAHKAN JENIS TEH
# ==================================================

def tambah_jenis_teh():
    conn = connectDB()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        print("\n=== TAMBAH JENIS TEH ===")

        nama = input("Nama jenis teh: ")
        deskripsi = input("Deskripsi: ")
        satuan = input("Satuan: ")

        cursor.execute("""
            INSERT INTO jenis_teh
            (nama_jenis_teh, deskripsi, satuan)
            VALUES (%s, %s, %s)
        """, (nama, deskripsi, satuan))

        conn.commit()
        print("Jenis teh berhasil ditambahkan.")

    except Exception as e:
        conn.rollback()
        print("Gagal menambahkan jenis teh:", e)

    finally:
        cursor.close()
        conn.close()


# ==================================================
# FITUR 7. MENGUBAH JENIS TEH
# ==================================================

def ubah_jenis_teh():
    conn, curr = connectDB()
    if conn is None:
        return

    curr = conn.cursor()

    try:
        id_jenis = int(input("Masukkan ID jenis teh: "))
        nama = input("Nama jenis teh baru: ")
        deskripsi = input("Deskripsi baru: ")
        satuan = input("Satuan baru: ")

        curr.execute("""
            UPDATE jenis_teh
            SET nama_jenis_teh = %s,
                deskripsi = %s,
                satuan = %s
            WHERE id_jenis_teh = %s
        """, (nama, deskripsi, satuan, id_jenis))

        conn.commit()

        if curr.rowcount > 0:
            print("Jenis teh berhasil diubah.")
        else:
            print("Data jenis teh tidak ditemukan.")

    except Exception as e:
        conn.rollback()
        print("Gagal mengubah jenis teh:", e)

    finally:
        curr.close()
        conn.close()


# ==================================================
# FITUR 8. MENGHAPUS JENIS TEH
# ==================================================

def hapus_jenis_teh():
    conn, curr = connectDB()
    if conn is None:
        return

    curr = conn.cursor()

    try:
        id_jenis = int(input("Masukkan ID jenis teh: "))

        curr.execute("""
            DELETE FROM jenis_teh
            WHERE id_jenis_teh = %s
        """, (id_jenis,))

        conn.commit()

        if curr.rowcount > 0:
            print("Jenis teh berhasil dihapus.")
        else:
            print("Data tidak ditemukan.")

    except Exception as e:
        conn.rollback()
        print("Gagal menghapus jenis teh:", e)

    finally:
        curr.close()
        conn.close()

# ==================================================
# FITUR 9. MENAMBAHKAN HASIL PANEN
# ==================================================

def tambah_hasil_panen(id_user):
    conn, curr = connectDB()
    if conn is None:
        return

    try:
        tampilkan_jenis_teh()

        print("\n=== TAMBAH HASIL PANEN ===")

        id_jenis = int(input("ID jenis teh: "))
        jumlah = float(input("Jumlah tersedia (kg): "))
        kualitas = input("Kualitas: ")
        harga = float(input("Harga awal per kg: "))
        deskripsi = input("Deskripsi: ")

        curr.execute("""
            INSERT INTO hasil_panen
            (id_user, id_jenis_teh, jumlah_tersedia,
             kualitas, tanggal_panen, harga_awal,
             status_hasil, deskripsi)
            VALUES (%s, %s, %s, %s, CURRENT_DATE,
                    %s, 'tersedia', %s)
        """, (
            id_user, id_jenis, jumlah,
            kualitas, harga, deskripsi
        ))

        conn.commit()
        print("Hasil panen berhasil ditambahkan.")

    except Exception as e:
        conn.rollback()
        print("Gagal menambahkan hasil panen:", e)

    finally:
        curr.close()
        conn.close()


# ==================================================
# FITUR 10. MENAMPILKAN HASIL PANEN SENDIRI
# ==================================================

def hasil_panen_saya(id_user):
    conn, curr = connectDB()
    if conn is None:
        return

    try:
        curr.execute("""
            SELECT hp.id_hasil_panen,
                   j.nama_jenis_teh,
                   hp.jumlah_tersedia,
                   hp.kualitas,
                   hp.tanggal_panen,
                   hp.harga_awal,
                   hp.status_hasil
            FROM hasil_panen hp
            JOIN jenis_teh j
                ON hp.id_jenis_teh = j.id_jenis_teh
            WHERE hp.id_user = %s
            ORDER BY hp.tanggal_panen DESC
        """, (id_user,))

        data = curr.fetchall()

        print("\n=== HASIL PANEN SAYA ===")

        for row in data:
            print("ID Panen:", row[0])
            print("Jenis Teh:", row[1])
            print("Jumlah:", row[2], "kg")
            print("Kualitas:", row[3])
            print("Tanggal:", row[4])
            print("Harga:", row[5])
            print("Status:", row[6])
            print("-------------------------")

        if not data:
            print("Belum ada hasil panen.")

    except Exception as e:
        print("Gagal menampilkan hasil panen:", e)

    finally:
        curr.close()
        conn.close()


# ==================================================
# FITUR 11. MENGUBAH HASIL PANEN
# ==================================================

def ubah_hasil_panen(id_user):
    conn, curr= connectDB()
    if conn is None:
        return

    try:
        hasil_panen_saya(id_user)

        id_panen = int(input("ID hasil panen: "))
        jumlah = float(input("Jumlah baru: "))
        kualitas = input("Kualitas baru: ")
        harga = float(input("Harga baru: "))

        curr.execute("""
            UPDATE hasil_panen
            SET jumlah_tersedia = %s,
                kualitas = %s,
                harga_awal = %s
            WHERE id_hasil_panen = %s
              AND id_user = %s
              AND NOT EXISTS (
                  SELECT 1
                  FROM detail_pesanan dp
                  JOIN transaksi tr
                    ON tr.id_pesanan = dp.id_pesanan
                  WHERE dp.id_hasil_panen =
                        hasil_panen.id_hasil_panen
              )
        """, (jumlah, kualitas, harga, id_panen, id_user))

        conn.commit()

        if curr.rowcount > 0:
            print("Hasil panen berhasil diubah.")
        else:
            print("Data tidak ditemukan atau sudah terikat transaksi.")

    except Exception as e:
        conn.rollback()
        print("Gagal mengubah hasil panen:", e)

    finally:
        curr.close()
        conn.close()


# ==================================================
# FITUR 12. MENGHAPUS HASIL PANEN
# ==================================================

def hapus_hasil_panen(id_user):
    conn, curr = connectDB()
    if conn is None:
        return

    try:
        hasil_panen_saya(id_user)

        id_panen = int(input("ID hasil panen yang dihapus: "))

        curr.execute("""
            DELETE FROM hasil_panen hp
            WHERE hp.id_hasil_panen = %s
              AND hp.id_user = %s
              AND NOT EXISTS (
                  SELECT 1
                  FROM detail_pesanan dp
                  WHERE dp.id_hasil_panen = hp.id_hasil_panen
              )
        """, (id_panen, id_user))

        conn.commit()

        if curr.rowcount > 0:
            print("Hasil panen berhasil dihapus.")
        else:
            print("Data tidak ditemukan atau sudah memiliki pesanan.")

    except Exception as e:
        conn.rollback()
        print("Gagal menghapus hasil panen:", e)

    finally:
        curr.close()
        conn.close()

def menu_utama():
    while True:
        print("\n========== SIPANEN ==========")
        print("Sistem Penjualan Hasil Panen Teh")
        print("=============================")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            login()
            input("Enter untuk melanjutkan....")
        elif pilihan == "2":
            registrasi()
            input("Enter untuk melanjutkan....")
        elif pilihan == "3":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!")
            input("Enter untuk melanjutkan....")

#melihat hasil panen untuk pengepul
def daftar_hasil_panen():
    hasil_panen_saya()

#melihat riwayat transaksi
def riwayat_transaksi(id_pengepul):
    conn, curr = connectDB()
    if conn is None:
        return

    curr.execute("""
        SELECT t.id_transaksi, p.tanggal_pesanan,
               t.total_harga, st.nama_status
        FROM transaksi t
        JOIN pesanan p
            ON t.id_pesanan = p.id_pesanan
        JOIN status_transaksi st
            ON t.id_status_transaksi = st.id_status_transaksi
        WHERE p.id_pengepul = %s
        ORDER BY p.tanggal_pesanan DESC
    """, (id_pengepul,))

    data = curr.fetchall()

    print("\n=== RIWAYAT TRANSAKSI ===")

    if data:
        for item in data:
            print(
                f"\nID Transaksi: {item[0]}"
                f"\nTanggal: {item[1]}"
                f"\nTotal Harga: Rp{item[2]:,.0f}"
                f"\nStatus: {item[3]}"
            )
            print("-" * 35)
    else:
        print("Belum terdapat riwayat transaksi.")

    curr.close()
    conn.close()

#fitur menu petani
def menu_petani(id_user):

    id_petani = id_user

    while True:
        header()
        print("\n=== MENU PETANI ===")
        print("1. Tambah Hasil Panen")
        print("2. Lihat Hasil Panen")
        print("3. Ubah Hasil Panen")
        print("4. Hapus Hasil Panen")
        print("5. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_hasil_panen(id_petani) 
            input("Enter untuk melanjutkan...")
        elif pilihan == "2":
            hasil_panen_saya(id_petani)
            input("Enter untuk melanjutkan...")
        elif pilihan == "3":
            ubah_hasil_panen(id_petani)
            input("Enter untuk melanjutkan...")
        elif pilihan == "4":
            hapus_hasil_panen(id_petani)
            input("Enter untuk melanjutkan...")
        elif pilihan == "5":
            logout()
            break
        else:
            print("Pilihan tidak valid.")
            input("Enter untuk melanjutkan....")

#fitur menu pengepul
def menu_pengepul(id_user):
   
    id_pengepul = (id_user)

    while True:
        print("\n=== MENU PENGEPUL ===")
        print("1. Lihat Daftar Hasil Panen")
        print("2. Lihat Riwayat Transaksi")
        print("3. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            daftar_hasil_panen()
            input("Enter untuk melanjutkan....")
        elif pilihan == "2":
            riwayat_transaksi(id_pengepul)
            input("Enter untuk melanjutkan....")
        elif pilihan == "3":
            logout()
            break
        else:
            print("Pilihan tidak valid.")
            input("Enter untuk melanjutkan....")

#fitur menu admin
def menu_admin():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Lihat Daftar Hasil Panen")
        print("2. Lihat Jenis Teh")
        print("3. Lihat Riwayat Transaksi")
        print("4. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            hasil_panen_saya()
            input("Enter untuk melanjutkan....")

        elif pilihan == "2":
            tampilkan_jenis_teh()
            input("Enter untuk melanjutkan....")

        elif pilihan == "3":
            tampilkan_semua_transaksi()
            input("Enter untuk melanjutkan....")

        elif pilihan == "4":
            logout()
            break

        else:
            print("Pilihan tidak valid.")
            input("Enter untuk melanjutkan....")

#menampilkan seluruh transaksi
def tampilkan_semua_transaksi():
    conn, cursor = connectDB()
    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.id_transaksi, p.id_pesanan,
               p.tanggal_pesanan, t.total_harga,
               st.nama_status
        FROM transaksi t
        JOIN pesanan p
            ON t.id_pesanan = p.id_pesanan
        JOIN status_transaksi st
            ON t.id_status_transaksi = st.id_status_transaksi
        ORDER BY p.tanggal_pesanan DESC
    """)

    data = cursor.fetchall()

    print("\n=== DATA SELURUH TRANSAKSI ===")

    if data:
        for item in data:
            print(
                f"\nID Transaksi: {item[0]}"
                f"\nID Pesanan: {item[1]}"
                f"\nTanggal: {item[2]}"
                f"\nTotal Harga: Rp{item[3]:,.0f}"
                f"\nStatus: {item[4]}"
            )
            print("-" * 35)
    else:
        print("Belum ada transaksi.")

    cursor.close()
    conn.close()

#
# ==========================================
# MENJALANKAN PROGRAM SIPANEN
# ==========================================

def menuUtama():
    while True:
        header()

        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            login()
            input("Enter untuk melanjutkan....")
            
        elif pilihan == "2":
            registrasi()
            input("Enter untuk melanjutkan....")

        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan SIPANEN.")
            break

        else:
            print("Pilihan tidak valid.")
            input("Enter untuk melanjutkan....")

menuUtama()
