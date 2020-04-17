from api import db


class GroupToPermission(db.Model):
    """
    The association table between group and permission.
    """
    group: db.Column = db.Column(db.String(36), db.ForeignKey("group.uuid"), primary_key=True, unique=True)
    permission: db.Column = db.Column(db.String(36), db.ForeignKey("permission.uuid"), primary_key=True, unique=True)
