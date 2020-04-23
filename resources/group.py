from flask import Blueprint
from models.group import Group
from utils.json import json

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
        return 400

    return {
        "uuid": group.uuid,
        "name": group.name,
    }
