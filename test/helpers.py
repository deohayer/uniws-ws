import os
import sys
import pytest
from uniws.shell import sh
from uniws.app import ABBRS


def assert_fs_entry(path: 'str', mode: 'int', pred) -> 'None':
    assert os.path.exists(path)
    assert pred(path)
    stmode = os.stat(path).st_mode
    assert (mode & (1 << 0)) <= (stmode & (1 << 0))
    assert (mode & (1 << 1)) <= (stmode & (1 << 1))
    assert (mode & (1 << 2)) <= (stmode & (1 << 2))
    assert (mode & (1 << 3)) <= (stmode & (1 << 3))
    assert (mode & (1 << 4)) <= (stmode & (1 << 4))
    assert (mode & (1 << 5)) <= (stmode & (1 << 5))
    assert (mode & (1 << 6)) <= (stmode & (1 << 6))
    assert (mode & (1 << 7)) <= (stmode & (1 << 7))
    assert (mode & (1 << 8)) <= (stmode & (1 << 8))


def dir_uniws() -> 'str':
    return os.path.dirname(sh('which uniws', cap=True).out.strip())


def dir_home() -> 'str':
    return os.getenv('HOME')


def check_setup(dir: 'str' = '', overlay: 'str' = ''):
    sh('uniws setup', cap=True)
    if overlay:
        cmdcp = f'cp -RaT {overlay} {dir}'
    else:
        cmdcp = 'true'
    if dir:
        sh(f'true'
           f' && rm -rf {dir}'
           f' && mkdir -p {dir}'
           f' && uniws init {dir}'
           f' && {cmdcp}'
           f';')
