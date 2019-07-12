import logging
import os
import subprocess
from .which import which

_logger = logging.getLogger(__name__)


def find_in_path(name):
    path = os.environ.get('PATH', os.defpath).split(os.pathsep)
    return which(name, path=os.pathsep.join(path))


def _exec_pipe(prog, args, env=None):
    cmd = (prog,) + args
    close_fds = os.name == "posix"
    pop = subprocess.Popen(cmd, bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=close_fds, env=env)
    return pop.stdin, pop.stdout


def exec_command_pipe(name, *args):
    prog = find_in_path(name)
    if not prog:
        raise Exception('Command "%s" not found. ' % name)
    return _exec_pipe(prog, args)


def find_pg_tool(name):
    path = None
    try:
        return which(name, path=path)
    except IOError:
        raise Exception('Command "%s" not found.' % name)


def exec_pg_environ():
    env = os.environ.copy()
    env['PGHOST'] = None
    env['PGPORT'] = None
    env['PGUSER'] = None
    env['PGPASSWORD'] = None
    return env


def exec_pg_command(name, *args):
    prog = find_pg_tool(name)
    env = exec_pg_environ()
    with open(os.devnull) as dn:
        args2 = (prog,) + args
        rc = subprocess.call(args2, env=env, stdout=dn, stderr=subprocess.STDOUT)
        if rc:
            raise Exception('progress subprocess %s error %s' % (args2, rc))


def exec_pg_comand_pipe(name, *args):
    prog = find_pg_tool(name)
    env = exec_pg_environ()
    return _exec_pipe(prog, args, env)

def file_open(name, mode="r", subdir="addons", pathinfo=False):
    basename = name
    if os.path.isabs(name):
        name = os.path.normcase(os.path.normpath(name))
