from api import db


class GroupToPermission(db.Model):
    """
    The association table between group and permission.
    """

    group_id: str = db.Column(db.String(36), db.ForeignKey("group.uuid"), primary_key=True, unique=True)
    permission_id: str = db.Column(db.String(36), db.ForeignKey("permission.uuid"), primary_key=True, unique=True)

    group = db.relationship('Group', backref=db.backref('group_permission_group', remote_side='Group.uuid'))
    permission = db.relationship('Permission',
                                 backref=db.backref('group_permission_permission', remote_side='Permission.uuid'))
