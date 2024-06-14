from .helpers import *

COMMAND = 'uniws hw action'
CMD = 'hwa'
HELP = 'Perform a workspace-specific action.'


def check_0000(capfd, cmd):
    # Outside.
    check_setup()
    sh(f'{cmd} -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        f'{COMMAND} [ARGS]...\n'
        f'\n'
        f'{HELP}\n'
        f'\n'
        f'Positional arguments:\n'
        f'  [ARGS]...    Arguments for the action.\n'
        f'\n'
        f'Optional arguments:\n'
        f'  -h/--help    Show the help text and exit.\n'
        f'\n'
    )
    sh(f'{cmd}', chk=False)
    out, err = capfd.readouterr()
    assert err == 'This command must be run inside a workspace.\n'
    assert out == ''


def test_0000(capfd):
    check_0000(capfd, COMMAND)
    check_0000(capfd, CMD)


def check_0001(capfd, cmd):
    dir = f'{dir_home()}/{os.path.basename(__file__)}_0001'
    check_setup(dir)
    sh(f'cd {dir} && {cmd} -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        f'{COMMAND} [ARGS]...\n'
        f'\n'
        f'{HELP}\n'
        f'\n'
        f'Positional arguments:\n'
        f'  [ARGS]...    Arguments for the action.\n'
        f'\n'
        f'Optional arguments:\n'
        f'  -h/--help    Show the help text and exit.\n'
        f'\n'
    )
    sh(f'cd {dir} && {cmd}')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        'Action: \n'
    )
    sh(f'cd {dir} && {cmd} 1 "a b c" -e')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        'Action: \n'
        'Argument: 1\n'
        'Argument: a b c\n'
        'Argument: -e\n'
    )


def test_0001(capfd):
    check_0001(capfd, COMMAND)
    check_0001(capfd, CMD)


def check_0002(capfd, cmd):
    # Component.
    filename = os.path.basename(__file__).split('.')[0]
    dir = f'{dir_home()}/{filename}_0002'
    check_setup(dir, f'{os.path.dirname(__file__)}/{filename}/0002')
    sh(f'cd {dir} && {cmd} -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        f'{COMMAND} ACTION [ARGS]...\n'
        f'\n'
        f'{HELP}\n'
        f'\n'
        f'Positional arguments:\n'
        f'  ACTION       The action to perform.\n'
        f'               Allowed values:\n'
        f'                * action1\n'
        f'                * action2 - the second action\n'
        f'  [ARGS]...    Arguments for the action.\n'
        f'\n'
        f'Optional arguments:\n'
        f'  -h/--help    Show the help text and exit.\n'
        f'\n'
    )
    sh(f'cd {dir} && {cmd} action1')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        'Action: action1\n'
    )
    sh(f'cd {dir} && {cmd} action2 1 "2 3"')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        'Action: action2\n'
        'Argument: 1\n'
        'Argument: 2 3\n'
    )


def test_0002(capfd):
    check_0002(capfd, COMMAND)
    check_0002(capfd, CMD)
