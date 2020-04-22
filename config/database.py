from config.environment import config
from logging import error
from sys import exit


def get_mysql_uri() -> str:
    """
    This function generates the mysql database uri based on the environment variables.
    :returns: The mysql database uri
    """

    # Getting username and password for authentication.
    username: str = config.get("MYSQL_USERNAME")
    password: str = config.get("MYSQL_PASSWORD")

    # Getting the mysql hostname.
    hostname: str = str(config.get("MYSQL_HOSTNAME"))
    # Setting mysql port to 0.
    port: int = 0

    # Parse the mysql port to int if possible.
    try:
        port = int(config.get("MYSQL_PORT"))
    except ValueError:
        pass

    # Checks whether mysql port is given and valid or logs error message.
    if not (port and 0 < port <= 49151):
        error("`{}` is not a valid value for `MYSQL_PORT`.\nBe sure to use an integer in range of 1-49151."
              .format(port))
        exit(1)

    # The mysql database
    database: str = str(config.get("MYSQL_DATABASE"))

    # The charset to be used
    charset: str = str(config.get("MYSQL_CHARSET"))

    # Build the uri for connection.
    uri: str = "mysql+pymysql://" + username + ":" + password + "@" + hostname + ":" + str(
        port) + "/" + database + "?charset=" + charset

    return uri
