const index = (req, res) => {
    console.log(req.session.user)
    if (!req.session.user) {
        return res.redirect('/'); // Redirect to login if not logged in
    }
    res.render('prodi/index', { user: req.session.user });
};

const getBeasiswa = (req, res) => {
    fetch('http://localhost:5000/prodi/pengajuan/1')
    .then(response => response.json())
    .then(data => {
        console.log('Data from API:', data); // Debugging data
        console.log('Session : ', req.session.user)
        res.render('prodi/showBeasiswa', {
            data: data.pengajuan, 
            session: req.session.user
        });
    })
    .catch(error => {
        console.error('Fetch error:', error);
        res.render('prodi/showBeasiswa', { error: 'Failed to load data', session: req.session.user });
    });
}

const approveBeasiswa = (req, res) => {
    const { pengajuan_id } = req.body;
    console.log('Pengajuan ID untuk Approve:', pengajuan_id);

    if (!pengajuan_id) {
        return res.status(400).json({ success: false, message: 'Pengajuan ID tidak ditemukan.' });
    }

    fetch(`http://localhost:5000/prodi/pengajuan/approve/${pengajuan_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('API Response:', data);
        if (data.message && data.message.includes('approved')) {
            res.json({ success: true, message: 'Beasiswa disetujui.' });
        } else {
            res.status(500).json({ success: false, message: 'Gagal menyetujui beasiswa.' });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        res.status(500).json({ success: false, message: 'Terjadi kesalahan.' });
    });
}

const declineBeasiswa = (req, res) => {
    const { pengajuan_id } = req.body;
    console.log('Pengajuan ID untuk Decline:', pengajuan_id);

    if (!pengajuan_id) {
        return res.status(400).json({ success: false, message: 'Pengajuan ID tidak ditemukan.' });
    }

    fetch(`http://localhost:5000/prodi/pengajuan/decline/${pengajuan_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('API Response:', data);
        if (data.message && data.message.includes('declined')) {
            res.json({ success: true, message: 'Beasiswa ditolak.' });
        } else {
            res.status(500).json({ success: false, message: 'Gagal menolak beasiswa.' });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        res.status(500).json({ success: false, message: 'Terjadi kesalahan.' });
    });
}

module.exports = {
    index,
    getBeasiswa,
    approveBeasiswa,
    declineBeasiswa
}
