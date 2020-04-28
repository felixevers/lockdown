from api import db
from uuid import uuid4
from typing import Optional
from string import ascii_uppercase
from random import choices


class Application(db.Model):
    """
    The application database model containing the basic information (below).
    """

    uuid: str = db.Column(db.String(36), primary_key=True, unique=True)
    name: str = db.Column(db.String(255), nullable=False, unique=True)
    token: str = db.Column(db.String(64), nullable=False, unique=True)

    def regenerate_token(self) -> str:
        """
        Regenerate the token of this application.
        :return: The new token
        """
        self.token = Application.generate_token()
        db.session.commit()

        return self.token

    @staticmethod
    def generate_token() -> str:
        """
        Generate a new application token containing 64 characters.
        :return: The new token
        """
        return "".join(choices(ascii_uppercase, k=64))

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
        token: str = Application.generate_token()

        application: Application = Application(uuid=uuid, name=name, token=token)

        db.session.add(application)
        db.session.commit()

        return application
