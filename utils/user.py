from typing import Optional
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User


@jwt_required
def get_user() -> Optional[User]:
    identity: any = get_jwt_identity()

    if not isinstance(identity, dict):
        abort(401)
        return None

    uuid: str = identity.get("uuid")

    if not uuid:
        abort(400)
        return None

    user: User = User.query(uuid=uuid).first()

    if not user:
        abort(400)
        return None

    return user
