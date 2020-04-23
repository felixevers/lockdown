from flask import Blueprint, jsonify, abort, Response
from flask_jwt_extended import unset_jwt_cookies
from utils.json import json
from models.user import User
from api import db

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
@json(pass_data=False, pass_user=True)
def get(user: User):
    """
    Get the current user identity.
    :return: A http response containing the current user information
    """

    return {
        "uuid": user.uuid,
        "name": user.name,
        "admin": user.admin,
    }


@user_api.route("/change/password", methods=["PATCH"])
@json(pass_user=True)
def update_password(data: dict, user: User):
    """
    Update the password of this user.
    :param user: The user mapped to the session.
    :param data: The json payload as dict.
    :return: A http response containing the result
    """

    password: str = data.get("password")
    new_password: str = data.get("newPassword")

    if not user.check(password):
        return 401

    user.update(new_password)

    return {
        "result": True,
    }


@user_api.route("/delete", methods=["DELETE"])
@json(pass_user=True, encode_json=False)
def delete(data: dict, user: User):
    """
    Delete logged user with password.
    :param user: The user mapped to the session.
    :param data: The json payload as dict.
    :return: A http response containing the deletion result
    """

    password: str = data.get("password")

    if not password or not user.check(password):
        return 403

    db.session.remove(user)
    db.session.commit()

    response: Response = jsonify({
        "result": True
    })

    unset_jwt_cookies(response)

    return response


@user_api.route("/all", methods=["GET"])
@json(pass_data=False, admin_only=True)
def get_all():
    """
    Get all registered users.
    :return: A http response containing all users
    """

    return [
        {"uuid": user.uuid, "name": user.name, "admin": user.admin} for user in User.query.all()
    ]


@user_api.route("/reset", methods=["PATCH"])
@json(admin_only=True)
def reset(data: dict):
    """
    Reset the password of an user
    :param data: The json payload as dict.
    :return: A http response containing the new password
    """

    uuid: str = data.get("uuid")

    if not uuid:
        return 400

    user: User = User.query.filter_by(uuid=uuid).first()

    if not user:
        return 404

    if user.admin:
        return 403

    password: str = User.generate_password()

    user.update(password)

    return {
        "password": password
    }
