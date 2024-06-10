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
        f'{COMMAND}\n'
        f'\n'
        f'{HELP}\n'
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
    # Implicit.
    dir = f'{dir_home()}/{os.path.basename(__file__)}_0001'
    check_setup(dir)
    sh(f'cd {dir} && {cmd} -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        f'{COMMAND}\n'
        f'\n'
        f'{HELP}\n'
        f'\n'
        f'Optional arguments:\n'
        f'  -h/--help    Show the help text and exit.\n'
        f'\n'
    )
    sh(f'cd {dir} && {cmd}')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == 'Hardware: \n'


def test_0001(capfd):
    check_0001(capfd, COMMAND)
    check_0001(capfd, CMD)


def check_0002(capfd, cmd):
    # Explicit.
    filename = os.path.basename(__file__).split('.')[0]
    dir = f'{dir_home()}/{filename}_0002'
    check_setup(dir, f'{os.path.dirname(__file__)}/{filename}/0002')
    sh(f'cd {dir} && {cmd} -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        f'{COMMAND} HW\n'
        f'\n'
        f'{HELP}\n'
        f'\n'
        f'Positional arguments:\n'
        f'  HW    A hardware to use.\n'
        f'        Allowed values:\n'
        f'         * hardware1\n'
        f'         * hardware2 - Hardware number 2\n'
        f'\n'
        f'Optional arguments:\n'
        f'  -h/--help    Show the help text and exit.\n'
        f'\n'
    )
    sh(f'cd {dir} && {cmd} hardware1')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == 'Hardware: hardware1\n'
    sh(f'cd {dir} && {cmd} hardware2')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == 'Hardware: hardware2\n'


def test_0002(capfd):
    check_0002(capfd, COMMAND)
    check_0002(capfd, CMD)
