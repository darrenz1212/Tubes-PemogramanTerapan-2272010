const express = require('express');
const session = require('express-session'); // Add this for session management
const app = express();
const fileUpload = require('express-fileupload');

app.use(session({
    secret: 'your-secret-key',
    resave: false,
    saveUninitialized: true,
    cookie: {
        maxAge: 1800000, // 30 menit, Anda bisa sesuaikan
        secure: false, // Atur menjadi true jika menggunakan HTTPS
        httpOnly: false
    }  // Set to true if using https
}));

app.set('view engine', 'pug');
app.set('views', 'view');

const myRoutes = require('./routes/route');
app.use(express.urlencoded({extended: false}));
app.use(express.json());
app.use(fileUpload());

app.use(myRoutes);

app.use((req, res, next) => {
    res.send('404');
});

app.listen(8000, () => {
    console.log('Server is running at port 8000');
});
