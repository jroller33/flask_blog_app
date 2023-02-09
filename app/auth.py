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



@bp.route('/register', methods=('GET', 'POST'))
def register():
# register() is a view function. when Flask receives a req to '/auth/register', it calls the register view and uses the return value as the response
    
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


