🎓 Sistem Verifikasi Ijazah Akademik Berbasis Blockchain

1. Deskripsi Proyek

Sistem Verifikasi Ijazah Akademik Berbasis Blockchain merupakan aplikasi yang dikembangkan untuk membantu proses penerbitan, pengelolaan, dan verifikasi keaslian ijazah akademik dengan memanfaatkan teknologi blockchain.

Aplikasi ini menggunakan Ethereum Smart Contract untuk menyimpan data ijazah sehingga informasi yang telah tercatat dapat diperiksa kembali melalui jaringan blockchain.

Tujuan utama pengembangan sistem ini adalah mengurangi risiko pemalsuan ijazah, meningkatkan transparansi data akademik, serta mempermudah proses verifikasi keaslian ijazah.

2. Tujuan Sistem

- Menerapkan teknologi blockchain dalam pengelolaan data ijazah akademik.
- Menyimpan informasi ijazah melalui Smart Contract.
- Mempermudah proses pemeriksaan keaslian ijazah.
- Menyediakan informasi kepemilikan ijazah berbasis NFT.
- Menampilkan informasi transaksi blockchain sebagai bukti aktivitas sistem.

3. Teknologi yang Digunakan

| Teknologi | Kegunaan |
| Python | Bahasa pemrograman utama |
| Streamlit | Framework antarmuka aplikasi |
| Solidity | Bahasa pemrograman Smart Contract |
| Web3.py | Penghubung Python dengan blockchain |
| Hardhat | Menjalankan jaringan blockchain lokal |
| Ethereum | Jaringan blockchain yang digunakan |
| MetaMask | Menghubungkan wallet pengguna |
| OpenZeppelin ERC-721 | Implementasi standar NFT |
| ReportLab | Membuat dokumen ijazah PDF |
| QR Code | Membuat kode untuk menuju halaman verifikasi |

4. Alur Kerja Sistem
Secara umum, sistem memiliki alur kerja sebagai berikut:

1. Menjalankan Blockchain: Hardhat digunakan untuk menjalankan jaringan blockchain lokal sebagai tempat Smart Contract beroperasi.
2. Menghubungkan Aplikasi: Aplikasi Streamlit terhubung ke jaringan blockchain melalui Web3.py menggunakan RPC URL, ABI, dan alamat kontrak.
3. Menghubungkan Wallet: Pengguna dapat menghubungkan MetaMask untuk melihat alamat wallet dan memeriksa kesesuaian jaringan.
4. Penerbitan Ijazah: Admin memasukkan data lulusan melalui halaman Issue Certificate.
5. Penyimpanan Data: Data ijazah dikirim ke Smart Contract dan dicatat melalui transaksi blockchain. Proses penerbitan juga menghasilkan token NFT.
6. Verifikasi Ijazah: Pengguna memasukkan nomor ijazah untuk memeriksa keberadaan dan status keaslian data pada Smart Contract.
7. Pengelolaan Ijazah: Admin dapat melihat detail ijazah, mencabut ijazah yang tidak berlaku, serta mencetak dokumen ijazah dalam format PDF.

5. Penjelasan Setiap Halaman

A. Dashboard
Dashboard merupakan halaman utama yang memberikan gambaran umum mengenai sistem.

Fungsi:
- Menampilkan ringkasan informasi ijazah.
- Menampilkan informasi koneksi blockchain.
- Menampilkan alamat Smart Contract.
- Memberikan akses menuju halaman pengelolaan dan verifikasi ijazah.

B. Certificate List
Halaman ini digunakan untuk melihat daftar ijazah yang telah diterbitkan.

Fungsi:
- Menampilkan data ijazah yang tercatat pada blockchain.
- Memudahkan admin melihat informasi ijazah.
- Menjadi akses awal untuk memeriksa data lulusan.

C. Issue Certificate
Halaman ini digunakan oleh admin untuk menerbitkan ijazah baru.

