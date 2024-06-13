const express = require('express');
const router = express.Router();


router.use(express.static('public'));


const loginController = require('../controller/loginController');
const registerController = require('../controller/registerController');
const prodiController = require('../controller/prodiController');
const mahasiswaController = require('../controller/mahasiswaController');

router.get('/', loginController.index);
router.post('/login', loginController.login);
router.get('/register', registerController.index);
router.post('/register', registerController.registerUser);

router.get('/prodi', prodiController.index);
router.get('/prodi/show-beasiswa', prodiController.getBeasiswa);
router.get('/prodi/show-mahasiswa', prodiController.getMahasiswa);
router.put('/prodi/approve-beasiswa', prodiController.approveBeasiswa);
router.put('/prodi/decline-beasiswa', prodiController.declineBeasiswa);
router.delete('/prodi/delete-mahasiswa', prodiController.deleteMahasiswa);
router.put('/prodi/update-mahasiswa', prodiController.updateMahasiswa);

router.get('/mahasiswa', mahasiswaController.index);
router.get('/mahasiswa/pengajuan', mahasiswaController.showPengajuanForm);
router.post('/mahasiswa/pengajuan', mahasiswaController.submitPengajuan);
router.get('/mahasiswa/history', mahasiswaController.pengajuanList)
router.delete('/mahasiswa/delete-pengajuan', mahasiswaController.deletePengajuan)

module.exports = router;
