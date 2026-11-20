// SPDX-License-Identifier: MIT
pragma solidity ^0.8.34;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SistemVerifikasiIjazah is ERC721 {

    // ==========================================
    // STRUCT DATA IJAZAH
    // ==========================================

    struct Ijazah {
        string nama;
        string nim;
        string prodi;
        string nomorIjazah;
        uint256 tahunLulus;
    }

    // ==========================================
    // DATA IJAZAH
    // ==========================================

    // Menyimpan data ijazah berdasarkan nomor ijazah
    mapping(string => Ijazah) public dataIjazah;

    // Menghubungkan Token ID dengan data ijazah
    mapping(uint256 => Ijazah) public ijazahByTokenId;

    // Menghubungkan nomor ijazah dengan Token ID
    mapping(string => uint256) public tokenIdIjazah;

    // Status pencabutan ijazah berdasarkan nomor ijazah.
    // false = belum dicabut, true = sudah dicabut.
    mapping(string => bool) public ijazahDicabut;

    // ==========================================
    // TOKEN ID
    // ==========================================

    // Token ID dimulai dari 1
    uint256 private nextTokenId = 1;

    // ==========================================
    // DATA PENGGUNA / ADMIN
    // ==========================================

    address public admin;

    // Dipertahankan dari contract awal.
    // Saat ini hanya admin yang otomatis terdaftar.
    mapping(address => bool) public penggunaTerdaftar;

    // ==========================================
    // EVENT
    // ==========================================

    event IjazahDitambahkan(
        string nomorIjazah,
        string nama,
        uint256 tokenId
    );

    event IjazahDiverifikasi(
        string nomorIjazah,
        bool status
    );

    event IjazahDicabut(
        string nomorIjazah,
        address dicabutOleh,
        string alasan
    );

    // ==========================================
    // MODIFIER HAK AKSES
    // ==========================================

    // Hanya wallet admin yang boleh menjalankan fungsi
    // yang mengubah data penerbitan atau status ijazah.
    modifier onlyAdmin() {
        require(
            msg.sender == admin,
            "Hanya admin yang dapat mengakses"
        );
        _;
    }

    // ==========================================
    // CONSTRUCTOR ERC-721
    // ==========================================

    constructor()
        ERC721("Ijazah Akademik", "IJAZ")
    {
        // Wallet yang melakukan deployment menjadi admin.
        admin = msg.sender;

        // Admin otomatis terdaftar.
        penggunaTerdaftar[msg.sender] = true;
    }

    // ==========================================
    // FITUR 1:
    // TAMBAH IJAZAH + MINT NFT
    // HANYA ADMIN
    // ==========================================

    function tambahIjazah(
        string memory _nama,
        string memory _nim,
        string memory _prodi,
        string memory _nomorIjazah,
        uint256 _tahunLulus,
        address _pemilik
    )
        public
        onlyAdmin
        returns (uint256)
    {
        require(
            bytes(_nama).length > 0,
            "Nama wajib diisi"
        );

        require(
            bytes(_nim).length > 0,
            "NIM wajib diisi"
        );

        require(
            bytes(_prodi).length > 0,
            "Program studi wajib diisi"
        );

        require(
            bytes(_nomorIjazah).length > 0,
            "Nomor ijazah wajib diisi"
        );

        require(
            _tahunLulus > 0,
            "Tahun lulus tidak valid"
        );

        // Nomor ijazah tidak boleh digunakan kembali,
        // termasuk jika ijazah sebelumnya sudah dicabut.
        require(
            dataIjazah[_nomorIjazah].tahunLulus == 0,
            "Nomor ijazah sudah terdaftar"
        );

        require(
            _pemilik != address(0),
            "Alamat pemilik tidak valid"
        );

        uint256 tokenId = nextTokenId;
        nextTokenId++;

        // Menerbitkan NFT kepada alamat pemilik.
        _safeMint(_pemilik, tokenId);

        Ijazah memory dataBaru = Ijazah(
            _nama,
            _nim,
            _prodi,
            _nomorIjazah,
            _tahunLulus
        );

        dataIjazah[_nomorIjazah] = dataBaru;
        ijazahByTokenId[tokenId] = dataBaru;
        tokenIdIjazah[_nomorIjazah] = tokenId;

        // Status awal ijazah adalah aktif / belum dicabut.
        ijazahDicabut[_nomorIjazah] = false;

        emit IjazahDitambahkan(
            _nomorIjazah,
            _nama,
            tokenId
        );

        return tokenId;
    }

    // ==========================================
    // FITUR 2:
    // CABUT IJAZAH
    // HANYA ADMIN
    // ==========================================

    function cabutIjazah(
        string memory _nomorIjazah,
        string memory _alasan
    )
        public
        onlyAdmin
    {
        require(
            bytes(_nomorIjazah).length > 0,
            "Nomor ijazah wajib diisi"
        );

        require(
            dataIjazah[_nomorIjazah].tahunLulus != 0,
            "Data ijazah tidak ditemukan"
        );

        require(
            !ijazahDicabut[_nomorIjazah],
            "Ijazah sudah dicabut"
        );

        require(
            bytes(_alasan).length > 0,
            "Alasan pencabutan wajib diisi"
        );

        // Tidak menghapus data atau membakar NFT.
        // Hanya mengubah status keabsahan ijazah.
        ijazahDicabut[_nomorIjazah] = true;

        emit IjazahDicabut(
            _nomorIjazah,
            msg.sender,
            _alasan
        );
    }

    // ==========================================
    // FITUR 3:
    // VERIFIKASI IJAZAH
    // DAPAT DIPANGGIL PUBLIK
    // ==========================================

    function verifikasiIjazah(
        string memory _nomorIjazah
    )
        public
        returns (bool)
    {
        require(
            bytes(_nomorIjazah).length > 0,
            "Nomor ijazah wajib diisi"
        );

        bool valid =
            dataIjazah[_nomorIjazah].tahunLulus != 0
            && !ijazahDicabut[_nomorIjazah];

        emit IjazahDiverifikasi(
            _nomorIjazah,
            valid
        );

        return valid;
    }

    // ==========================================
    // FITUR 4:
    // CEK KEASLIAN DATA
    // VIEW / TANPA TRANSAKSI
    // ==========================================

    function cekKeaslianData(
        string memory _nomorIjazah
    )
        public
        view
        returns (bool)
    {
        require(
            bytes(_nomorIjazah).length > 0,
            "Nomor ijazah wajib diisi"
        );

        return (
            dataIjazah[_nomorIjazah].tahunLulus != 0
            && !ijazahDicabut[_nomorIjazah]
        );
    }

    // ==========================================
    // FITUR 5:
    // LIHAT DATA IJAZAH
    // DATA TETAP DAPAT DILIHAT MESKI DICABUT
    // ==========================================

    function lihatDataIjazah(
        string memory _nomorIjazah
    )
        public
        view
        returns (
            string memory nama,
            string memory nim,
            string memory prodi,
            string memory nomorIjazah,
            uint256 tahunLulus
        )
    {
        require(
            dataIjazah[_nomorIjazah].tahunLulus != 0,
            "Data ijazah tidak ditemukan"
        );

        Ijazah memory ijazah =
            dataIjazah[_nomorIjazah];

        return (
            ijazah.nama,
            ijazah.nim,
            ijazah.prodi,
            ijazah.nomorIjazah,
            ijazah.tahunLulus
        );
    }

    // ==========================================
    // FITUR 6:
    // LIHAT STATUS IJAZAH
    // ==========================================

    function statusIjazah(
        string memory _nomorIjazah
    )
        public
        view
        returns (bool terdaftar, bool dicabut, bool valid)
    {
        terdaftar =
            dataIjazah[_nomorIjazah].tahunLulus != 0;

        dicabut =
            terdaftar && ijazahDicabut[_nomorIjazah];

        valid =
            terdaftar && !dicabut;
    }

    // ==========================================
    // FITUR 7:
    // VALIDASI PENGGUNA
    // ==========================================

    function validasiPengguna(
        address _pengguna
    )
        public
        view
        returns (bool)
    {
        require(
            _pengguna != address(0),
            "Alamat pengguna tidak valid"
        );

        return penggunaTerdaftar[_pengguna];
    }

    // ==========================================
    // FITUR 8:
    // CETAK IJAZAH
    // HANYA JIKA IJAZAH MASIH VALID
    // ==========================================

    function cetakIjazah(
        string memory _nomorIjazah
    )
        public
        view
        returns (string memory)
    {
        require(
            dataIjazah[_nomorIjazah].tahunLulus != 0,
            "Data ijazah tidak ditemukan"
        );

        require(
            !ijazahDicabut[_nomorIjazah],
            "Ijazah sudah dicabut dan tidak valid"
        );

        return "Ijazah siap dicetak";
    }

    // ==========================================
    // FITUR NFT:
    // CEK PEMILIK NFT
    // ==========================================

    function getOwner(
        uint256 tokenId
    )
        public
        view
        returns (address)
    {
        return ownerOf(tokenId);
    }

    // ==========================================
    // FITUR NFT:
    // MENDAPATKAN TOKEN ID IJAZAH
    // ==========================================

    function getTokenId(
        string memory _nomorIjazah
    )
        public
        view
        returns (uint256)
    {
        require(
            tokenIdIjazah[_nomorIjazah] != 0,
            "Ijazah tidak ditemukan"
        );

        return tokenIdIjazah[_nomorIjazah];
    }
}