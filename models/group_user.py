from api import db


class GroupToUser(db.Model):
    """
    The association table between group and user.
    """

    group_id: str = db.Column(db.String(36), db.ForeignKey("group.uuid"), primary_key=True, unique=True)
    user_id: str = db.Column(db.String(36), db.ForeignKey("user.uuid"), primary_key=True, unique=True)

    group = db.relationship('Group', backref=db.backref('group_user_group', remote_side='Group.uuid'))
    user = db.relationship('User', backref=db.backref('group_user_user', remote_side='User.uuid'))
