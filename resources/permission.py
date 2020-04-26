from flask import Blueprint
from models.application import Application
from models.permission import Permission
from models.group import Group
from models.group_permission import GroupToPermission
from utils.json import json
from api import db

permission_api = Blueprint("permission", __name__)


@permission_api.route("/create", methods=["POST"])
@json(admin_only=True)
def create(data: dict):
    """
    Creates a new permission by passed name and application uuid.
    :param data: The json payload as dict.
    :return: A http response containing the new permission.
    """

    application_uuid: str = data.get("application")
    name: str = data.get("name")

    if not application_uuid or not name:
        return 400

    application: Application = Application.query.filter_by(uuid=application_uuid).first()

    if not application:
        return 404

    permission: Permission = Permission.create(name, application.uuid)

    if not permission:
        return 400

    return {
        "name": permission.name,
        "application": application.uuid,
    }


@permission_api.route("/delete", methods=["DELETE"])
@json(admin_only=True)
def delete(data: dict):
    """
    Deletes a permission by passed uuid.
    :param data: The json payload as dict.
    :return: A http response containing the result.
    """

    uuid: str = data.get("uuid")

    if not uuid:
        return 400

    permission: Permission = Permission.query.filter_by(uuid=uuid).first()

    if not permission:
        return 404

    db.session.remove(permission)
    db.session.commit()

    return {}


@permission_api.route("/list", methods=["GET"])
@json(admin_only=True)
def list(data: dict):
    """
    Lists all permissions by passed application.
    :param data: The json payload as dict.
    :return: A http response containing the granted permissions.
    """

    application_uuid: str = data.get("application")

    if not application_uuid:
        return 400

    application: Application = Application.query.filter_by(uuid=application_uuid).first()

    if not application:
        return 404

    return [
        {
            "uuid": permission.uuid,
            "name": permission.name,
            "application": application.uuid,
        }
        for permission in Permission.query.filter_by(uuid=application.uuid).all()
    ]


@permission_api.route("/grant", methods=["PUT"])
@json(admin_only=True)
def grant(data: dict):
    """
    Grant a permissions to a group.
    :param data: The json payload as dict.
    :return: A http response containing the result.
    """

    group_uuid: str = data.get("group")
    permission_uuid: str = data.get("permission")

    if not group_uuid or not permission_uuid:
        return 400

    group: Group = Group.query.filter_by(uuid=group_uuid).first()
    permission: Permission = Permission.query.filter_by(uuid=permission_uuid).first()

    if not group or not permission:
        return 404

    group_permission: GroupToPermission = group.grant_permission(permission)

    if not group_permission:
        return 400

    return {
        "group": group.uuid,
        "permission": permission,
    }


@permission_api.route("/revoke", methods=["DELETE"])
@json(admin_only=True)
def revoke(data: dict):
    """
    Revoke a permissions from a group.
    :param data: The json payload as dict.
    :return: A http response containing the result.
    """

    group_uuid: str = data.get("group")
    permission_uuid: str = data.get("permission")

    if not group_uuid or not permission_uuid:
        return 400

    group: Group = Group.query.filter_by(uuid=group_uuid).first()
    permission: Permission = Permission.query.filter_by(uuid=permission_uuid).first()

    if not group or not permission:
        return 404

    result: bool = group.revoke_permission(permission)

    if not result:
        return 400

    return {}
