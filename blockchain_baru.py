
from pathlib import Path
import json

from web3 import Web3
from config import (
    RPC_URL,
    EXPECTED_CHAIN_ID,
    CONTRACT_ADDRESS,
    ABI_PATH
)


class BlockchainService:

    def __init__(self):
        self.w3 = Web3(
            Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 10})
        )

        if not self.w3.is_connected():
            raise ConnectionError("Blockchain tidak terhubung!")

        self.chain_id = self.w3.eth.chain_id

        if self.chain_id != EXPECTED_CHAIN_ID:
            raise ConnectionError(
                f"Chain ID tidak sesuai: {self.chain_id}"
            )

        if not Web3.is_address(CONTRACT_ADDRESS):
            raise ValueError("Alamat kontrak tidak valid!")

        abi_path = Path(ABI_PATH)

        if not abi_path.is_absolute():
            abi_path = Path(__file__).parent / abi_path

        if not abi_path.exists():
            raise FileNotFoundError(
                f"File ABI tidak ditemukan: {abi_path}"
            )

        with open(abi_path, "r", encoding="utf-8") as file:
            artifact = json.load(file)

        self.contract_address = Web3.to_checksum_address(
            CONTRACT_ADDRESS
        )

        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=artifact["abi"]
        )

        self.admin = self.contract.functions.admin().call()

    def is_connected(self):
        return self.w3.is_connected()

    def send_transaction(self, function):
        tx_hash = function.transact({
            "from": self.admin
        })

        receipt = self.w3.eth.wait_for_transaction_receipt(
            tx_hash,
            timeout=120
        )

        if receipt.status != 1:
            raise RuntimeError("Transaksi gagal!")

        return receipt

    def add_degree(
        self, nama, nim, prodi,
        nomor_ijazah, tahun_lulus, pemilik
    ):
        if not Web3.is_address(pemilik):
            raise ValueError("Alamat wallet tidak valid!")

        receipt = self.send_transaction(
            self.contract.functions.tambahIjazah(
                nama,
                nim,
                prodi,
                nomor_ijazah,
                int(tahun_lulus),
                Web3.to_checksum_address(pemilik)
            )
        )

        token_id = self.get_token_id(nomor_ijazah)

        return {
            "token_id": token_id,
            "transaction_hash": receipt.transactionHash.hex(),
            "block_number": receipt.blockNumber
        }

    def get_status(self, nomor_ijazah):
        registered, revoked, valid = (
            self.contract.functions.statusIjazah(
                nomor_ijazah
            ).call()
        )

        return {
            "registered": registered,
            "revoked": revoked,
            "valid": valid
        }

    def get_degree(self, nomor_ijazah):
        data = self.contract.functions.lihatDataIjazah(
            nomor_ijazah
        ).call()

        return {
            "nama": data[0],
            "nim": data[1],
            "prodi": data[2],
            "nomor_ijazah": data[3],
            "tahun_lulus": int(data[4])
        }

    def verify_degree(self, nomor_ijazah):
        return self.contract.functions.cekKeaslianData(
            nomor_ijazah
        ).call()

    def revoke_degree(self, nomor_ijazah, alasan):
        receipt = self.send_transaction(
            self.contract.functions.cabutIjazah(
                nomor_ijazah,
                alasan
            )
        )

        return receipt.transactionHash.hex()

    def get_token_id(self, nomor_ijazah):
        return int(
            self.contract.functions.getTokenId(
                nomor_ijazah
            ).call()
        )

    def get_owner(self, token_id):
        return self.contract.functions.getOwner(
            int(token_id)
        ).call()

    def get_all_records(self):
        logs = self.contract.events.IjazahDitambahkan.get_logs(
            from_block=0
        )

        nomor_tercatat = []

        for log in logs:
            nomor = log["args"]["nomorIjazah"]

            if nomor not in nomor_tercatat:
                nomor_tercatat.append(nomor)

        records = []

        for nomor in nomor_tercatat:
            data = self.get_degree(nomor)
            status = self.get_status(nomor)

            records.append({
                "token_id": self.get_token_id(nomor),
                "nama": data["nama"],
                "nim": data["nim"],
                "prodi": data["prodi"],
                "nomor_ijazah": data["nomor_ijazah"],
                "tahun_lulus": data["tahun_lulus"],
                "status": (
                    "Dicabut" if status["revoked"] else "Valid"
                ),
                "valid": status["valid"],
                "revoked": status["revoked"]
            })

        return sorted(
            records,
            key=lambda x: x["token_id"],
            reverse=True
        )
