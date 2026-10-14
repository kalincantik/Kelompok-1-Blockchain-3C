// SPDX-License-Identifier: MIT
pragma solidity ^0.8.34;

contract SistemVerifikasiIjazah {

    // data ijazah

    struct Ijazah {
        string nama;
        string nim;
        string prodi;
        string nomorIjazah;
        uint256 tahunLulus;
    }

    mapping(string => Ijazah) public dataIjazah;


    // data pengguna

    address public admin;

    mapping(address => bool) public penggunaTerdaftar;

    // event

    event IjazahDitambahkan(
        string nomorIjazah,
        string nama
    );

    event IjazahDiverifikasi(
        string nomorIjazah,
        bool status
    );


    // CONSTRUCTOR

    constructor() {
        admin = msg.sender;
        penggunaTerdaftar[msg.sender] = true;
    }


    // tambah ijazah

    function tambahIjazah(
        string memory _nama,
        string memory _nim,
        string memory _prodi,
        string memory _nomorIjazah,
        uint256 _tahunLulus
    ) public {

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
            dataIjazah[_nomorIjazah].tahunLulus == 0,
            "Nomor ijazah sudah terdaftar"
        );

        dataIjazah[_nomorIjazah] = Ijazah(
            _nama,
            _nim,
            _prodi,
            _nomorIjazah,
            _tahunLulus
        );

        emit IjazahDitambahkan(
            _nomorIjazah,
            _nama
        );
    }


    // verifikasi ijazah

    function verifikasiIjazah(
        string memory _nomorIjazah
    ) public returns (bool) {

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


    // cek keaslian data

    function cekKeaslianData(
        string memory _nomorIjazah
    ) public view returns (bool) {

        require(
            bytes(_nomorIjazah).length > 0,
            "Nomor ijazah wajib diisi"
        );

        if (
            dataIjazah[_nomorIjazah].tahunLulus != 0
        ) {
            return true;
        }

        return false;
    }


    // lihat data ijazah

    function lihatDataIjazah(
        string memory _nomorIjazah
    ) public view returns (
        string memory nama,
        string memory nim,
        string memory prodi,
        string memory nomorIjazah,
        uint256 tahunLulus
    ) {

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


    // validasi pengguna

    function validasiPengguna(
        address _pengguna
    ) public view returns (bool) {

        require(
            _pengguna != address(0),
            "Alamat pengguna tidak valid"
        );

        return penggunaTerdaftar[_pengguna];
    }


    // cetak ijazah

    function cetakIjazah(
        string memory _nomorIjazah
    ) public view returns (
        string memory pesan
    ) {

        require(
            dataIjazah[_nomorIjazah].tahunLulus != 0,
            "Data ijazah tidak ditemukan"
        );

        return "Ijazah siap dicetak";
    }
}