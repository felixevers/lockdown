from api import db
from uuid import uuid4
from typing import Optional, List
from models.permission import Permission
from models.group_permission import GroupToPermission
from models.group_user import GroupToUser
from models.user import User


class Group(db.Model):
    """
    The group database model containing the basic information (below).
    """

    uuid: str = db.Column(db.String(36), primary_key=True, unique=True)
    name: str = db.Column(db.String(255), nullable=False, unique=True)

    def grant_permission(self, permission: Permission) -> Optional["GroupToPermission"]:
        """
        Grants a permission to this group.
        :param permission: The permission to grant
        :return: The association object or nothing is this group already has the given permission.
        """

        if GroupToPermission.query.filter_by(group=self.uuid, permission=permission.uuid).count() > 0:
            return None

        group_permission: GroupToPermission = GroupToPermission(group=self.uuid, permission=permission.uuid)

        db.session.add(group_permission)
        db.session.commit()

        return group_permission

    def revoke_permission(self, permission: Permission) -> bool:
        """
        Revokes a permission from this group.
        :param permission: The permission to revoke
        :return: The result whether the permission could be revoked.
        """

        group_permission: Optional[GroupToPermission] = GroupToPermission.query. \
            filter_by(group=self.uuid, permission=permission.uuid).first()

        if not group_permission:
            return False

        db.session.delete(group_permission)
        db.session.commit()

        return True

    def get_permissions(self) -> List[Permission]:
        """
        Gets all permission granted to this group.
        :return: A list with all granted permission.
        """

        return [*map(lambda group_permission: group_permission.permission,
                     GroupToPermission.query.filter_by(group=self.uuid).all())]

    def check_permission(self, permission: Permission) -> bool:
        """
        Checks if the this group owns a certain permission.
        :param permission: The permission to check
        :return: The result whether the given permission is granted to this group or not.
        """

        return GroupToPermission.query.filter_by(group=self.uuid, permission=permission.uuid).count() > 1

    def add_user(self, user: User) -> Optional[GroupToUser]:
        """
        Adds a given user to this group.
        :param user: The user to add
        :return: The association object or nothing is this user is already a member of this group.
        """

        if GroupToUser.query.filter_by(group=self.uuid, user=user.uuid).count() > 0:
            return None

        group_user: GroupToUser = GroupToUser(group=self.uuid, user=user.uuid)

        db.session.add(group_user)
        db.session.commit()

        return group_user

    def remove_user(self, user: User) -> bool:
        """
        Removes a certain user from this group.
        :param user: A group member
        :return: The result whether the group member could removed or not.
        """

        group_user: GroupToUser = Group.query.filter_by(group=self.uuid, user=user.uuid).first()

        if not group_user:
            return False

        db.session.delete(group_user)
        db.session.commit()

        return True

    def get_users(self) -> List[User]:
        """
        Gets all members of this group.
        :return: A member list of this group.
        """

        return [User.query.filter_by(uuid=user).all() for user in GroupToUser.query.filter_by(group=self.uuid).all()]

    @staticmethod
    def create(name: str) -> Optional["Group"]:
        """
        Creates a new group.
        :param name: The wanted group name
        :return: The new group or nothing if the name already exists.
        """

        if Group.query.filter_by(name=name).count() > 0:
            return None

        uuid: str = str(uuid4())

        group: Group = Group(uuid=uuid, name=name)

        db.session.add(group)
        db.session.commit()

        return group
