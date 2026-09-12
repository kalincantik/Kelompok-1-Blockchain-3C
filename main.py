from blockchain import Blockchain


blockchain = Blockchain()


print("=" * 50)
print(" SISTEM VERIFIKASI IJAZAH BERBASIS BLOCKCHAIN")
print("=" * 50)


print("\nAKTOR 1 - MAHASISWA")
print("-" * 50)

nama = input("Masukkan nama mahasiswa: ")
nim = input("Masukkan NIM: ")
program_studi = input("Masukkan program studi: ")
tahun_lulus = input("Masukkan tahun lulus: ")

print("\nMahasiswa mengajukan data kelulusan.")
print("Data berhasil dikirim ke Universitas.")


print("\nAKTOR 2 - UNIVERSITAS")
print("-" * 50)

universitas = input("Masukkan nama universitas: ")
nomor_ijazah = input("Masukkan nomor ijazah: ")

ijazah = {
    "nomor_ijazah": nomor_ijazah,
    "nama": nama,
    "nim": nim,
    "program_studi": program_studi,
    "universitas": universitas,
    "tahun_lulus": tahun_lulus
}

new_block = blockchain.add_block(ijazah)

print("\nIjazah berhasil diterbitkan oleh Universitas.")
print("Data ijazah berhasil ditambahkan ke Blockchain.")
print("Block ke :", new_block.index)
print("Hash     :", new_block.hash)


print("\nAKTOR 3 - PERUSAHAAN / INSTANSI")
print("-" * 50)

print("Perusahaan menerima ijazah dari mahasiswa.")
nomor_verifikasi = input("Masukkan nomor ijazah yang akan diverifikasi: ")

print("\nPermintaan verifikasi dikirim ke Verifikator.")


print("\nAKTOR 4 - VERIFIKATOR")
print("-" * 50)

status, hasil = blockchain.verify_diploma(nomor_verifikasi)

if status:
    print("\n" + "=" * 50)
    print(" IJAZAH VALID")
    print("=" * 50)

    print("Nomor Ijazah :", hasil["nomor_ijazah"])
    print("Nama         :", hasil["nama"])
    print("NIM          :", hasil["nim"])
    print("Program Studi:", hasil["program_studi"])
    print("Universitas  :", hasil["universitas"])
    print("Tahun Lulus  :", hasil["tahun_lulus"])

else:
    print("\n" + "=" * 50)
    print(" IJAZAH TIDAK VALID")
    print("=" * 50)

    print("Keterangan:", hasil)


print("\nSTATUS BLOCKCHAIN")
print("-" * 50)

if blockchain.is_chain_valid():
    print("Blockchain VALID dan tidak dimanipulasi.")
else:
    print("Blockchain TIDAK VALID!")