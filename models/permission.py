from api import db
from uuid import uuid4
from typing import Optional
from models.application import Application


class Permission(db.Model):
    """
    The permission database model containing the basic information (below).
    """

    uuid: db.Column = db.Column(db.String(36), primary_key=True, unique=True)
    name: db.Column = db.Column(db.String(255), nullable=False, unique=True)
    application: db.Column = db.Column(db.String(36), db.ForeignKey("application.uuid"), nullable=False)

    @staticmethod
    def create(name: str, application: Application) -> Optional["Permission"]:
        """
        Creates a new permission for an certain application.
        :param name: The wanted name
        :param application: The associated application for the permission
        :return: The new permission or nothing if the permission name already exists.
        """

        if Permission.query.filter_by(name=name).count() > 0:
            return None

        uuid: str = str(uuid4())

        permission: Permission = Permission(uuid=uuid, name=name, application=application.uuid)

        db.session.add(permission)
        db.session.commit()

        return permission
