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


    // ==========================================
    // TOKEN ID
    // ==========================================

    // Token ID dimulai dari 1
    uint256 private nextTokenId = 1;


    // ==========================================
    // DATA PENGGUNA
    // ==========================================

    address public admin;

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


    // ==========================================
    // CONSTRUCTOR ERC-721
    // ==========================================

    constructor()
        ERC721("Ijazah Akademik", "IJAZ")
    {
        admin = msg.sender;

        // Akun yang melakukan deploy otomatis terdaftar
        penggunaTerdaftar[msg.sender] = true;
    }


    // ==========================================
    // FITUR 1:
    // TAMBAH IJAZAH + MINT NFT
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
        returns (uint256)
    {

        // Validasi nama
        require(
            bytes(_nama).length > 0,
            "Nama wajib diisi"
        );

        // Validasi NIM
        require(
            bytes(_nim).length > 0,
            "NIM wajib diisi"
        );

        // Validasi program studi
        require(
            bytes(_prodi).length > 0,
            "Program studi wajib diisi"
        );

        // Validasi nomor ijazah
        require(
            bytes(_nomorIjazah).length > 0,
            "Nomor ijazah wajib diisi"
        );

        // Cek apakah nomor ijazah sudah ada
        require(
            dataIjazah[_nomorIjazah].tahunLulus == 0,
            "Nomor ijazah sudah terdaftar"
        );

        // Validasi alamat pemilik
        require(
            _pemilik != address(0),
            "Alamat pemilik tidak valid"
        );


        // ==========================================
        // AMBIL TOKEN ID
        // ==========================================

        uint256 tokenId = nextTokenId;


        // ==========================================
        // TOKEN ID BERIKUTNYA
        // ==========================================

        nextTokenId++;


        // ==========================================
        // MINT NFT
        // ==========================================

        _safeMint(_pemilik, tokenId);


        // ==========================================
        // SIMPAN DATA IJAZAH
        // ==========================================

        Ijazah memory dataBaru = Ijazah(
            _nama,
            _nim,
            _prodi,
            _nomorIjazah,
            _tahunLulus
        );

        dataIjazah[_nomorIjazah] = dataBaru;


        // ==========================================
        // HUBUNGKAN TOKEN ID DENGAN IJAZAH
        // ==========================================

        ijazahByTokenId[tokenId] = dataBaru;


        // ==========================================
        // HUBUNGKAN NOMOR IJAZAH DENGAN TOKEN ID
        // ==========================================

        tokenIdIjazah[_nomorIjazah] = tokenId;


        // ==========================================
        // EVENT
        // ==========================================

        emit IjazahDitambahkan(
            _nomorIjazah,
            _nama,
            tokenId
        );


        return tokenId;
    }


    // ==========================================
    // FITUR 2:
    // VERIFIKASI IJAZAH
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

        bool ditemukan =
            dataIjazah[_nomorIjazah].tahunLulus != 0;

        emit IjazahDiverifikasi(
            _nomorIjazah,
            ditemukan
        );

        return ditemukan;
    }


    // ==========================================
    // FITUR 3:
    // CEK KEASLIAN DATA
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
        );
    }


    // ==========================================
    // FITUR 4:
    // LIHAT DATA IJAZAH
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
    // FITUR 5:
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
    // FITUR 6:
    // CETAK IJAZAH
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