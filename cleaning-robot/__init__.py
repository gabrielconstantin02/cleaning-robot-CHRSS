import os

from flask import Flask
from . import db
from . import auth
from . import environment
from . import cleaning
from . import vacuum_settings
from . import mop_settings
from . import cleaning_schedule
from . import air_quality
from . import automatic_empty

def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'cleaning-robot.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

   # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    app.register_blueprint(auth.bp)
    app.register_blueprint(environment.bp)
    app.register_blueprint(cleaning.bp)
    app.register_blueprint(vacuum_settings.bp)
    app.register_blueprint(mop_settings.bp)
    app.register_blueprint(cleaning_schedule.bp)
    app.register_blueprint(air_quality.bp)
    app.register_blueprint(automatic_empty.bp)

    return app
