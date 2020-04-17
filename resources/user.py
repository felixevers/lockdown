from flask import Blueprint
from typing import Dict, Optional
from utils.json import json
from models.user import User

user_api = Blueprint("user", __name__)


@user_api.route("/create", methods=["POST"])
@json()
def create(data: dict) -> (Dict[str, any], Optional[int]):
    """
    Creates a user by name and password
    :param data: The json payload as dict.
    :return: A http response containing the user information
    """
    name: str = data.get("name")
    password: str = data.get("password")

    if not name or not password:
        return {}, 400

    print(password, User.get_password_security_level(password))

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
