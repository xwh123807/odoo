import logging
import os
import subprocess
from collections import defaultdict, Mapping
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


def _fileopen(path, mode, basedir, pathinfo, basename=None):
    pass


def flatten(list):
    pass


def reverse_enumerate(l):
    pass


def partition(pred, elems):
    pass


def topological_sort(elems):
    pass


def to_xml(s):
    pass


def get_iso_codes(lang):
    pass


def scan_languages():
    pass


def get_user_companies(cr, user):
    pass


def mod10r(number):
    pass


def str2bool(s, default=None):
    pass


def human_size(sz):
    pass


def logged(f):
    pass


class profile(object):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


def detect_ip_addr():
    pass


def posix_to_ldml(fmt, locale):
    pass


def split_every(n, iterable, piece_maker=tuple):
    pass


def get_and_group_by_field(cr, uid, obj, ids, field, context=None):
    pass


def get_and_group_by_company(cr, uid, obj, ids, context=None):
    pass


def resolver_attr(obj, attr):
    pass


def attrgetter(*items):
    pass


def remove_accents(input_str):
    pass


class unquote(str):
    def __repr__(self):
        pass


class UnquoteEvalContext(defaultdict):
    def __init__(self):
        pass

    def __missing__(self, key):
        pass


class mute_logger(object):
    def __init__(self):
        pass

    def filter(self, record):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self, *args, **kwargs):
        pass


class CountingStream(object):
    def __init__(self):
        pass

    def __iter__(self):
        pass

    def __next__(self):
        pass


def stripped_sys_argv(*strip_args):
    pass


class ConstantMapping(Mapping):
    def __init__(self):
        pass

    def __len__(self):
        pass

    def __iter__(self):
        pass

    def __getitem__(self, item):
        pass


def dumpstacks(sig=None, frame=None):
    pass


def freehash(arg):
    pass


def clean_context(context):
    pass


class frozendict(dict):
    pass


class Collector(Mapping):
    pass


class StackMap(MutableMapping)
    pass


class OrderedSet(MutableSet):
    pass


class LastOrderedSet(OrderedSet):
    pass


def groupby(iterable, key=None):
    pass


def unique(it):
    pass


class Reverse(object):
    pass


def ignore(*exec):
    pass


def formatLang():
    pass


def formatDate():
    pass


def wrap_module(module, attr_list):
    pass
