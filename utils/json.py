from functools import wraps
from flask import request, abort, jsonify


def json(*, dict_only: bool = True, encode_json: bool = True) -> ():
    """
    This wrapper checks http requests for valid json.
    If the http request contains no valid json the payload will be set to empty dict.
    This wrapper will call the wrapped function with an attribute named `json` containing the payload.
    The function return will send a valid json http response with status code 200 - ok.
    :param encode_json: Whether the returned data have to be encoded as json. Default: True
    :param dict_only: Whether the json payload must be a dict or any kind of data. Default: True
    :returns: The json wrapper
    """

    def _json(f: ()) -> ():
        @wraps(f)
        def wrapper(*args, **kwargs) -> any:
            payload: any = request.json or {}

            if dict_only and not isinstance(payload, dict):
                abort(400, "only json objects allowed")

            result: any = f(data=payload)

            if encode_json:
                return jsonify(result), 200

            return result

        return wrapper

    return _json
