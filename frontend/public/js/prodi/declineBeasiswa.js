document.addEventListener('DOMContentLoaded', function() {
    const declineButtons = document.querySelectorAll('.btn-decline');

    declineButtons.forEach(button => {
        button.addEventListener('click', function() {
            const pengajuanId = this.getAttribute('data-id');

            // Tambahkan konfirmasi dengan SweetAlert
            Swal.fire({
                title: 'Anda yakin?',
                text: "Anda akan menolak pengajuan ini!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Ya, tolak!'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/prodi/decline-beasiswa`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ pengajuan_id: pengajuanId })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Server Response:', data);
                        if (data.success) {
                            Swal.fire(
                                'Ditolak!',
                                'Pengajuan beasiswa telah ditolak.',
                                'success'
                            ).then(() => {
                                location.reload(); // Refresh halaman untuk menampilkan status yang diperbarui
                            });
                        } else {
                            Swal.fire(
                                'Gagal!',
                                data.message || 'Pengajuan beasiswa gagal ditolak.',
                                'error'
                            );
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        Swal.fire(
                            'Gagal!',
                            'Terjadi kesalahan saat menolak pengajuan.',
                            'error'
                        );
                    });
                }
            });
        });
    });
});
