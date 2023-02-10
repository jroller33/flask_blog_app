# __init__.py does two things: contains Application Factory and tells python that the 'app/' folder should be treated as a package.


# https://flask.palletsprojects.com/en/2.2.x/tutorial/views/
# ending right before endpoints and URLS

import os

from flask import Flask


# create_app() is the application factory function
def create_app(test_config=None):
    
    # creates and configures the app
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        # SECRET_KEY should be changed before deploying
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),    # path for DB
    )
    
    if test_config is None:
        # load instance config if it exists when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if it's passed into the function
        app.config.from_mapping(test_config)
        
    # make sure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # route that says hello
    # http://127.0.0.1:5000/hello
    # if you put two routes on the same function, it will respond to both
    @app.route('/')
    @app.route('/hello')
    def hello():
        return 'sup'
    
    
    from . import db
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    return app