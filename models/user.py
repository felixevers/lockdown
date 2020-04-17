from api import db
from uuid import uuid4
from flask_bcrypt import check_password_hash, generate_password_hash
from typing import Optional, Dict
from models.permission import Permission
from models.group_user import GroupToUser
from random import choices
from string import ascii_letters
import logging


class User(db.Model):
    """
    The user database model containing the basic information (below).
    """

    uuid: db.Column = db.Column(db.String(36), primary_key=True, unique=True)
    name: db.Column = db.Column(db.String(255), nullable=False, unique=True)
    password: db.Column = db.Column(db.String(255), nullable=False)
    admin: db.Column = db.Column(db.Boolean, nullable=False, default=False)

    def check(self, password: str) -> None:
        """
        Checks if the given password equal to the user password.
        :param password: The password to check
        :return: Nothing
        """
        return check_password_hash(self.password, password)

    def update(self, password: str) -> None:
        """
        Updates the password of this user.
        :param password: The wanted new password.
        :return: Nothing
        """
        self.password = generate_password_hash(password)

        db.session.commit()

    def check_permission(self, permission: Permission) -> bool:
        """
        Checks if the user has a certain permission.
        :param permission: The permission to check
        :return: Whether the user has this permission
        """
        return any(
            group.first().check_permission(permission) for group in GroupToUser.query.filter_by(user=self.uuid).all())

    @staticmethod
    def create(name: str, password: str, *, admin: bool = False) -> Optional["User"]:
        """
        Inserts a new user into the database.
        :param name: The wanted name
        :param password: The wanted password
        :param admin: Whether the new user should be an administrator or not
        :return: The new user or nothing if the wanted name is not available
        """
        if User.query.filter_by(name=name).count() > 0:
            return None

        uuid: str = str(uuid4())
        password: str = generate_password_hash(password)

        user: User = User(uuid=uuid, name=name, password=password, admin=admin)

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def get_password_security_level(password: str) -> int:
        """
        Rates a password by the following criteria:
        - lowercase
        - uppercase
        - number
        - special char
        - length above 8
        - length above 16
        - length above 32
        - length above 64
        If the password fulfills one of this criteria the security level will be increased by one.
        :param password: The password to check
        :return: The security level of the given password.
        """
        criteria: Dict[str, bool] = {
            "lowercase": False,
            "uppercase": False,
            "number": False,
            "special_char": False,
            "length_above_8": False,
            "length_above_16": False,
            "length_above_32": False,
            "length_above_64": False,
        }

        for char in password:
            if char.islower():
                criteria["lowercase"] = True
            elif char.isupper():
                criteria["uppercase"] = True
            elif char.isdigit():
                criteria["number"] = True
            elif not char.isalnum():
                criteria["special_char"] = True

        if len(password) > 8:
            criteria["length_above_8"] = True
        if len(password) > 16:
            criteria["length_above_16"] = True
        if len(password) > 32:
            criteria["length_above_32"] = True
        if len(password) > 64:
            criteria["length_above_64"] = True

        return sum(criteria.values())

    @staticmethod
    def init() -> None:
        """
        Create a user with admin privileges if it not exists.
        :return: Nothing
        """
        if User.query.filter_by(admin=True).count() == 0:
            name: str = "admin"
            password: str = "".join(choices(ascii_letters, k=16))
            User.create(name, password, admin=True)

            logging.warning(" NO USER WITH ADMIN PRIVILEGES FOUND ".center(100, "#"))
            logging.warning("created new administrator".center(100))
            logging.warning(f"{name}:{password}".center(100))
            logging.warning("#" * 100)
