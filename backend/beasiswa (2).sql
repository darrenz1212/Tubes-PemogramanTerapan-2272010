-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 13 Jun 2024 pada 06.31
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `beasiswa`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `dokumen_pengajuan`
--

CREATE TABLE `dokumen_pengajuan` (
  `dokumen_id` int(11) NOT NULL,
  `pengajuan_id` int(11) DEFAULT NULL,
  `nama_dokumen` varchar(255) NOT NULL,
  `path_dokumen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `fakultas`
--

CREATE TABLE `fakultas` (
  `fakultas_id` int(11) NOT NULL,
  `nama_fakultas` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `fakultas`
--

INSERT INTO `fakultas` (`fakultas_id`, `nama_fakultas`) VALUES
(1, 'Teknologi Informasi');

-- --------------------------------------------------------

--
-- Struktur dari tabel `jenis_beasiswa`
--

CREATE TABLE `jenis_beasiswa` (
  `beasiswa_id` int(11) NOT NULL,
  `nama_beasiswa` varchar(255) NOT NULL,
  `deskripsi_beasiswa` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `jenis_beasiswa`
--

INSERT INTO `jenis_beasiswa` (`beasiswa_id`, `nama_beasiswa`, `deskripsi_beasiswa`) VALUES
(1234, 'Beasiswa Berprestasi', 'Beasiswa yang diberikan untuk mahasiswa dengan ipk > 3.0'),
(12345, 'Beasiswa Atlet', 'Beasiswa yang diberikan untuk atlet');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `nrp` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `nama_mahasiswa` varchar(255) NOT NULL,
  `program_studi_id` int(11) DEFAULT NULL,
  `ipk_terakhir` float NOT NULL,
  `status_aktif` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `mahasiswa`
--

INSERT INTO `mahasiswa` (`nrp`, `user_id`, `nama_mahasiswa`, `program_studi_id`, `ipk_terakhir`, `status_aktif`) VALUES
(123456, 2465873, 'JANE DOE PUTRI', 1, 3.81, 1),
(2272013, 2272010, 'DARREN ZAVIER ', 1, 3.75, 1),
(2272015, 4235678, 'PRAJOGO PANGESTI', 1, 3.75, 1),
(2272028, 6574872, 'Anton', 1, 3.5, 1),
(2272030, 6574876, 'karenn', 1, 3.5, 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `pengajuan_beasiswa`
--

CREATE TABLE `pengajuan_beasiswa` (
  `pengajuan_id` int(11) NOT NULL,
  `nrp` int(11) DEFAULT NULL,
  `beasiswa_id` int(11) DEFAULT NULL,
  `periode_id` int(11) DEFAULT NULL,
  `tanggal_pengajuan` date NOT NULL,
  `status_pengajuan` enum('Diajukan','Disetujui Prodi','Tidak Disetujui Prodi') NOT NULL,
  `status_pengajuan_fakultas` enum('Diajukan','Disetujui Fakultas','Tidak Disetujui Fakultas') NOT NULL,
  `dokumen_pengajuan` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `pengajuan_beasiswa`
--

INSERT INTO `pengajuan_beasiswa` (`pengajuan_id`, `nrp`, `beasiswa_id`, `periode_id`, `tanggal_pengajuan`, `status_pengajuan`, `status_pengajuan_fakultas`, `dokumen_pengajuan`) VALUES
(1, 2272013, 1234, 1, '2024-06-05', 'Tidak Disetujui Prodi', 'Diajukan', 'asdfgaherjhaethnasdfgh'),
(3, 123456, 1234, 1, '2024-06-05', 'Tidak Disetujui Prodi', 'Diajukan', 'Hflkuaywelkjfbasdlkvagwerlfakjsbdvaliwuerfgvba;sdjf'),
(13, 2272028, 1234, 1, '2024-06-13', 'Tidak Disetujui Prodi', 'Diajukan', 'filepath'),
(14, NULL, 1234, 1, '2024-06-13', 'Diajukan', 'Diajukan', 'filepath'),
(16, 2272030, 1234, 1, '2024-06-13', 'Tidak Disetujui Prodi', 'Diajukan', 'filepath');

-- --------------------------------------------------------

--
-- Struktur dari tabel `periode_pengajuan`
--

CREATE TABLE `periode_pengajuan` (
  `periode_id` int(11) NOT NULL,
  `nama_periode` varchar(255) NOT NULL,
  `tanggal_mulai` date NOT NULL,
  `tanggal_selesai` date NOT NULL,
  `fakultas_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `periode_pengajuan`
--

INSERT INTO `periode_pengajuan` (`periode_id`, `nama_periode`, `tanggal_mulai`, `tanggal_selesai`, `fakultas_id`) VALUES
(1, 'Periode Ganjil', '2024-02-01', '2024-04-30', 1),
(2, 'Periode Genap', '2024-06-01', '2024-08-31', 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `program_studi`
--

CREATE TABLE `program_studi` (
  `program_studi_id` int(11) NOT NULL,
  `nama_program_studi` varchar(255) NOT NULL,
  `fakultas_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `program_studi`
--

INSERT INTO `program_studi` (`program_studi_id`, `nama_program_studi`, `fakultas_id`) VALUES
(1, 'Teknik Infomatika', 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('administrator','mahasiswa','program_studi','fakultas') NOT NULL,
  `program_studi_id` int(11) DEFAULT NULL,
  `fakultas_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`user_id`, `username`, `password`, `role`, `program_studi_id`, `fakultas_id`) VALUES
(1234567, 'JHON DOE AHMAD', 'darren1234', 'mahasiswa', 1, 1),
(2272010, 'DARREN ZAVIER HASAEL', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'mahasiswa', 1, 1),
(2465873, 'JANE DOE PUTRI', 'jennydoe', 'administrator', 1, 1),
(4235678, 'PRAJOGO PANGESTI', 'd7d2f7cbeece7fca99e95c59d1f56310fb922e2ac1e7fb22e6ed1615360f33c6', 'mahasiswa', 1, 1),
(5647384, 'ALAN JAWATO', '66867678cbe9beb641ffaeee9a9210b1412e6a99c67ae9afa48cbc6b3f5dab72', 'mahasiswa', 1, 1),
(6574834, 'JOSEPH HANDOKO', '27545b395a8e5915b48557d0e26ef3e05e368d0f65ae786a806df38f9f4e3bc5', 'administrator', 1, 1),
(6574837, 'ALDIAN TEGA WIDJAYA KUSUMO AHRTO', '17532abc380037ee598bd06ebd4a9e075104d7e9e615720baa4934efd64a40f0', 'fakultas', NULL, 1),
(6574840, 'REZA PAHLEVI', 'c6b778a9d01f7e597a18e6d66a733a8602102c48ffa1cf51e152e6a685b9c52f', 'mahasiswa', 1, 1),
(6574842, 'SuhermanTanoko', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'program_studi', NULL, 1),
(6574846, 'GatotBrotot', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'program_studi', NULL, NULL),
(6574847, 'William ', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'program_studi', NULL, NULL),
(6574848, 'ucup', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'program_studi', NULL, NULL),
(6574850, 'palandi', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'program_studi', NULL, NULL),
(6574866, 'joni', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'program_studi', 1, NULL),
(6574869, 'alex', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'mahasiswa', 1, NULL),
(6574872, 'ujang ', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'mahasiswa', 1, NULL),
(6574873, 'harianto', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'program_studi', 1, NULL),
(6574875, 'bernandus', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'mahasiswa', 1, NULL),
(6574876, 'karen', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'mahasiswa', 1, NULL),
(6574877, 'bobi', '919357e357b72b41935142e1e70828a99e507b05805f691f3c249ffe192db90c', 'program_studi', 1, NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('administrator','mahasiswa','program_studi','fakultas') NOT NULL,
  `program_studi_id` int(11) DEFAULT NULL,
  `fakultas_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `dokumen_pengajuan`
--
ALTER TABLE `dokumen_pengajuan`
  ADD PRIMARY KEY (`dokumen_id`),
  ADD KEY `pengajuan_id` (`pengajuan_id`);

--
-- Indeks untuk tabel `fakultas`
--
ALTER TABLE `fakultas`
  ADD PRIMARY KEY (`fakultas_id`);

--
-- Indeks untuk tabel `jenis_beasiswa`
--
ALTER TABLE `jenis_beasiswa`
  ADD PRIMARY KEY (`beasiswa_id`);

--
-- Indeks untuk tabel `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD PRIMARY KEY (`nrp`),
  ADD KEY `mahasiswa_ibfk_1` (`user_id`),
  ADD KEY `mahasiswa_ibfk_2` (`program_studi_id`);

--
-- Indeks untuk tabel `pengajuan_beasiswa`
--
ALTER TABLE `pengajuan_beasiswa`
  ADD PRIMARY KEY (`pengajuan_id`),
  ADD KEY `beasiswa_id` (`beasiswa_id`),
  ADD KEY `periode_id` (`periode_id`),
  ADD KEY `nrp` (`nrp`);

--
-- Indeks untuk tabel `periode_pengajuan`
--
ALTER TABLE `periode_pengajuan`
  ADD PRIMARY KEY (`periode_id`),
  ADD KEY `fakultas_id` (`fakultas_id`);

--
-- Indeks untuk tabel `program_studi`
--
ALTER TABLE `program_studi`
  ADD PRIMARY KEY (`program_studi_id`),
  ADD KEY `fakultas_id` (`fakultas_id`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `fakultas_id` (`fakultas_id`),
  ADD KEY `user_ibfk_1` (`program_studi_id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `program_studi_id` (`program_studi_id`),
  ADD KEY `fakultas_id` (`fakultas_id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `dokumen_pengajuan`
--
ALTER TABLE `dokumen_pengajuan`
  MODIFY `dokumen_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `fakultas`
--
ALTER TABLE `fakultas`
  MODIFY `fakultas_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `jenis_beasiswa`
--
ALTER TABLE `jenis_beasiswa`
  MODIFY `beasiswa_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12346;

--
-- AUTO_INCREMENT untuk tabel `mahasiswa`
--
ALTER TABLE `mahasiswa`
  MODIFY `nrp` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2272031;

--
-- AUTO_INCREMENT untuk tabel `pengajuan_beasiswa`
--
ALTER TABLE `pengajuan_beasiswa`
  MODIFY `pengajuan_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT untuk tabel `periode_pengajuan`
--
ALTER TABLE `periode_pengajuan`
  MODIFY `periode_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `program_studi`
--
ALTER TABLE `program_studi`
  MODIFY `program_studi_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6574878;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `dokumen_pengajuan`
--
ALTER TABLE `dokumen_pengajuan`
  ADD CONSTRAINT `dokumen_pengajuan_ibfk_1` FOREIGN KEY (`pengajuan_id`) REFERENCES `pengajuan_beasiswa` (`pengajuan_id`);

--
-- Ketidakleluasaan untuk tabel `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD CONSTRAINT `mahasiswa_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `mahasiswa_ibfk_2` FOREIGN KEY (`program_studi_id`) REFERENCES `program_studi` (`program_studi_id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `pengajuan_beasiswa`
--
ALTER TABLE `pengajuan_beasiswa`
  ADD CONSTRAINT `pengajuan_beasiswa_ibfk_1` FOREIGN KEY (`nrp`) REFERENCES `mahasiswa` (`nrp`),
  ADD CONSTRAINT `pengajuan_beasiswa_ibfk_2` FOREIGN KEY (`beasiswa_id`) REFERENCES `jenis_beasiswa` (`beasiswa_id`),
  ADD CONSTRAINT `pengajuan_beasiswa_ibfk_3` FOREIGN KEY (`periode_id`) REFERENCES `periode_pengajuan` (`periode_id`);

--
-- Ketidakleluasaan untuk tabel `periode_pengajuan`
--
ALTER TABLE `periode_pengajuan`
  ADD CONSTRAINT `periode_pengajuan_ibfk_1` FOREIGN KEY (`fakultas_id`) REFERENCES `fakultas` (`fakultas_id`);

--
-- Ketidakleluasaan untuk tabel `program_studi`
--
ALTER TABLE `program_studi`
  ADD CONSTRAINT `program_studi_ibfk_1` FOREIGN KEY (`fakultas_id`) REFERENCES `fakultas` (`fakultas_id`);

--
-- Ketidakleluasaan untuk tabel `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`program_studi_id`) REFERENCES `program_studi` (`program_studi_id`) ON DELETE SET NULL ON UPDATE SET NULL,
  ADD CONSTRAINT `user_ibfk_2` FOREIGN KEY (`fakultas_id`) REFERENCES `fakultas` (`fakultas_id`);

--
-- Ketidakleluasaan untuk tabel `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`program_studi_id`) REFERENCES `program_studi` (`program_studi_id`),
  ADD CONSTRAINT `users_ibfk_2` FOREIGN KEY (`fakultas_id`) REFERENCES `fakultas` (`fakultas_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
