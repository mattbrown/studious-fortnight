import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from microblog import models

db = SQLAlchemy(model_class=models.Base)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)


    if test_config is None:
        app.config.from_pyfile('config.py', silent=False)
    else:
        app.config.from_mapping(test_config)

    # Setup database
    db.init_app(app)
    db.create_all()

    # Setup Paths
    from . import users,posts
    app.register_blueprint(users.bp)
    app.register_blueprint(posts.bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


