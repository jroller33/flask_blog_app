import sqlite3
import click
from flask import current_app, g

# `g` is a special object that's unique for each request. stores data that can be used by multiple functions. connection is stored and reused if its the same request
# current_app points to Flask app handling the request.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()