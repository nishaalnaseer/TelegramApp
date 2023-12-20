from os import getenv


class Pool:
    def __init__(self):
        self._host = getenv("db-host")
        self._username = getenv("username")
        self._password = getenv("password")
        self._database = getenv("db-name")
        self._port = getenv("db-port")

    # async start_pool():