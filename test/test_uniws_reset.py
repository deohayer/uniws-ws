from .helpers import *


def test_0000(capfd):
    # Availability.
    sh('uniws reset -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == \
        (''
         'uniws reset\n'
         '\n'
         'Manage app. Remove shortcuts and revert changes.\n'
         '\n'
         'Optional arguments:\n'
         '  -h/--help    Show the help text and exit.\n'
         '\n'
         '')


def test_0001(capfd):
    # Normal.
    path_dir = dir_uniws()
    path_uniws = f'{path_dir}/uniws'
    # Reset once.
    sh('uniws setup')
    out, err = capfd.readouterr()
    sh('uniws reset')
    out, err = capfd.readouterr()
    exp = ''
    # Check if PYTHON_ARGCOMPLETE_OK was removed.
    exp += f'Modify: {path_uniws}\n'
    with open(path_uniws) as file:
        assert '# PYTHON_ARGCOMPLETE_OK\n' not in file.readlines()
    # Check if the command abbreviations were removed.
    for abbr in ABBRS:
        assert not os.path.exists(f'{path_dir}/{abbr}')
        exp += f'Remove: {path_dir}/{abbr}\n'
    assert err == ''
    assert out == exp


def test_0002(capfd):
    # Repeat.
    path_dir = dir_uniws()
    # Reset twice.
    sh('uniws reset')
    out, err = capfd.readouterr()
    sh('uniws reset')
    out, err = capfd.readouterr()
    exp = ''
    # Check if the command abbreviations were ignored.
    for abbr in ABBRS:
        exp += f'Ignore: {path_dir}/{abbr}\n'
    assert err == ''
    assert out == exp
