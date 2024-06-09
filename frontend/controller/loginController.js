const index = (req, res) => {
    res.render('auth/login');
};

const login = (req, res) => {
    const { username, password } = req.body;
    
    fetch('http://127.0.0.1:5000/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Login successful') {
            req.session.user = {
                role: data.role,
                user_id: data.user_id,
                username: data.username
            };
            if (data.role === "program_studi"){
                res.redirect('/prodi'); // Replace with the desired route after login
            }
        } else {
            res.render('auth/login', { error: 'Login failed. Please try again.' });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        res.render('auth/login', { error: 'An error occurred. Please try again later.' });
    });
};

module.exports = {
    index,
    login
};
