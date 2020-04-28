from flask import Blueprint
from models.permission import Application
from utils.json import json
from api import db

application_api = Blueprint("application", __name__)


@application_api.route("/create", methods=["POST"])
@json(admin_only=True)
def create(data: dict):
    """
    Create an new application.
    :param data: The json payload as dict.
    :return: A http response containing the new application.
    """

    name: str = data.get("name")

    if not name:
        return 400

    application: Application = Application.create(name)

    if not application:
        return 404

    return {
        "uuid": application.uuid,
        "name": application.name,
        "token": application.token,
    }


@application_api.route("/delete", methods=["DELETE"])
@json(admin_only=True)
def delete(data: dict):
    """
    Delete an existing application.
    :param data: The json payload as dict.
    :return: A http response containing the result.
    """

    uuid: str = data.get("uuid")

    if not uuid:
        return 400

    application: Application = Application.query.filter_by(uuid=uuid).first()

    if not application:
        return 404

    db.session.remove(application)
    db.session.commit()

    return {}


@application_api.route("/all", methods=["GET"])
@json(admin_only=True, pass_data=False)
def list_all():
    """
    Lists all applications.
    :return: A http response containing the result.
    """

    return [
        {
            "uuid": application.uuid,
            "name": application.name,
            "token": application.token,
        }
        for application in Application.query.all()
    ]


@application_api.route("/update/name", methods=["PATCH"])
@json(admin_only=True)
def update_name(data: dict):
    """
    Update the name of an existing application.
    :param data: The json payload as dict.
    :return: A http response containing the result.
    """

    uuid: str = data.get("uuid")
    name: str = data.get("name")

    if not name or not uuid:
        return 400

    application: Application = Application.query.filter_by(uuid=uuid).first()

    if not application:
        return 404

    application.name = name
    db.session.commit()

    return {}


@application_api.route("/regenerate", methods=["PATCH"])
@json(admin_only=True)
def regenerate_token(data: dict):
    """
    Regenerate the token of an existing application.
    :param data: The json payload as dict.
    :return: A http response containing the new token.
    """

    uuid: str = data.get("uuid")

    if not uuid:
        return 400

    application: Application = Application.query.filter_by(uuid=uuid).first()

    if not application:
        return 404

    token: str = application.regenerate_token()

    return {
        "token": token,
    }
