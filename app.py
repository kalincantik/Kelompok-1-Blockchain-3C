import json
import hashlib
from pathlib import Path
from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape
from urllib.parse import quote

import streamlit as st
import streamlit.components.v2 as components
from web3 import Web3

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)

# QR Code is optional. Install with: pip install qrcode[pil]
try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False


# =========================================================
# 1. KONFIGURASI APLIKASI
# =========================================================

st.set_page_config(
    page_title="Verifikasi Ijazah Akademik",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

RPC_URL = "http://127.0.0.1:8545"
PROJECT_DIR = Path(__file__).parent
DEPLOYMENT_PATH = PROJECT_DIR / "deployment.json"
ARTIFACT_PATH = (
    PROJECT_DIR
    / "artifacts"
    / "contracts"
    / "SistemVerifikasiIjazah.sol"
    / "SistemVerifikasiIjazah.json"
)

NAVY = "#081426"
NAVY_2 = "#0D1D33"
PANEL = "#112640"
CYAN = "#20C7E8"
CYAN_LIGHT = "#8BEAFF"
TEXT = "#EAF4FF"
MUTED = "#9CB2C9"
GREEN = "#20C997"
RED = "#FF647C"
GOLD = "#F4C76B"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, {NAVY} 0%, #0B1B30 55%, #102641 100%);
        color: {TEXT};
    }}
    [data-testid="stSidebar"] {{
        background: #071326;
        border-right: 1px solid #1C3855;
    }}
    [data-testid="stSidebar"] * {{ color: {TEXT}; }}
    [data-testid="stSidebar"] [role="radiogroup"] {{
        gap: 5px;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] label {{
        background: transparent;
        border: 1px solid transparent;
        border-radius: 9px;
        padding: 7px 10px;
        transition: background .15s ease, border .15s ease;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
        background: #102943;
        border-color: #214361;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{
        background: linear-gradient(90deg, #123B55, #102943);
        border-color: #1D7894;
    }}
    [data-testid="stSidebar"] [role="radiogroup"] label p {{
        font-size: 0.88rem;
        font-weight: 600;
    }}
    h1, h2, h3, h4 {{ color: {TEXT} !important; }}
    p, label, .stMarkdown {{ color: {TEXT}; }}
    [data-testid="stMetric"] {{
        background: linear-gradient(145deg, #122A45, #0D2037);
        border: 1px solid #214361;
        padding: 17px 18px;
        border-radius: 14px;
    }}
    [data-testid="stMetricLabel"] {{ color: {MUTED} !important; }}
    [data-testid="stMetricValue"] {{ color: {CYAN_LIGHT} !important; }}
    div.stButton > button, div.stFormSubmitButton > button {{
        background: {CYAN};
        color: #041323;
        border: 0;
        border-radius: 9px;
        font-weight: 700;
        min-height: 42px;
    }}
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {{
        background: {CYAN_LIGHT};
        color: #041323;
        border: 0;
    }}
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextArea"] textarea {{
        background: #0B1D32;
        color: {TEXT};
        border: 1px solid #31516F;
        border-radius: 8px;
    }}
    [data-testid="stFileUploader"] {{
        background: #0D2037;
        border: 1px dashed #31516F;
        border-radius: 10px;
        padding: 8px;
    }}
    [data-testid="stDataFrame"] {{
        border: 1px solid #24445F;
        border-radius: 10px;
    }}
    hr {{ border-color: #24445F !important; }}
    .hero {{
        background: linear-gradient(110deg, #102B48, #0D2037);
        border: 1px solid #24506D;
        border-radius: 18px;
        padding: 24px 26px;
        margin-bottom: 18px;
    }}
    .hero-kicker {{
        color: {CYAN};
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }}
    .hero-title {{
        color: {TEXT};
        font-size: 1.85rem;
        font-weight: 800;
        margin: 5px 0;
    }}
    .hero-sub {{
        color: {MUTED};
        margin: 0;
    }}
    .info-card {{
        background: #102640;
        border: 1px solid #24445F;
        border-radius: 13px;
        padding: 16px;
        min-height: 95px;
    }}
    .small-label {{ color: {MUTED}; font-size: 0.82rem; }}
    .small-value {{ color: {CYAN_LIGHT}; font-size: 1.05rem; font-weight: 700; }}
    .status-pill {{
        display: inline-block;
        padding: 5px 11px;
        border-radius: 20px;
        background: #123E3B;
        color: #7CF0C6;
        font-size: 0.82rem;
        font-weight: 700;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def hero(title, subtitle, kicker="BLOCKCHAIN ACADEMIC CREDENTIAL"):
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-kicker">{kicker}</div>
          <div class="hero-title">{title}</div>
          <p class="hero-sub">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(label, value):
    st.markdown(
        f"""
        <div class="info-card">
          <div class="small-label">{label}</div>
          <div class="small-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 2. KOMPONEN METAMASK (TETAP DIPERTAHANKAN)
# =========================================================

WALLET_HTML = """
<div>
    <button id="connect-wallet" type="button">Hubungkan MetaMask</button>
    <p id="wallet-status">Wallet belum terhubung.</p>
</div>
"""

WALLET_CSS = """
button {
    padding: 0.7rem 1rem;
    border: none;
    border-radius: 8px;
    background: var(--st-primary-color);
    color: white;
    font-weight: 600;
    cursor: pointer;
}
p {
    color: var(--st-text-color);
    overflow-wrap: anywhere;
}
"""

WALLET_JS = """
export default function(component) {
    const { parentElement, setStateValue } = component;
    const button = parentElement.querySelector("#connect-wallet");
    const status = parentElement.querySelector("#wallet-status");
    let mounted = true;
    const HARDHAT_CHAIN_ID = "0x7a69";

    async function readWallet() {
        if (!window.ethereum) return;
        const accounts = await window.ethereum.request({method: "eth_accounts"});
        const chainId = await window.ethereum.request({method: "eth_chainId"});
        if (!mounted) return;
        const connected = Boolean(accounts && accounts.length > 0);
        const address = connected ? accounts[0] : "";
        setStateValue("wallet", {address, chainId, connected});
        status.textContent = connected
            ? "Wallet terhubung: " + address + " | Chain ID: " + chainId
            : "Wallet belum terhubung.";
    }

    async function switchToHardhat() {
        try {
            await window.ethereum.request({
                method: "wallet_switchEthereumChain",
                params: [{chainId: HARDHAT_CHAIN_ID}]
            });
        } catch (error) {
            if (error.code === 4902) {
                await window.ethereum.request({
                    method: "wallet_addEthereumChain",
                    params: [{
                        chainId: HARDHAT_CHAIN_ID,
                        chainName: "Verifikasi Ijazah",
                        nativeCurrency: {name: "Ether", symbol: "ETH", decimals: 18},
                        rpcUrls: ["http://127.0.0.1:8545"]
                    }]
                });
            } else {
                throw error;
            }
        }
    }

    async function connectWallet() {
        if (!window.ethereum) {
            status.textContent = "MetaMask tidak ditemukan.";
            return;
        }
        try {
            status.textContent = "Meminta MetaMask berpindah ke jaringan Hardhat...";
            await switchToHardhat();
            await window.ethereum.request({method: "eth_requestAccounts"});
            await readWallet();
        } catch (error) {
            status.textContent = "Koneksi gagal: " + error.message;
        }
    }

    function onAccountsChanged() { readWallet().catch(() => {}); }
    function onChainChanged() { readWallet().catch(() => {}); }

    button.addEventListener("click", connectWallet);
    if (window.ethereum) {
        window.ethereum.on("accountsChanged", onAccountsChanged);
        window.ethereum.on("chainChanged", onChainChanged);
        readWallet().catch(() => {});
    }

    return () => {
        mounted = false;
        button.removeEventListener("click", connectWallet);
        if (window.ethereum && window.ethereum.removeListener) {
            window.ethereum.removeListener("accountsChanged", onAccountsChanged);
            window.ethereum.removeListener("chainChanged", onChainChanged);
        }
    };
}
"""

wallet_component = components.component(
    name="ijazah_metamask_wallet",
    html=WALLET_HTML,
    css=WALLET_CSS,
    js=WALLET_JS,
)


# =========================================================
# 3. KONEKSI WEB3 DAN SMART CONTRACT
# =========================================================

w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 5}))

if not w3.is_connected():
    st.error(
        "Tidak dapat terhubung ke Hardhat Network. "
        "Jalankan Hardhat Node terlebih dahulu dengan `npx hardhat node`."
    )
    st.stop()

if not DEPLOYMENT_PATH.exists():
    st.error("deployment.json tidak ditemukan. Periksa hasil deployment kontrak.")
    st.stop()

try:
    with open(DEPLOYMENT_PATH, "r", encoding="utf-8") as file:
        deployment_data = json.load(file)
    CONTRACT_ADDRESS = Web3.to_checksum_address(deployment_data["address"])
except Exception as error:
    st.error(f"Alamat kontrak pada deployment.json tidak valid: {error}")
    st.stop()

if not ARTIFACT_PATH.exists():
    st.error(
        "Artifact ABI tidak ditemukan pada:\n"
        f"{ARTIFACT_PATH}\n"
        "Pastikan nama folder dan file artifact sesuai dengan hasil compile."
    )
    st.stop()

try:
    with open(ARTIFACT_PATH, "r", encoding="utf-8") as file:
        contract_artifact = json.load(file)
    CONTRACT_ABI = contract_artifact["abi"]
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    ADMIN_ADDRESS = Web3.to_checksum_address(contract.functions.admin().call())
except Exception as error:
    st.error(f"Gagal memuat Smart Contract: {error}")
    st.stop()

if "riwayat_verifikasi" not in st.session_state:
    st.session_state.riwayat_verifikasi = []
if "transaksi_sesi" not in st.session_state:
    st.session_state.transaksi_sesi = []
if "hash_pdf_sesi" not in st.session_state:
    st.session_state.hash_pdf_sesi = {}


# =========================================================
# 4. HELPER FUNCTION
# =========================================================

def get_status(nomor):
    return contract.functions.statusIjazah(nomor).call()


def get_ijazah(nomor):
    return contract.functions.lihatDataIjazah(nomor).call()


def get_issued_certificates():
    """Membaca event penerbitan dari node blockchain untuk membangun daftar."""
    try:
        logs = contract.events.IjazahDitambahkan.get_logs(
            from_block=0,
            to_block="latest",
        )
        certificates = []
        seen = set()
        for log in logs:
            args = log["args"]
            nomor = args["nomorIjazah"]
            if nomor in seen:
                continue
            seen.add(nomor)
            try:
                data = get_ijazah(nomor)
                terdaftar, dicabut, valid = get_status(nomor)
                certificates.append({
                    "Token ID": int(args["tokenId"]),
                    "Nomor Ijazah": data[3],
                    "Nama": data[0],
                    "NIM": data[1],
                    "Program Studi": data[2],
                    "Tahun Lulus": int(data[4]),
                    "Status": (
                        "Dicabut" if dicabut else
                        "Valid" if valid else
                        "Tidak Valid"
                    ),
                })
            except Exception:
                continue
        certificates.sort(key=lambda item: item["Token ID"])
        return certificates, None
    except Exception as error:
        return [], str(error)


def add_transaction_record(label, tx_hash, receipt):
    st.session_state.transaksi_sesi.insert(0, {
        "Waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "Aktivitas": label,
        "Transaction Hash": tx_hash.hex(),
        "Block": receipt.blockNumber,
        "Status": "Berhasil" if receipt.status == 1 else "Gagal",
    })


def show_tx_result(tx_hash, receipt, success_message):
    if receipt.status == 1:
        st.success(success_message)
        st.write("Transaction Hash:")
        st.code(tx_hash.hex())
        st.write(f"Block Number: **{receipt.blockNumber}**")
        st.caption("Transaksi telah dikonfirmasi oleh Hardhat Network.")
    else:
        st.error("Transaksi gagal diproses oleh blockchain.")


def build_diploma_pdf(data, token_id, owner):
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "JudulIjazah",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=23,
        spaceAfter=12,
        textColor=colors.HexColor("#183B5B"),
    )
    subtitle_style = ParagraphStyle(
        "SubjudulIjazah",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        leading=15,
    )
    elements = [
        Paragraph("DOKUMEN DATA IJAZAH AKADEMIK", title_style),
        Paragraph(
            "Dokumen informasi yang diambil dari Sistem Verifikasi "
            "Ijazah berbasis blockchain",
            subtitle_style,
        ),
        Spacer(1, 1 * cm),
    ]
    rows = [
        ["Keterangan", "Data"],
        ["Nama Lengkap", str(data[0])],
        ["NIM", str(data[1])],
        ["Program Studi", str(data[2])],
        ["Nomor Ijazah", str(data[3])],
        ["Tahun Lulus", str(data[4])],
        ["Token ID NFT", str(token_id)],
        ["Pemilik NFT", str(owner)],
        ["Alamat Penerbit/Admin", str(ADMIN_ADDRESS)],
        ["Alamat Smart Contract", str(CONTRACT_ADDRESS)],
        ["Waktu Dokumen Dibuat", datetime.now().strftime("%d-%m-%Y %H:%M:%S")],
    ]
    table_data = [
        [Paragraph(escape(str(cell)), styles["BodyText"]) for cell in row]
        for row in rows
    ]
    table = Table(table_data, colWidths=[5 * cm, 11 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#24476B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#EAF0F6")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.7 * cm))
    elements.append(Paragraph(
        "Catatan: Dokumen ini merupakan keluaran aplikasi untuk menampilkan "
        "data ijazah yang tercatat pada smart contract. Dokumen ini bukan "
        "pengganti ijazah resmi yang diterbitkan oleh perguruan tinggi.",
        styles["Italic"],
    ))
    document.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


# =========================================================
# 5. STATUS WALLET DAN SIDEBAR
# =========================================================

wallet_result = wallet_component(
    key="ijazah_metamask",
    default={
        "wallet": {
            "address": "",
            "chainId": "",
            "connected": False,
        }
    },
    on_wallet_change=lambda: None,
)

wallet = wallet_result.wallet
wallet_connected = bool(
    wallet
    and wallet.get("connected")
    and wallet.get("address")
)

wallet_address = ""
wallet_chain_id = None
network_ok = False
is_admin = False

if wallet_connected:
    try:
        wallet_address = Web3.to_checksum_address(wallet["address"])
        wallet_chain_id = int(str(wallet.get("chainId", "")), 16)
        network_ok = wallet_chain_id == int(w3.eth.chain_id)
        is_admin = network_ok and wallet_address == ADMIN_ADDRESS
    except (ValueError, TypeError):
        wallet_connected = False

with st.sidebar:
    st.markdown(
        """
        <div style="
            padding: 10px 8px 18px 8px;
            display:flex;
            align-items:center;
            gap:12px;
        ">
          <div style="
              width:42px;height:42px;border-radius:13px;
              background:linear-gradient(145deg,#20C7E8,#087FA8);
              display:flex;align-items:center;justify-content:center;
              color:#061629;font-size:23px;font-weight:900;
              box-shadow:0 5px 18px rgba(32,199,232,.18);
          ">🎓</div>
          <div>
            <div style="font-size:16px;font-weight:800;letter-spacing:.5px;color:#EAF4FF;">
              IJAZAH CHAIN
            </div>
            <div style="font-size:10px;letter-spacing:1.3px;color:#8FAAC4;">
              ACADEMIC PLATFORM
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="font-size:10px;font-weight:800;letter-spacing:1.8px;'
        'color:#6F8DAA;padding:5px 10px 8px 10px;">MENU UTAMA</div>',
        unsafe_allow_html=True,
    )

    nav_items = [
        "Dashboard",
        "Certificate List",
        "Issue Certificate",
        "Certificate Detail",
        "Verify Certificate",
        "Wallet & Transaction",
        "Cabut Ijazah",
        "Informasi NFT",
        "Cetak Ijazah",
        "Riwayat Verifikasi",
    ]
    nav_icons = {
        "Dashboard": "⌂",
        "Certificate List": "▤",
        "Issue Certificate": "＋",
        "Certificate Detail": "▣",
        "Verify Certificate": "✓",
        "Wallet & Transaction": "◈",
        "Cabut Ijazah": "⊘",
        "Informasi NFT": "◇",
        "Cetak Ijazah": "▧",
        "Riwayat Verifikasi": "◷",
    }

    page = st.radio(
        "Navigasi",
        nav_items,
        format_func=lambda item: f"{nav_icons.get(item, '•')}   {item}",
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div style="
            margin:18px 0 10px 0;padding:13px 13px 12px 13px;
            border:1px solid #1F405D;border-radius:12px;
            background:linear-gradient(145deg,#102640,#0B1B30);
        ">
          <div style="font-size:10px;font-weight:800;letter-spacing:1.5px;color:#6F8DAA;">
            NETWORK STATUS
          </div>
          <div style="margin-top:9px;color:#76EAC3;font-size:12px;font-weight:700;">
            ● &nbsp; BLOCKCHAIN CONNECTED
          </div>
          <div style="margin-top:9px;font-size:11px;color:#A7BCD0;line-height:1.8;">
            Chain ID &nbsp; <b style="color:#EAF4FF;">{chain_id}</b><br>
            Latest Block &nbsp; <b style="color:#EAF4FF;">{block_number}</b><br>
            Network &nbsp; <b style="color:#EAF4FF;">Hardhat Local</b>
          </div>
        </div>
        """.format(
            chain_id=w3.eth.chain_id,
            block_number=w3.eth.block_number,
        ),
        unsafe_allow_html=True,
    )


# =========================================================
# 6. DASHBOARD
# =========================================================

if page == "Dashboard":
    hero(
        "Dashboard",
        "Pusat informasi penerbitan dan verifikasi ijazah akademik.",
    )

    certificates, event_error = get_issued_certificates()
    total_ijazah = len(certificates)
    total_valid = sum(1 for item in certificates if item["Status"] == "Valid")
    total_dicabut = sum(1 for item in certificates if item["Status"] == "Dicabut")
    total_verifikasi = len(st.session_state.riwayat_verifikasi)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Ijazah", total_ijazah)
    c2.metric("Ijazah Valid", total_valid)
    c3.metric("Ijazah Dicabut", total_dicabut)
    c4.metric("Total Verifikasi Sesi", total_verifikasi)

    st.markdown("### Ringkasan Blockchain")
    left, right = st.columns(2)
    with left:
        info_card("Status Koneksi", "Terhubung" if w3.is_connected() else "Terputus")
        st.write("")
        info_card("Chain ID", str(w3.eth.chain_id))
    with right:
        info_card("Block Terbaru", str(w3.eth.block_number))
        st.write("")
        info_card("Smart Contract", CONTRACT_ADDRESS[:12] + "..." + CONTRACT_ADDRESS[-8:])

    st.markdown("### Aktivitas Verifikasi Terbaru")
    if st.session_state.riwayat_verifikasi:
        st.dataframe(
            st.session_state.riwayat_verifikasi[:5],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Belum ada verifikasi pada sesi aplikasi ini.")

    if event_error:
        st.warning(
            "Daftar ijazah belum dapat dibaca dari event kontrak. "
            f"Detail: {event_error}"
        )


# =========================================================
# 7. CERTIFICATE LIST
# =========================================================

elif page == "Certificate List":
    hero(
        "Certificate List",
        "Daftar ijazah yang diterbitkan dan tercatat pada blockchain.",
    )
    certificates, event_error = get_issued_certificates()

    if event_error:
        st.error(f"Gagal membaca event penerbitan: {event_error}")
        st.caption(
            "Pastikan node Hardhat yang aktif adalah node tempat kontrak ini "
            "di-deploy dan ABI sesuai dengan kontrak."
        )
    elif certificates:
        search = st.text_input(
            "Cari berdasarkan nama, NIM, atau nomor ijazah",
            key="search_certificate_list",
        )
        filtered = [
            item for item in certificates
            if search.lower() in (
                item["Nama"] + " " + item["NIM"] + " " + item["Nomor Ijazah"]
            ).lower()
        ] if search else certificates

        st.caption(f"Menampilkan {len(filtered)} dari {len(certificates)} ijazah.")
        st.dataframe(filtered, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada ijazah yang diterbitkan pada blockchain.")


# =========================================================
# 8. ISSUE CERTIFICATE
# =========================================================

elif page == "Issue Certificate":
    hero(
        "Issue Certificate",
        "Terbitkan ijazah baru dan mint NFT kepada wallet pemilik.",
    )

    if not is_admin:
        st.warning(
            "Fitur penerbitan hanya tersedia jika MetaMask terhubung "
            "menggunakan wallet admin pada jaringan Hardhat."
        )

    with st.form("form_tambah_ijazah"):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Lengkap")
            nim = st.text_input("NIM")
            prodi = st.text_input("Program Studi")
        with col2:
            nomor = st.text_input("Nomor Ijazah")
            tahun = st.number_input(
                "Tahun Lulus",
                min_value=1,
                max_value=2100,
                value=2026,
                step=1,
            )
            pemilik = st.text_input("Alamat Wallet Pemilik NFT")

        uploaded_pdf = st.file_uploader(
            "Unggah PDF ijazah (opsional, untuk menghitung SHA-256)",
            type=["pdf"],
            key="upload_issue_pdf",
        )
        submit_tambah = st.form_submit_button(
            "Terbitkan Ijazah",
            type="primary",
            use_container_width=True,
        )

    if uploaded_pdf is not None:
        pdf_bytes = uploaded_pdf.getvalue()
        pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()
        st.success("File PDF berhasil dibaca dan hash SHA-256 berhasil dihitung.")
        st.code(pdf_hash)
        st.caption(
            "Penting: kontrak Solidity saat ini belum memiliki field untuk "
            "menyimpan hash. Hash ini hanya ditampilkan di aplikasi dan belum "
            "disimpan permanen di blockchain."
        )
        st.session_state.hash_pdf_sesi[nomor.strip() or "belum_diisi"] = pdf_hash

    if submit_tambah:
        if not is_admin:
            st.error("Hanya wallet admin yang dapat menerbitkan ijazah.")
        elif not all([nama.strip(), nim.strip(), prodi.strip(), nomor.strip(), pemilik.strip()]):
            st.error("Semua data wajib diisi.")
        elif not Web3.is_address(pemilik):
            st.error("Alamat wallet pemilik tidak valid.")
        elif int(tahun) < 1:
            st.error("Tahun lulus tidak valid.")
        else:
            try:
                pemilik_checksum = Web3.to_checksum_address(pemilik.strip())
                tx_hash = contract.functions.tambahIjazah(
                    nama.strip(),
                    nim.strip(),
                    prodi.strip(),
                    nomor.strip(),
                    int(tahun),
                    pemilik_checksum,
                ).transact({"from": ADMIN_ADDRESS})
                st.info("Transaksi dikirim. Menunggu konfirmasi blockchain...")
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                add_transaction_record("Penerbitan Ijazah", tx_hash, receipt)
                if receipt.status == 1:
                    token_id = contract.functions.getTokenId(nomor.strip()).call()
                    show_tx_result(tx_hash, receipt, "Ijazah berhasil diterbitkan!")
                    st.metric("Token ID NFT", token_id)
                else:
                    st.error("Transaksi penerbitan gagal.")
            except Exception as error:
                st.error("Gagal menerbitkan ijazah.")
                st.code(str(error))


# =========================================================
# 9. CERTIFICATE DETAIL
# =========================================================

elif page == "Certificate Detail":
    hero(
        "Certificate Detail",
        "Lihat detail data, status keabsahan, dan informasi NFT ijazah.",
    )
    nomor_detail = st.text_input("Masukkan Nomor Ijazah", key="nomor_detail")

    if st.button("Tampilkan Detail", type="primary"):
        if not nomor_detail.strip():
            st.warning("Nomor ijazah wajib diisi.")
        else:
            try:
                nomor_bersih = nomor_detail.strip()
                data = get_ijazah(nomor_bersih)
                terdaftar, dicabut, valid = get_status(nomor_bersih)
                token_id = contract.functions.getTokenId(nomor_bersih).call()
                owner = contract.functions.getOwner(token_id).call()

                st.markdown("### Informasi Ijazah")
                a, b = st.columns(2)
                with a:
                    st.write("**Nama Lengkap**")
                    st.write(data[0])
                    st.write("**NIM**")
                    st.write(data[1])
                    st.write("**Program Studi**")
                    st.write(data[2])
                with b:
                    st.write("**Nomor Ijazah**")
                    st.write(data[3])
                    st.write("**Tahun Lulus**")
                    st.write(data[4])
                    st.write("**Token ID NFT**")
                    st.write(token_id)

                st.markdown("### Informasi Blockchain")
                st.write("**Alamat Penerbit/Admin:**")
                st.code(ADMIN_ADDRESS)
                st.write("**Pemilik NFT:**")
                st.code(owner)
                st.write("**Alamat Smart Contract:**")
                st.code(CONTRACT_ADDRESS)

                if not terdaftar:
                    st.error("Ijazah tidak ditemukan.")
                elif dicabut:
                    st.error("Status: SUDAH DICABUT")
                elif valid:
                    st.success("Status: AKTIF / VALID")
                else:
                    st.warning("Status: TIDAK VALID")

                if nomor_bersih in st.session_state.hash_pdf_sesi:
                    st.caption("Hash PDF pada sesi aplikasi:")
                    st.code(st.session_state.hash_pdf_sesi[nomor_bersih])
            except Exception as error:
                st.error("Data ijazah tidak ditemukan atau gagal dibaca.")
                st.caption(str(error))


# =========================================================
# 10. VERIFY CERTIFICATE
# =========================================================

elif page == "Verify Certificate":
    hero(
        "Verify Certificate",
        "Periksa keaslian ijazah berdasarkan nomor ijazah yang tercatat di blockchain.",
    )

    query_verify = st.query_params.get("verify", "")
    nomor_cek = st.text_input(
        "Nomor Ijazah",
        value=query_verify,
        key="nomor_verifikasi",
        placeholder="Contoh: IJZ-001",
    )

    if st.button("Verifikasi Ijazah", type="primary", use_container_width=True):
        if not nomor_cek.strip():
            st.warning("Nomor ijazah wajib diisi.")
        else:
            try:
                nomor_diperiksa = nomor_cek.strip()
                valid = contract.functions.cekKeaslianData(nomor_diperiksa).call()
                terdaftar, dicabut, status_valid = get_status(nomor_diperiksa)

                if not terdaftar:
                    hasil = "Tidak ditemukan"
                    st.error("IJAZAH TIDAK DITEMUKAN")
                elif dicabut:
                    hasil = "Sudah dicabut"
                    st.error("IJAZAH SUDAH DICABUT")
                elif valid and status_valid:
                    hasil = "Valid"
                    st.success("IJAZAH VALID DAN TERCATAT DI BLOCKCHAIN")
                else:
                    hasil = "Tidak valid"
                    st.warning("IJAZAH TIDAK VALID")

                st.session_state.riwayat_verifikasi.insert(0, {
                    "Waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "Nomor Ijazah": nomor_diperiksa,
                    "Hasil": hasil,
                    "Block": w3.eth.block_number,
                })
            except Exception as error:
                st.error("Verifikasi gagal.")
                st.caption(str(error))

    st.divider()
    st.markdown("### Verifikasi menggunakan QR Code")
    st.caption(
        "QR Code dapat dibuat dari halaman Certificate Detail atau Issue Certificate "
        "setelah nomor ijazah tersedia."
    )
    nomor_qr = st.text_input("Nomor ijazah untuk membuat QR Code", key="nomor_qr")
    if st.button("Buat QR Code"):
        if not nomor_qr.strip():
            st.warning("Masukkan nomor ijazah terlebih dahulu.")
        elif not QR_AVAILABLE:
            st.warning("Library QR Code belum terpasang. Jalankan: pip install qrcode[pil]")
        else:
            try:
                # URL lokal ini akan membuka aplikasi dengan nomor terisi pada halaman verifikasi.
                verify_url = (
                    "http://localhost:8501/?verify=" + quote(nomor_qr.strip())
                )
                qr_image = qrcode.make(verify_url)

                qr_buffer = BytesIO()
                qr_image.save(qr_buffer, format="PNG")
                qr_buffer.seek(0)

                st.image(
                    qr_buffer.getvalue(),
                    caption="QR Code menuju halaman verifikasi lokal",
                    width=250
                )
                st.code(verify_url)
                st.caption(
                    "URL localhost hanya dapat dibuka pada komputer yang menjalankan "
                    "aplikasi. Untuk akses publik, ganti dengan domain aplikasi yang "
                    "sudah dipublikasikan."
                )
            except Exception as error:
                st.error(f"Gagal membuat QR Code: {error}")


# =========================================================
# 11. WALLET & TRANSACTION
# =========================================================

elif page == "Wallet & Transaction":
    hero(
        "Wallet & Transaction",
        "Informasi koneksi MetaMask, jaringan, admin, dan transaksi aplikasi.",
    )

    st.markdown("### Hubungkan Wallet")
    wallet_result = wallet_component(
        key="ijazah_metamask_wallet_page",
        default={
            "wallet": {"address": "", "chainId": "", "connected": False}
        },
        on_wallet_change=lambda: None,
    )
    wallet_page = wallet_result.wallet
    connected_page = bool(
        wallet_page
        and wallet_page.get("connected")
        and wallet_page.get("address")
    )

    if connected_page:
        try:
            address_page = Web3.to_checksum_address(wallet_page["address"])
            chain_page = int(str(wallet_page.get("chainId", "")), 16)
            st.success("Wallet MetaMask terhubung.")
            st.code(address_page)
            st.write(f"Chain ID MetaMask: **{chain_page}**")
            st.write(f"Chain ID Hardhat: **{w3.eth.chain_id}**")
            if chain_page != w3.eth.chain_id:
                st.error("Jaringan MetaMask dan Hardhat belum sesuai.")
            elif address_page == ADMIN_ADDRESS:
                st.success("Wallet terhubung sebagai ADMIN.")
            else:
                st.warning("Wallet terhubung, tetapi bukan wallet admin.")
        except Exception as error:
            st.error(f"Gagal membaca informasi wallet: {error}")
    else:
        st.info("Wallet belum terhubung.")

    st.divider()
    st.markdown("### Informasi Jaringan")
    c1, c2, c3 = st.columns(3)
    c1.metric("Chain ID", w3.eth.chain_id)
    c2.metric("Block Terbaru", w3.eth.block_number)
    c3.metric("Status", "Connected")
    st.write("**Alamat Smart Contract**")
    st.code(CONTRACT_ADDRESS)
    st.write("**Alamat Admin Smart Contract**")
    st.code(ADMIN_ADDRESS)

    try:
        balance = w3.eth.get_balance(ADMIN_ADDRESS)
        st.metric("Saldo Admin", f"{float(w3.from_wei(balance, 'ether')):.6f} ETH")
    except Exception:
        st.info("Saldo admin tidak dapat dibaca.")

    st.divider()
    st.markdown("### Transaksi pada Sesi Aplikasi")
    if st.session_state.transaksi_sesi:
        st.dataframe(
            st.session_state.transaksi_sesi,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Belum ada transaksi yang dilakukan melalui sesi aplikasi ini.")

    st.warning(
        "Catatan integrasi: tombol MetaMask di atas menghubungkan dan memeriksa wallet. "
        "Transaksi Web3.py pada versi ini tetap ditandatangani akun admin yang tersedia "
        "pada node Hardhat, bukan langsung oleh MetaMask."
    )


# =========================================================
# 12. CABUT IJAZAH
# =========================================================

elif page == "Cabut Ijazah":
    hero(
        "Pencabutan Ijazah",
        "Ubah status keabsahan ijazah melalui transaksi Smart Contract.",
    )
    if not is_admin:
        st.warning("Pencabutan hanya dapat dilakukan oleh wallet admin.")

    with st.form("form_cabut_ijazah"):
        nomor_cabut = st.text_input("Nomor Ijazah")
        alasan = st.text_area("Alasan Pencabutan")
        submit_cabut = st.form_submit_button(
            "Cabut Ijazah",
            type="primary",
            use_container_width=True,
        )

    if submit_cabut:
        if not is_admin:
            st.error("Hanya admin yang dapat mencabut ijazah.")
        elif not nomor_cabut.strip() or not alasan.strip():
            st.warning("Nomor ijazah dan alasan wajib diisi.")
        else:
            try:
                tx_hash = contract.functions.cabutIjazah(
                    nomor_cabut.strip(),
                    alasan.strip(),
                ).transact({"from": ADMIN_ADDRESS})
                st.info("Transaksi dikirim. Menunggu konfirmasi...")
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                add_transaction_record("Pencabutan Ijazah", tx_hash, receipt)
                show_tx_result(tx_hash, receipt, "Ijazah berhasil dicabut.")
            except Exception as error:
                st.error("Gagal mencabut ijazah.")
                st.code(str(error))


# =========================================================
# 13. INFORMASI NFT
# =========================================================

elif page == "Informasi NFT":
    hero(
        "Informasi NFT",
        "Periksa Token ID dan wallet pemilik NFT ijazah.",
    )
    nomor_nft = st.text_input("Masukkan Nomor Ijazah", key="nomor_nft")
    if st.button("Cek Informasi NFT", type="primary"):
        if not nomor_nft.strip():
            st.warning("Nomor ijazah wajib diisi.")
        else:
            try:
                token_id = contract.functions.getTokenId(nomor_nft.strip()).call()
                owner = contract.functions.getOwner(token_id).call()
                st.metric("Token ID", token_id)
                st.write("**Pemilik NFT:**")
                st.code(owner)
                st.write("**Alamat Smart Contract:**")
                st.code(CONTRACT_ADDRESS)
            except Exception as error:
                st.error("NFT tidak ditemukan.")
                st.caption(str(error))


# =========================================================
# 14. CETAK IJAZAH
# =========================================================

elif page == "Cetak Ijazah":
    hero(
        "Cetak Ijazah",
        "Buat dokumen PDF berdasarkan data ijazah yang tersimpan di Smart Contract.",
    )
    nomor_cetak = st.text_input("Masukkan Nomor Ijazah", key="nomor_cetak")

    if st.button("Buat Dokumen Ijazah", type="primary"):
        if not nomor_cetak.strip():
            st.warning("Nomor ijazah wajib diisi.")
        else:
            try:
                nomor_bersih = nomor_cetak.strip()
                terdaftar, dicabut, valid = get_status(nomor_bersih)
                if not terdaftar:
                    st.error("Ijazah tidak ditemukan di blockchain.")
                elif dicabut or not valid:
                    st.error("Ijazah sudah dicabut atau tidak valid sehingga tidak dapat dicetak.")
                else:
                    # Fungsi cetakIjazah pada kontrak memvalidasi status ijazah.
                    contract.functions.cetakIjazah(nomor_bersih).call()
                    data = get_ijazah(nomor_bersih)
                    token_id = contract.functions.getTokenId(nomor_bersih).call()
                    owner = contract.functions.getOwner(token_id).call()
                    pdf_bytes = build_diploma_pdf(data, token_id, owner)
                    st.success("Dokumen ijazah berhasil dibuat.")
                    st.download_button(
                        label="Unduh Ijazah (PDF)",
                        data=pdf_bytes,
                        file_name=f"Ijazah_{nomor_bersih}.pdf",
                        mime="application/pdf",
                    )
            except Exception as error:
                st.error("Gagal membuat dokumen ijazah.")
                st.caption(str(error))


# =========================================================
# 15. RIWAYAT VERIFIKASI
# =========================================================

elif page == "Riwayat Verifikasi":
    hero(
        "Riwayat Verifikasi",
        "Catatan pemeriksaan ijazah selama sesi aplikasi Streamlit berlangsung.",
    )
    history = st.session_state.get("riwayat_verifikasi", [])
    if history:
        st.dataframe(history, use_container_width=True, hide_index=True)
        st.info(
            "Riwayat ini masih disimpan pada session_state Streamlit. "
            "Data dapat hilang saat sesi berakhir atau aplikasi dimulai ulang. "
            "Penyimpanan permanen melalui event blockchain bukan persyaratan "
            "modul praktikum ini."
        )
        if st.button("Hapus Riwayat Sesi"):
            st.session_state.riwayat_verifikasi = []
            st.rerun()
    else:
        st.info("Belum ada riwayat. Lakukan pemeriksaan melalui menu Verify Certificate.")


# =========================================================
# 16. FOOTER
# =========================================================

st.divider()
st.caption(
    "Sistem Verifikasi Ijazah Akademik | Web3.py • Hardhat • ERC-721 • Streamlit"
)
