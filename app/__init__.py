# __init__.py does two things: contains Application Factory and tells python that the 'app/' folder should be treated as a package.

import os

from flask import Flask


# create_app() is the application factory function
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite'),    # path for DB
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/hello')
    def hello():
        return 'sup'
    
    return app