Data yang dimasukkan meliputi:
- Nama lulusan.
- Nomor Induk Mahasiswa (NIM).
- Program studi.
- Nomor ijazah.
- Tahun kelulusan.
- Alamat wallet pemilik ijazah.

Setelah data divalidasi, sistem mengirim transaksi ke Smart Contract untuk menyimpan data dan membuat token NFT.

D. Certificate Detail
Halaman ini digunakan untuk melihat informasi lengkap suatu ijazah berdasarkan nomor ijazah.

Informasi yang ditampilkan meliputi:
- Nama lulusan.
- NIM.
- Program studi.
- Nomor ijazah.
- Tahun kelulusan.
- Status ijazah.
- Informasi token dan pemilik NFT.

E. Verify Certificate
Halaman ini digunakan untuk memeriksa keaslian ijazah.

Fungsi:
- Memasukkan nomor ijazah yang ingin diperiksa.
- Memeriksa keberadaan data pada Smart Contract.
- Memeriksa apakah ijazah masih berlaku atau sudah dicabut.
- Menampilkan hasil verifikasi berupa status valid atau tidak valid.
- Menghasilkan QR Code yang mengarah ke halaman verifikasi.

F. Wallet & Transaction
Halaman ini berkaitan dengan koneksi wallet dan informasi transaksi blockchain.

Fungsi:
- Menghubungkan MetaMask dengan aplikasi.
- Menampilkan alamat wallet.
- Memeriksa kesesuaian jaringan blockchain.
- Menampilkan informasi transaksi yang dilakukan melalui aplikasi.

Catatan: Pada implementasi saat ini, transaksi Smart Contract dari backend Web3.py menggunakan akun admin Hardhat. Koneksi MetaMask digunakan untuk menghubungkan dan menampilkan informasi wallet, bukan sebagai penandatangan langsung transaksi backend.

G. Cabut Ijazah
Halaman ini digunakan admin untuk mencabut status berlaku suatu ijazah.

Fungsi:
- Memasukkan nomor ijazah.
- Memasukkan alasan pencabutan.
- Mengirim transaksi pencabutan ke Smart Contract.
- Menampilkan hasil transaksi pencabutan.

Ijazah yang telah dicabut akan memiliki status tidak valid ketika dilakukan pemeriksaan.

H. Informasi NFT
Halaman ini digunakan untuk melihat informasi token NFT yang berkaitan dengan ijazah.

Fungsi:
- Mencari token berdasarkan nomor ijazah.
- Menampilkan Token ID.
- Menampilkan alamat wallet pemilik NFT.

I. Cetak Ijazah
Halaman ini digunakan untuk menghasilkan dokumen ijazah dalam format PDF.

Fungsi:
- Mencari data ijazah berdasarkan nomor ijazah.
- Memeriksa status ijazah.
- Mengambil informasi lulusan dari Smart Contract.
- Menghasilkan dokumen PDF yang dapat diunduh.

J. Riwayat Verifikasi
Halaman ini digunakan untuk menampilkan aktivitas verifikasi yang dilakukan selama sesi aplikasi berjalan.

Informasi yang ditampilkan meliputi:
- Waktu verifikasi.
- Nomor ijazah.
- Hasil verifikasi.
- Nomor blok saat pemeriksaan.

Catatan: Riwayat verifikasi pada implementasi saat ini disimpan menggunakan session state Streamlit, sehingga belum menjadi penyimpanan permanen di blockchain.

6. Struktur Smart Contract
Smart Contract menggunakan Solidity dan standar ERC-721 dari OpenZeppelin.
Beberapa fungsi utama yang digunakan:

