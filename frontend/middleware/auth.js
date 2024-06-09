function ensureAuthenticated(req, res, next) {
    console.log('Session user:', req.session.user); // Tambahkan log untuk melihat data user di session
    if (req.session.user) {
        res.locals.user = req.session.user;
        return next();
    } else {
        res.redirect('/');
    }
}

module.exports = {
    ensureAuthenticated
};