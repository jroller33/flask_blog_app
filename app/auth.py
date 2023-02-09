import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# blueprint is a way to organize a group of related views. blueprint is available in factory function
# this app will have 2 blueprints: one for auth functions, one for blog post functions. code for each blueprint goes in separate modules.