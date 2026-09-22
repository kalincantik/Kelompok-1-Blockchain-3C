from block import Block
from pow import proof_of_work
from pos import proof_of_stake


# PROOF OF WORK

print("PROOF OF WORK")

print("\nEksperimen PoW dengan difficulty 2, 3, 4, dan 5")

hasil_pow = []

for difficulty in [2, 3, 4, 5]:

    # Membuat block baru untuk setiap percobaan
    block = Block(
        index=1,
        data={
            "jenis": "Ijazah Akademik",
            "nomor_ijazah": "IJZ-001",
            "nama": "SUMANTO"
        },
        previous_hash="0"
    )

    # Menjalankan Proof of Work
    nonce, waktu, hash_block = proof_of_work(
        block,
        difficulty
    )

    hasil_pow.append({
        "difficulty": difficulty,
        "nonce": nonce,
        "waktu": waktu,
        "hash": hash_block
    })


# Menampilkan hasil PoW
print("\nHASIL EKSPERIMEN PoW")

print(
    f"{'Difficulty':<12}"
    f"{'Nonce':<12}"
    f"{'Waktu (detik)':<18}"
    f"Hash"
)

print("-" * 60)

for hasil in hasil_pow:
    print(
        f"{hasil['difficulty']:<12}"
        f"{hasil['nonce']:<12}"
        f"{hasil['waktu']:<18.4f}"
        f"{hasil['hash']}"
    )


# PROOF OF STAKE

print("\n")
print("PROOF OF STAKE")


# Percobaan 1

validators_1 = {
    "Universitas": 10,
    "Instansi Pendidikan": 20,
    "Lembaga Pemerintah": 30,
    "Perusahaan": 40
}

print("\nPERCOBAAN 1")
print("-" * 60)
print("Nilai stake:")

for validator, stake in validators_1.items():
    print(f"{validator:<25}: {stake}")


# Menyimpan jumlah terpilih
hasil_1 = {
    validator: 0
    for validator in validators_1
}


# Simulasi 20 kali
for i in range(20):

    selected = proof_of_stake(validators_1)

    hasil_1[selected] += 1


print("\nHasil simulasi 20 kali:")

for validator, jumlah in hasil_1.items():
    print(f"{validator:<25}: {jumlah} kali")


# Percobaan 2
validators_2 = {
    "Universitas": 70,
    "Instansi Pendidikan": 10,
    "Lembaga Pemerintah": 10,
    "Perusahaan": 10
}

print("\n")
print("PERCOBAAN 2")
print("-" * 60)
print("Nilai stake:")

for validator, stake in validators_2.items():
    print(f"{validator:<25}: {stake}")


# Menyimpan jumlah terpilih
hasil_2 = {
    validator: 0
    for validator in validators_2
}


# Simulasi 20 kali
for i in range(20):

    selected = proof_of_stake(validators_2)

    hasil_2[selected] += 1


print("\nHasil simulasi 20 kali:")

for validator, jumlah in hasil_2.items():
    print(f"{validator:<25}: {jumlah} kali")


print("SELESAI")
