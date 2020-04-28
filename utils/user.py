from typing import Optional
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User


@jwt_required
def get_user(*, admin: bool = False) -> Optional[User]:
    """
    Get the user object by jwt identity.
    :param admin: If only admin users allowed (default: false)
    :return: The user object or nothing if the user dont fulfills the requirements
    """

    identity: any = get_jwt_identity()

    if not isinstance(identity, dict):
        abort(401)
        return None

    uuid: str = identity.get("uuid")

    if not uuid:
        abort(400)
        return None

    user: User = User.query.filter_by(uuid=uuid).first()

    if not user:
        abort(400)
        return None

    if admin and not user.admin:
        abort(403)

    return user
