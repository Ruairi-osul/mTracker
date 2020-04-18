from flask import Flask
from mtracker.config import Config
from mtracker.extentions import db


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from mtracker.main.routes import main
    from mtracker.experiments.routes import experiments
    from mtracker.session_types.routes import session_types
    from mtracker.surgery_types.routes import surgery_types
    from mtracker.groups.routes import groups
    from mtracker.data_types.routes import data_types
    from mtracker.mice.routes import mice
    from mtracker.datasets.routes import datasets
    from mtracker.images.routes import images

    app.register_blueprint(main)
    app.register_blueprint(experiments)
    app.register_blueprint(session_types)
    app.register_blueprint(surgery_types)
    app.register_blueprint(groups)
    app.register_blueprint(data_types)
    app.register_blueprint(mice)
    app.register_blueprint(datasets)
    app.register_blueprint(images)

    return app
