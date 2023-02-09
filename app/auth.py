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
