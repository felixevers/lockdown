from functools import wraps
from typing import Callable
from flask import request, abort, jsonify
from models.user import User
from utils.user import get_user


def json(*, pass_user: bool = False, admin_only: bool = False, pass_data: bool = True, dict_only: bool = True,
         encode_json: bool = True) -> Callable:
    """
    This wrapper checks http requests for valid json.
    If the http request contains no valid json the payload will be set to empty dict.
    This wrapper will call the wrapped function with an attribute named `json` containing the payload.
    The function return will send a valid json http response with status code 200 - ok.
    :param pass_user: Whether the session user should be passed to the wrapped function.
    :param admin_only: Whether the session user have to an administrator.
    :param pass_data: Whether the request payload should be passed to the wrapped function.
    :param encode_json: Whether the returned data have to be encoded as json. Default: True
    :param dict_only: Whether the json payload must be a dict or any kind of data. Default: True
    :returns: The json wrapper
    """

    def _json(f: ()) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs) -> any:
            if pass_user or admin_only:
                user: User = get_user(admin=admin_only)

                if pass_user:
                    kwargs["user"] = user

            if pass_data:
                payload: any = request.json or {}

                if dict_only and not isinstance(payload, dict):
                    abort(400, "only json objects allowed")

                kwargs["data"] = payload

            result: any = f(**kwargs)

            if isinstance(result, int):
                return jsonify({}), result
            elif encode_json:
                return jsonify(result), 200

            return result

        return wrapper

    return _json
