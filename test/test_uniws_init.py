from .helpers import *


def assert_layout(dir: 'str'):
    files = {
        f'.uniws/__init__.py': 0o644,
        f'.uniws/.bashrc': 0o644,
        f'.uniws/hardware.py': 0o644,
        f'.uniws/hwc.sh': 0o755,
        f'.uniws/hwp.sh': 0o755,
        f'.uniws/hws.sh': 0o755,
        f'.uniws/hwu.sh': 0o755,
        f'.uniws/hwd.sh': 0o755,
        f'.uniws/hwa.sh': 0o755,
        f'.uniws/software.py': 0o644,
        f'.uniws/swf.sh': 0o755,
        f'.uniws/swb.sh': 0o755,
        f'.uniws/swi.sh': 0o755,
        f'.uniws/swt.sh': 0o755,
        f'.uniws/swc.sh': 0o755,
        f'.uniws/swa.sh': 0o755,
        f'.gitattributes': 0o644,
        f'.gitignore': 0o644,
        f'.gitmodules': 0o644,
        f'README.md': 0o644,
    }
    assert_fs_entry(f'{dir}/.uniws', 0o755, os.path.isdir)
    actual = []
    actual.extend(os.listdir(dir))
    actual.extend(f'.uniws/{x}' for x in os.listdir(f'{dir}/.uniws'))
    actual.remove('.uniws')
    for x in actual:
        assert x in files
    for x in files:
        assert_fs_entry(f'{dir}/{x}', files[x], os.path.isfile)


def test_0000(capfd):
    # Availability.
    sh('uniws init -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == \
        (''
         'uniws init [DIR]\n'
         '\n'
         'Initialize a new workspace.\n'
         '\n'
         'Positional arguments:\n'
         '  [DIR]    Empty or non-existent directory. Defaults to current.\n'
         '\n'
         'Optional arguments:\n'
         '  -h/--help    Show the help text and exit.\n'
         '\n'
         '')


def test_0001(capfd):
    # Current.
    dir = f'{dir_home()}/test_uniws_init'
    sh(f'true'
       f' && rm -rf {dir}'
       f' && mkdir -p {dir}'
       f' && cd {dir}'
       f' && uniws init'
       f';')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == ''
    assert_layout(dir)


def test_0002(capfd):
    # Direct.
    dir = f'{dir_home()}/test_uniws_init'
    sh(f'true'
       f' && rm -rf {dir}'
       f' && mkdir -p {dir}'
       f' && uniws init {dir}'
       f';')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == ''
    assert_layout(dir)


def test_0003(capfd):
    # Nested.
    dir = f'{dir_home()}/test_uniws/init'
    sh(f'true'
       f' && rm -rf {os.path.dirname(dir)}'
       f' && mkdir -p {dir}'
       f' && uniws init {dir}'
       f';')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == ''
    assert_layout(dir)


def test_0004(capfd):
    # Not empty.
    dir = f'{dir_home()}/test_uniws_init'
    file = f'{dir}/file'
    sh(f'true'
       f' && rm -rf {dir}'
       f' && mkdir -p {dir}'
       f' && touch {file}'
       f' && uniws init {dir}'
       f';', chk=False)
    out, err = capfd.readouterr()
    assert err == f'The directory is not empty: {dir}\n'
    assert out == ''
    assert len(os.listdir(dir)) == 1
    assert_fs_entry(file, 0o644, os.path.isfile)


def test_0005(capfd):
    # Not a directory.
    file = f'{dir_home()}/test_uniws_init'
    sh(f'true'
       f' && rm -rf {file}'
       f' && touch {file}'
       f' && uniws init {file}'
       f';', chk=False)
    out, err = capfd.readouterr()
    assert err == f'Not a directory: {file}\n'
    assert out == ''
    assert_fs_entry(file, 0o644, os.path.isfile)
