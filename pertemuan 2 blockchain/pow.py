import time


def proof_of_work(block, difficulty):
    target = "0" * difficulty

    start_time = time.time()

    # Mulai dari nonce 0
    block.nonce = 0

    while True:
        # Hitung hash menggunakan fungsi dari Block
        block.hash = block.calculate_hash()

        # Cek apakah hash memenuhi difficulty
        if block.hash.startswith(target):
            break

        # Jika belum memenuhi, tambah nonce
        block.nonce += 1

    end_time = time.time()

    waktu = end_time - start_time

    return block.nonce, waktu, block.hash