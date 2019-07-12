import sys
import os

ENOENT = 2

windows = sys.platform.startswith('win')

defpath = os.environ.get('PATH', os.defpath).split(os.pathsep)

if windows:
    defpathext = ['']
else:
    defpathext = ['']


def which_files(file, mode=os.F_OK | os.X_OK, path=None, pathext=None):
    filepath, file = os.path.split(file)

    if filepath:
        path = (filepath,)
    elif path is None:
        path = defpath
    elif isinstance(path, str):
        path = path.split(os.path.split(os.pathsep))

    if pathext is None:
        pathext = defpathext
    elif isinstance(pathext, str):
        pathext = pathext.split(os.pathsep)

    if not '' in pathext:
        pathext.insert(0, '')

    for dir in path:
        basepath = os.path.join(dir, file)
        for ext in pathext:
            fullpath = basepath + ext
            if os.path.exists(fullpath) and os.access(fullpath, mode):
                yield fullpath


def which(file, mode=os.F_OK | os.X_OK, path=None, pathext=None):
    path = next(which_files(file, mode, path, pathext), None)
    if path is None:
        raise IOError(ENOENT, '%s not found' % (mode & os.X_OK and 'command' or 'file'), file)
    return path
