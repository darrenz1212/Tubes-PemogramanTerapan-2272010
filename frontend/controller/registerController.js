const index = (req, res) => {
    res.render('auth/register');
}


const registerUser = (req, res) => {
    const { username, password, role, programStudiId, fakultasId } = req.body;


    const payload = {
        username,
        password,
        role,
        program_studi_id: programStudiId, 
        fakultasId: parseInt(fakultasId) 
    };

 
    fetch('http://127.0.0.1:5000/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data); 

        if (data.message && data.message === 'User registered successfully') {
            if (payload.role === 'mahasiswa') {
                fetch('http://127.0.0.1:5000/admin/get-user', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(userData => {
                    console.log('User Data:', userData); 
                    
     
                    const user = userData.user.find(u => u.username === username);

                    if (user) {
                        const userId = user.user_id; 
                        console.log('User ID:', userId); 
                        const mahasiswaBody = {
                            ipk: 0, 
                            status: true, 
                        };

                        fetch(`http://127.0.0.1:5000/admin/add-mhsw/${userId}`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(mahasiswaBody)
                        })
                        .then(mahasiswaResponse => mahasiswaResponse.json())
                        .then(mahasiswaData => {
                            console.log('Mahasiswa Data:', mahasiswaData); 

                            if (mahasiswaData.message && mahasiswaData.message.includes('successfully')) {
                                res.render('auth/register', { success: 'User and student registered successfully!' });
                            } else {
                                res.render('auth/register', { error: 'User registered, but failed to register student. Please try again.' });
                            }
                        })
                        .catch(mahasiswaError => {
                            console.error('Error registering student:', mahasiswaError);
                            res.render('auth/register', { error: 'User registered, but an error occurred while registering student.' });
                        });
                    } else {
                        res.render('auth/register', { error: 'User registered, but userId not found.' });
                    }
                })
                .catch(userError => {
                    console.error('Error fetching userId:', userError);
                    res.render('auth/register', { error: 'User registered, but an error occurred while fetching userId.' });
                });
            } else {
                res.render('auth/register', { success: 'User registered successfully!' });
            }
        } else {
            res.render('auth/register', { error: 'Registration failed. Please try again.' });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        res.render('auth/register', { error: 'An error occurred. Please try again later.' });
    });
}



module.exports = {
    index,
    registerUser
}
