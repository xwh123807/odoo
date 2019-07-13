from .command import Command


def check_root_user():
    pass


def check_postgres_user():
    pass


def report_configuration():
    pass


def rm_pid_file(main_pid):
    pass


def setup_pid_file():
    pass


def export_translation():
    pass


def import_translation():
    pass


def main(args):
    pass


class Server(Command):
    """ Start the odoo server (default command) """

    def run(self, args):
        main(args)
