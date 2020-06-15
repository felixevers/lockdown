from os import environ
from typing import Dict

defaults: Dict[str, any] = {
    # flask
    "FLASK_DEBUG": True,

    # mysql
    "MYSQL_HOSTNAME": "mysql",
    "MYSQL_PORT": 3306,  # default mysql port
    "MYSQL_DATABASE": "lockdown",
    "MYSQL_USERNAME": "lockdown",
    "MYSQL_PASSWORD": "lockdown",
    "MYSQL_CHARSET": "utf8mb4",  # recommended charset

    # sqlalchemy
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,

    # jwt
    "JWT_SECRET_KEY": "lockdown-secret",
    "JWT_TOKEN_LOCATION": ["cookies"],
    "JWT_COOKIE_DOMAIN": "lockdown.tld",
}

config: Dict[str, any] = {}

# Iterate over defaults keys to set the config depends on the environment variable exists or not.
for key in defaults.keys():
    if key in environ:
        config[key] = environ.get(key)
    else:
        config[key] = defaults[key]
