import sys

import myfly


class Server:
    def __init__(self):
        pass

    def server(self):
        rc = myfly.service.server.start()
        sys.exit(rc)