| Fungsi | Kegunaan |
| `tambahIjazah()` | Menerbitkan ijazah baru |
| `cekKeaslianData()` | Memeriksa keaslian data ijazah |
| `lihatDataIjazah()` | Mengambil informasi ijazah |
| `statusIjazah()` | Memeriksa status ijazah |
| `cabutIjazah()` | Mencabut status berlaku ijazah |
| `verifikasiIjazah()` | Melakukan verifikasi dan menghasilkan event |
| `getTokenId()` | Mengambil Token ID ijazah |
| `getOwner()` | Mengambil alamat pemilik NFT |
| `cetakIjazah()` | Memeriksa kesiapan ijazah untuk dicetak |

7. Cara Menjalankan Aplikasi
Persyaratan: 

Pastikan perangkat telah memiliki:
- Python.
- Node.js dan npm.
- MetaMask.
- Hardhat.
- Library Python dan dependensi proyek.

Langkah 1 — Clone Repository
git clone https://github.com/USERNAME/REPOSITORY.git

Masuk ke direktori proyek:
cd REPOSITORY

Langkah 2 — Install Library Python
pip install streamlit web3 reportlab "qrcode[pil]" pandas

Pastikan juga dependensi lain yang digunakan pada proyek sudah terpasang.

Langkah 3 — Install Dependensi Hardhat
npm install

Langkah 4 — Jalankan Hardhat Local Node
npx hardhat node

Hardhat akan menjalankan jaringan blockchain lokal dengan alamat RPC:
http://127.0.0.1:8545

Jaringan lokal menggunakan Chain ID `31337`.

Langkah 5 — Deploy Smart Contract
Apabila jaringan lokal baru dijalankan dan belum memiliki kontrak yang ter-deploy, lakukan proses deployment menggunakan konfigurasi dan script deployment proyek.

npx hardhat run scripts/deploy.js --network localhost

Pastikan alamat kontrak dan ABI yang digunakan aplikasi sesuai dengan hasil deployment terbaru.

Langkah 6 — Jalankan Streamlit
Buka terminal baru, kemudian jalankan:

streamlit run app.py

Aplikasi dapat diakses melalui browser pada alamat lokal yang ditampilkan oleh Streamlit.

8. Konfigurasi MetaMask
Untuk menghubungkan MetaMask dengan jaringan Hardhat lokal, gunakan konfigurasi berikut:

| Pengaturan | Nilai |
| Network Name | Hardhat Local |
| RPC URL | `http://127.0.0.1:8545` |
| Chain ID | `31337` |
| Currency Symbol | ETH |

Gunakan akun pengujian Hardhat untuk kebutuhan pengembangan lokal. Jangan menggunakan akun atau private key utama untuk pengujian.

9. Catatan Pengembangan
Beberapa hal yang perlu diperhatikan:
- Jaringan Hardhat lokal digunakan untuk kebutuhan pengembangan dan pengujian.
- Data blockchain lokal dapat berubah atau hilang ketika jaringan lokal dibuat ulang.
- Alamat kontrak harus diperbarui apabila dilakukan deployment ulang.
- Hash dokumen PDF dihitung pada sisi aplikasi dan belum disimpan sebagai data permanen di Smart Contract.
- Riwayat verifikasi saat ini masih bersifat sementara selama sesi aplikasi berjalan.
- QR Code menggunakan alamat lokal sehingga akses dari perangkat lain memerlukan konfigurasi URL yang dapat dijangkau.

10. Penutup
Sistem Verifikasi Ijazah Akademik Berbasis Blockchain dikembangkan sebagai implementasi pemanfaatan teknologi blockchain dalam bidang pendidikan, khususnya untuk meningkatkan transparansi dan mempermudah pemeriksaan keaslian ijazah akademik.

Melalui integrasi Smart Contract, Web3.py, Streamlit, dan NFT, sistem ini diharapkan dapat menjadi salah satu alternatif pengelolaan dan verifikasi dokumen akademik secara digital.

---

Project: Sistem Verifikasi Ijazah Akademik Berbasis Blockchain  
Framework: Streamlit  
Blockchain: Ethereum (Hardhat Local Network)  
Smart Contract: Solidity - ERC-721
