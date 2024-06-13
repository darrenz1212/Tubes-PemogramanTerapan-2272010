

const index = (req, res) => {
    console.log(req.session.user);
    res.render('mahasiswa/index', {
        user: req.session.user
    });
};

const showPengajuanForm = (req, res) => {
    res.render('mahasiswa/pengajuan', {
        user: req.session.user
    });
};

const submitPengajuan = async (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ message: 'User not logged in' });
    }

    const mahasiswaUsername = req.session.user.username; 
    const { beasiswaId, periodeId } = req.body;

    try {
        const response = await fetch('http://127.0.0.1:5000/admin/show-mhsw');
        const apiData = await response.json();

        console.log('Data from API:', apiData);

        if (!apiData.mahasiswa || !Array.isArray(apiData.mahasiswa)) {
            return res.status(500).json({ message: 'Invalid data format received from API' });
        }

        const mahasiswa = apiData.mahasiswa.find(mhsw => mhsw.nama_mahasiswa.toLowerCase() === mahasiswaUsername.toLowerCase());

        if (!mahasiswa) {
            return res.status(404).json({ message: 'Mahasiswa not found' });
        }

        const nrp = mahasiswa.nrp;
        console.log(`NRP: ${nrp}`);

        const submitResponse = await fetch(`http://localhost:5000/mahasiswa/submit/${nrp}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                beasiswaId: parseInt(beasiswaId),
                periodeId: parseInt(periodeId)
            })
        });

        const submitData = await submitResponse.json();
        console.log('Response from server:', submitData);

        if (submitData.message && submitData.message === 'Pengajuan submitted successfully') {
            res.render('mahasiswa/pengajuan', { success: 'Pengajuan submitted successfully!', user: req.session.user, nrp });
        } else {
            res.render('mahasiswa/pengajuan', { error: 'Failed to submit pengajuan. Please try again.', user: req.session.user, nrp });
        }
    } catch (error) {
        console.error('Error:', error);
        res.render('mahasiswa/pengajuan', { error: 'An error occurred. Please try again later.', user: req.session.user, nrp });
    }
};

const pengajuanList = async (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ message: 'User not logged in' });
    }

    const mahasiswaUsername = req.session.user.username;

    try {
        const response = await fetch('http://127.0.0.1:5000/admin/show-mhsw');
        const apiData = await response.json();

        console.log('Data from API:', apiData);

        if (!apiData.mahasiswa || !Array.isArray(apiData.mahasiswa)) {
            return res.status(500).json({ message: 'Invalid data format received from API' });
        }

        const mahasiswa = apiData.mahasiswa.find(mhsw => mhsw.nama_mahasiswa.toLowerCase() === mahasiswaUsername.toLowerCase());

        if (!mahasiswa) {
            return res.status(404).json({ message: 'Mahasiswa not found' });
        }

        const nrp = mahasiswa.nrp;

        const pengajuanResponse = await fetch(`http://localhost:5000/mahasiswa/showBeasiswa/${nrp}`);
        const pengajuanData = await pengajuanResponse.json();

        console.log('Beasiswa Data from API:', pengajuanData);

        if (!pengajuanData.pengajuan || !Array.isArray(pengajuanData.pengajuan)) {
            return res.status(500).json({ message: 'Invalid data format received from API' });
        }

        res.render('mahasiswa/historyPengajuan', {
            user: req.session.user,
            pengajuan: pengajuanData.pengajuan
        });
    } catch (error) {
        console.error('Error:', error);
        res.render('mahasiswa/historyPengajuan', { error: 'An error occurred. Please try again later.', user: req.session.user });
    }
};
const deletePengajuan = async (req, res) => {
    const { pengajuanId } = req.body;
    console.log(pengajuanId)
    if (!pengajuanId){
        return res.status(400).json({ success: false, message: 'pengajuanId tidak ditemukan.' })
        }
    try {
        const response = await fetch(`http://localhost:5000/mahasiswa/deletePengajuan/${pengajuanId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        if (result.message && result.message === 'Pengajuan deleted successfully') {
            res.json({ success: true, message: 'Pengajuan deleted successfully' });
        } else {
            res.status(500).json({ success: false, message: 'Failed to delete pengajuan' });
        }
    } catch (error) {
        res.status(500).json({ success: false, message: 'An error occurred. Please try again later.' });
    }
};

module.exports = {
    index,
    showPengajuanForm,
    submitPengajuan,
    pengajuanList,
    deletePengajuan
};