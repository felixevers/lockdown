from api import db


class GroupToUser(db.Model):
    """
    The association table between group and user.
    """
    group: db.Column = db.Column(db.String(36), db.ForeignKey("group.uuid"), primary_key=True, unique=True)
    user: db.Column = db.Column(db.String(36), db.ForeignKey("user.uuid"), primary_key=True, unique=True)
