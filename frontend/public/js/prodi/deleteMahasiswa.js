document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.btn-delete');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const nrp = this.getAttribute('data-id');

            Swal.fire({
                title: 'Anda yakin?',
                text: "Anda menghapus mahasiswa ini!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Ya, hapus!'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/prodi/delete-mahasiswa`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ nrp : nrp})
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Server Response:', data);
                        if (data.success) {
                            Swal.fire(
                                'Dihapus!',
                                'Mahasiswa telah di hapus.',
                                'success'
                            ).then(() => {
                                location.reload(); 
                            });
                        } else {
                            Swal.fire(
                                'Gagal!',
                                data.message || 'Mahasiswa gagal di hapus.',
                                'error'
                            );
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        Swal.fire(
                            'Gagal!',
                            'Terjadi kesalahan saat menghapus beasiswa.',
                            'error'
                        );
                    });
                }
            });
        });
    });
});
