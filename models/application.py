from api import db
from uuid import uuid4
from typing import Optional


class Application(db.Model):
    """
    The application database model containing the basic information (below).
    """

    uuid: db.Column = db.Column(db.String(36), primary_key=True, unique=True)
    name: db.Column = db.Column(db.String(255), nullable=False, unique=True)
    token: db.Column = db.Column(db.String(36), nullable=False, unique=True)

    @staticmethod
    def create(name: str) -> Optional["Application"]:
        """
        Creates a new application.
        :param name: The wanted application name
        :return: The new application or nothing if the name already mapped to an application.
        """

        if Application.query.filter_by(name=name).count() > 0:
            return None

        uuid: str = str(uuid4())
        token: str = str(uuid4())

        application: Application = Application(uuid=uuid, name=name, token=token)

        db.session.add(application)
        db.session.commit()

        return application
