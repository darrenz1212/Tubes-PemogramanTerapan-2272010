const express = require('express');
const router = express.Router();
router.use(express.static('public'));

const loginController = require('../controller/loginController');
const prodiController = require('../controller/prodiController');

router.get('/', loginController.index);
router.post('/login', loginController.login);

router.get('/prodi', prodiController.index);
router.get('/prodi/show-beasiswa', prodiController.getBeasiswa);
router.put('/prodi/approve-beasiswa', prodiController.approveBeasiswa);
router.put('/prodi/decline-beasiswa', prodiController.declineBeasiswa);

module.exports = router;
