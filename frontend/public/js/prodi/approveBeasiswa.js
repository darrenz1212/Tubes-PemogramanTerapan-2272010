document.addEventListener('DOMContentLoaded', function() {
    const approveButtons = document.querySelectorAll('.btn-approve');

    approveButtons.forEach(button => {
        button.addEventListener('click', function() {
            const pengajuanId = this.getAttribute('data-id');

            Swal.fire({
                title: 'Anda yakin?',
                text: "Anda akan menyetujui pengajuan ini!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Ya, setujui!'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(`/prodi/approve-beasiswa`, {
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
                                'Disetujui!',
                                'Pengajuan beasiswa telah disetujui.',
                                'success'
                            ).then(() => {
                                location.reload(); // Refresh halaman untuk menampilkan status yang diperbarui
                            });
                        } else {
                            Swal.fire(
                                'Gagal!',
                                data.message || 'Pengajuan beasiswa gagal disetujui.',
                                'error'
                            );
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        Swal.fire(
                            'Gagal!',
                            'Terjadi kesalahan saat menyetujui pengajuan.',
                            'error'
                        );
                    });
                }
            });
        });
    });
});
