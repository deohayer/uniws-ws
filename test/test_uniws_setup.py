from .helpers import *


def test_0000(capfd):
    # Availability.
    sh('uniws setup -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == \
        (''
         'uniws setup\n'
         '\n'
         'Manage app. Add shortcuts and completion.\n'
         '\n'
         'Optional arguments:\n'
         '  -h/--help    Show the help text and exit.\n'
         '\n'
         '')


def test_0001(capfd):
    # Normal.
    path_dir = dir_uniws()
    path_uniws = f'{path_dir}/uniws'
    # Setup once.
    sh('uniws reset')
    out, err = capfd.readouterr()
    sh('uniws setup')
    out, err = capfd.readouterr()
    exp = f'Modify: {path_uniws}\n'
    # Check if PYTHON_ARGCOMPLETE_OK was added.
    with open(path_uniws) as file:
        assert '# PYTHON_ARGCOMPLETE_OK\n' in file.readlines()
    # Check if all command abbreviations were created.
    for abbr in ABBRS:
        path_abbr = f'{path_dir}/{abbr}'
        assert_fs_entry(path_abbr, 0o755, os.path.isfile)
        exp += f'Create: {path_dir}/{abbr}\n'
    assert err == ''
    assert out == exp


def test_0002(capfd):
    # Repeat.
    path_dir = dir_uniws()
    path_uniws = f'{path_dir}/uniws'
    # Setup twice.
    sh('uniws reset')
    out, err = capfd.readouterr()
    sh('uniws setup')
    out, err = capfd.readouterr()
    sh('uniws setup')
    out, err = capfd.readouterr()
    exp = ''
    # Check if another PYTHON_ARGCOMPLETE_OK was not added.
    with open(path_uniws) as file:
        count = 0
        lines = file.readlines()
        for i in range(len(lines)):
            if '# PYTHON_ARGCOMPLETE_OK\n' == lines[i]:
                count += 1
        assert count == 1
    # Check if all command abbreviations were ignored.
    for abbr in ABBRS:
        exp += f'Ignore: {path_dir}/{abbr}\n'
    assert err == ''
    assert out == exp
