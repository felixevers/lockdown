from flask import Flask
from config.environment import config
from config.database import get_mysql_uri
from api import db, jwt_manager
from resources.auth import auth_api


def create_app() -> Flask:
    """
    Creates a flask application and initializes the extensions.
    :returns: A flask application
    """
    app: Flask = Flask("lockdown")

    app.config.update(**config)
    app.config["SQLALCHEMY_DATABASE_URI"] = get_mysql_uri()

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app: Flask) -> None:
    """
    Registers flask extensions like `sqlalchemy` and `jwt`.
    :param app: A flask application
    :returns: Nothing
    """
    db.init_app(app)
    jwt_manager.init_app(app)


def register_blueprints(app: Flask) -> None:
    """
    Registers flask blueprints defined in resources.
    :param app: A flask application
    :returns: Nothing
    """
    app.register_blueprint(auth_api, url_prefix="/auth")


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8080)
