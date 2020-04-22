from flask import Blueprint, jsonify, Response
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, create_access_token, create_refresh_token, \
    get_jwt_identity, unset_jwt_cookies, set_refresh_cookies, set_access_cookies
from utils.json import json
from models.user import User

auth_api = Blueprint("auth", __name__)


@auth_api.route("/login", methods=["POST"])
@json(encode_json=False)
def login(data: dict):
    """
    User logs in with name and password.
    :param data: The json payload as dict.
    :return: A http response containing the jwt access and refresh tokens.
    """

    name: str = data.get("name")
    password: str = data.get("password")

    if not name or not password:
        return {}, 400

    user: User = User.query.filter_by(name=name).first()

    if not user or not user.check(password):
        return {}, 401

    identity: dict = {
        "uuid": user.uuid,
        "name": user.name,
        "admin": user.admin,
    }

    access_token: str = create_access_token(identity, fresh=True)
    refresh_token: str = create_refresh_token(identity)

    response: Response = jsonify({})

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@auth_api.route("/refresh", methods=["PATCH"])
@json(encode_json=False)
@jwt_refresh_token_required
def refresh():
    """
    Regenerate a jwt access token by given refresh token.
    :return: A http response containing the jwt access.
    """

    identity: any = get_jwt_identity()

    if not isinstance(identity, dict):
        return 401

    access_token: str = create_access_token(identity, fresh=False)

    response: Response = jsonify({
        "access": access_token,
    })

    set_access_cookies(response, access_token)

    return response


@auth_api.route("/logout", methods=["DELETE"])
@json(encode_json=False)
@jwt_required
def logout():
    """
    Unset the given jwt cookies.
    :return: A http response deleting the jwt cookies.
    """

    response: Response = jsonify({
        "result": True
    })

    unset_jwt_cookies(response)

    return response
