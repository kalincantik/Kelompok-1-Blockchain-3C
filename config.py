from pathlib import Path

APP_TITLE = "Sistem Verifikasi Ijazah"

RPC_URL = "http://127.0.0.1:8545"
EXPECTED_CHAIN_ID = 31337

CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

ABI_PATH = (
    Path(__file__).parent
    / "artifacts"
    / "contracts"
    / "SistemVerifikasiIjazah.sol"
    / "SistemVerifikasiIjazah.json"
)