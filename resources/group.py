from flask import Blueprint
from models.group import Group
from utils.json import json
from api import db

group_api = Blueprint("group", __name__)


@group_api.route("/create", methods=["POST"])
@json(admin_only=True)
def create(data: dict):
    """
    Creates a new group by passed name.
    :param data: The json payload as dict.
    :return: A http response containing the new group data.
    """

    name: str = data.get("name")

    if not name:
        return 400

    group: Group = Group.create(name)

    if not group:
        return 404

    return {
        "uuid": group.uuid,
        "name": group.name,
    }


@group_api.route("/delete", methods=["DELETE"])
@json(admin_only=True)
def delete(data: dict):
    """
    Deletes a group by passed uuid.
    :param data: The json payload as dict.
    :return: A http response containing the result.
    """

    uuid: str = data.get("uuid")

    if not uuid:
        return 400

    group: Group = Group.query.filter_by(uuid=uuid).first()

    if not group:
        return 404

    db.session.remove(group)
    db.session.commit()

    return {}


@group_api.route("/all", methods=["GET"])
@json(admin_only=True, pass_data=False)
def list_all():
    """
    Lists all existing groups.
    :return: A http response containing all groups.
    """

    return [
        {
            "uuid": group.uuid,
            "name": group.name,
        }
        for group in Group.query.all()
    ]


@group_api.route("/update/name", methods=["PATCH"])
@json(admin_only=True, pass_data=True)
def update_name(data: dict):
    """
    Update the name of a existing group.
    :param data: The json payload as dict.
    :return: A http response containing the result.
    """

    uuid: str = data.get("uuid")
    name: str = data.get("name")

    if not uuid or not name:
        return 400

    group: Group = Group.query.filter_by(uuid=uuid).first()

    if not group:
        return 404

    group.name = name
    db.session.commit()

    return {
        "result": True,
    }
