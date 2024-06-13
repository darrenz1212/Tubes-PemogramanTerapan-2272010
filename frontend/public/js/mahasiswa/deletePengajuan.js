document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.btn-delete');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const pengajuanId = this.getAttribute('data-id');
            console.log(`Attempting to delete pengajuan with ID: ${pengajuanId}`);  // Debug log

            Swal.fire({
                title: 'Anda yakin?',
                text: "Anda akan menghapus pengajuan ini!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Ya, hapus!'
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch('/mahasiswa/delete-pengajuan', {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ pengajuanId: pengajuanId })
                    })
                    .then(response => {
                        console.log('Received response from server');  // Debug log
                        return response.json();
                    })
                    .then(data => {
                        console.log('Server Response:', data);  // Debug log
                        if (data.success) {
                            Swal.fire(
                                'Dihapus!',
                                'Pengajuan telah dihapus.',
                                'success'
                            ).then(() => {
                                const row = document.querySelector(`button[data-id="${pengajuanId}"]`).closest('tr');
                                row.remove();
                            });
                        } else {
                            Swal.fire(
                                'Gagal!',
                                data.message || 'Pengajuan gagal dihapus.',
                                'error'
                            );
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        Swal.fire(
                            'Gagal!',
                            'Terjadi kesalahan saat menghapus pengajuan.',
                            'error'
                        );
                    });
                }
            });
        });
    });
});
