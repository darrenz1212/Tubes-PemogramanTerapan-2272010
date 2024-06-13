document.addEventListener('DOMContentLoaded', function() {
    const editButtons = document.querySelectorAll('.btn-edit');

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const nrp = this.getAttribute('data-id');
            console.log('NRP:', nrp); // Debug log
            fetch(`http://127.0.0.1:5000/admin/get-mhsw/${nrp}`)
            .then(response => response.json())
            .then(data => {
                if (data) {
                    console.log('Data Mahasiswa:', data); // Debug log
                    document.getElementById('nama_mahasiswa').value = data.nama_mahasiswa;
                    document.getElementById('nrp').value = data.nrp;
                    document.getElementById('prodi').value = data.prodi;
                    document.getElementById('ipk').value = data.ipk;
                    document.getElementById('status').value = data.status.toString();
                    document.getElementById('user_id').value = data.user_id;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Submit form untuk update data mahasiswa
    const editForm = document.getElementById('editMahasiswaForm');
    editForm.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('Form submitted'); // Debug log

        const formData = new FormData(editForm);
        const payload = {
            nama_mahasiswa: formData.get('nama_mahasiswa'),
            nrp: formData.get('nrp'),
            prodi: formData.get('prodi'),
            ipk: parseFloat(formData.get('ipk')),
            status: formData.get('status') === 'true',
            user_id: formData.get('user_id')
        };

        console.log('Payload:', payload); // Debug log

        fetch(`http://127.0.0.1:5000/admin/update-mhsw/${payload.nrp}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response from server:', data); // Debug log
            if (data.message && data.message.includes('updated successfully')) {
                Swal.fire(
                    'Berhasil!',
                    'Data mahasiswa telah diperbarui.',
                    'success'
                ).then(() => {
                    window.location.href = "/prodi/show-mahasiswa";
                });
            } else {
                Swal.fire(
                    'Gagal!',
                    'Gagal memperbarui data mahasiswa.',
                    'error'
                );
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire(
                'Gagal!',
                'Terjadi kesalahan saat memperbarui data.',
                'error'
            );
        });
    });
});
