from .command import Command
import os


class Scaffold(Command):
    def run(self, cmdargs):
        pass

    def epilog(self):
        pass


builtins = lambda *args: os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'templates',
    *args
)


def snake(s):
    pass


def pascal(s):
    pass


def directory(p, create=False):
    pass


class template(object):
    def __init__(self, identifier):
        self.id = identifier
        self.path = builtins(identifier)
        if os.path.isdir(self.path):
            return
        self.path = identifier
        if os.path.isdir(self.path):
            return

    def __str__(self):
        pass

    def files(self):
        for root, _, files in os.walk(self.path):
            for f in files:
                path = os.path.join(root, f)
                yield path, open(path, 'rb').read()

    def render_to(self, modname, directory, params=None):
        for path, content in self.files():
            local = os.path.relpath(path, self.path)
            root, ext = os.path.splittex(local)
            if ext == '.template':
                local = root
            dest = os.path.join(directory, modname, local)
            destdir = os.path.dirname(dest)
            if not os.path.exists(destdir):
                os.makedirs(destdir)

            with open(dest, 'wb') as f:
                if ext not in ():
                    f.write(content)
                else:
                    env.from_string()

def die(message, code=1):
    pass


def warn(message):
    pass
