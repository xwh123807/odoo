import os
import zipfile
import tempfile
import shutil
from os.path import join


def listdir(dir, recursive=False):
    dir = os.path.normpath(dir)
    if not recursive:
        return os.listdir(dir)

    res = []
    for root, dirs, files in walksymlinks(dir):
        root = root[len(dir) + 1:]
        res.extend([join(root, f) for f in files])
    return res


def walksymlinks(top, topdown=True, onerror=None):
    for dirpath, dirnames, filenames in os.walk(top, topdown, onerror):
        if topdown:
            yield dirpath, dirnames, filenames

        symlinks = (dirname for dirname in dirnames if os.path.islink(os.path.join(dirpath, dirname)))
        for s in symlinks:
            for x in walksymlinks(os.path.join(dirpath, s), topdown, onerror):
                yield x

        if not topdown:
            yield dirpath, dirnames, filenames


def tempdir():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


def zip_dir(path, stream, include_dir=True, fnct_sort=None):
    path = os.path.normpath(path)
    len_prefix = len(os.path.dirname(path)) if include_dir else len(path)
    if len_prefix:
        len_prefix += 1

    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        for dirpath, dirnames, filenames in os.walk(path):
            filenames = sorted(filenames, key=fnct_sort)
            for fname in filenames:
                bname, ext = os.path.splitext(fname)
                ext = ext or bname
                if ext not in ['.pyc', '.pyo', '.swp', '.DS_Store']:
                    path = os.path.normpath(os.path.join(dirpath, fname))
                    if os.path.isfile(path):
                        zipf.write(path, path[len_prefix:])
