from flask import Flask
from mtracker.config import Config
from mtracker.extentions import db


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from mtracker.main.routes import main
    from mtracker.experiments.routes import experiments

    app.register_blueprint(main)
    app.register_blueprint(experiments)

    return app
