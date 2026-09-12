from block import Block


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(
            0,
            {
                "keterangan": "Genesis Block"
            },
            "0"
        )

    def add_block(self, data):
        previous_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            data,
            previous_block.hash
        )

        self.chain.append(new_block)

        return new_block

    def verify_diploma(self, nomor_ijazah):
        for block in self.chain:
            if block.data.get("nomor_ijazah") == nomor_ijazah:

                current_hash = block.calculate_hash()

                if current_hash != block.hash:
                    return False, "Data ijazah telah dimanipulasi!"

                if block.index > 0:
                    previous_block = self.chain[block.index - 1]

                    if block.previous_hash != previous_block.hash:
                        return False, "Blockchain telah rusak!"

                return True, block.data

        return False, "Ijazah tidak ditemukan."

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True