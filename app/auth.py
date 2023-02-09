# blueprint is a way to organize a group of related views. blueprint is available in factory function
# this app will have 2 blueprints: one for auth functions, one for blog post functions. code for each bp goes in separate modules.

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

# creates a blueprint named 'auth'. needs to be imported and registered with the factory fn using app.register_blueprint()
bp = Blueprint('auth', __name__, url_prefix='/auth')


# runs before the view function, no matter the URL.
# load_logged_in_user() checks if user id is stored in session, gets it from the db and stores it in g.user for the length of the request
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# to logout, remove user_id from session. then load_logged_in_user() won't load a user on subsequent requests
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# register() is a view function. when Flask receives a req to '/auth/register', it calls the register view and uses the return value as the response
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # if user's input was valid, insert new data into db
        # never store passwords directly into db, use generate_password_hash() to hash the pw, then store the hash. db.commit() saves changes afterwards
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


# login() view function. /auth/login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
            
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # session is a dict that stores data across requests. if validation succeeds, the user's `id` is stored in a new session
        # data is stored in a cookie sent to the browser, and browser sends it back with subsequent requests. cookie gets signed by flask for verification
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')