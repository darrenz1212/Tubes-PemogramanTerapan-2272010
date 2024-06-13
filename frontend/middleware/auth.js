function ensureAuthenticated(req, res, next) {
    console.log('Session user:', req.session.user);
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