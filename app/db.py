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
        
        
def init_db():
    db = get_db()
    
    # .open_resource() opens a file relative to the `app` package (later when deployed may not know what the full path is)
    # get_db returns a db connection
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        
        
# this creates a CLI command 'init-db' that calls the init function and shows success message
@click.command('init-db')
def init_db_command():
    """clears existing data and creates new tables"""
    init_db()
    click.echo('Initialized database')
    
    
def init_app(app):
    # tells Flask to call `close_db()` after response when cleaning up
    app.teardown_appcontext(close_db)
    
    # adds a new command that can be called with the `flask` command
    app.cli.add_command(init_db_command)