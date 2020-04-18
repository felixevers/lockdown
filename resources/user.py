from flask import Blueprint
from utils.json import json
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

user_api = Blueprint("user", __name__)


@user_api.route("/create", methods=["POST"])
@json()
def create(data: dict):
    """
    Creates a user by name and password
    :param data: The json payload as dict.
    :return: A http response containing the user information
    """
    name: str = data.get("name")
    password: str = data.get("password")

    if not name or not password:
        return {}, 400

    user: User = User.create(name, password)

    if not user:
        return {
            "result": False,
        }

    return {
        "result": True,
        "uuid": user.uuid,
        "name": user.name,
    }


@user_api.route("/get", methods=["GET"])
@json()
@jwt_required
def get(data: dict):
    identity: any = get_jwt_identity()

    if not isinstance(identity, dict):
        return 401

    uuid: str = identity.get("uuid")

    if not uuid:
        return {}, 400

    user: User = User.query(uuid=uuid).first()

    if not user:
        return {}, 400

    return {
        "uuid": user.uuid,
        "name": user.name,
        "admin": user.admin,
    }
