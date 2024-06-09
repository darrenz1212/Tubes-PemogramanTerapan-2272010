const express = require('express');
const session = require('express-session'); // Add this for session management
const app = express();

app.use(session({
    secret: 'your-secret-key',
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false } // Set to true if using https
}));

app.set('view engine', 'pug');
app.set('views', 'view');

const myRoutes = require('./routes/route');
app.use(express.urlencoded({extended: false}));
app.use(express.json()); // Add this to handle JSON body

app.use(myRoutes);

app.use((req, res, next) => {
    res.send('404');
});

app.listen(8000, () => {
    console.log('Server is running at port 8000');
});
