from .helpers import *

COMMAND = 'uniws hw connect'
CMD = 'hwc'
HELP = 'Manage the connection to hardware.'


def check_0000(capfd, cmd):
    # Outside.
    check_setup()
    sh(f'{cmd} -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        f'{COMMAND} [STATE]\n'
        f'\n'
        f'{HELP}\n'
        f'\n'
        f'Positional arguments:\n'
        f'  [STATE]    The state to set.\n'
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
        f'{COMMAND} [STATE]\n'
        f'\n'
        f'{HELP}\n'
        f'\n'
        f'Positional arguments:\n'
        f'  [STATE]    The state to set.\n'
        f'             Default: switch\n'
        f'             Allowed values:\n'
        f'              * switch - Change the connection state.\n'
        f'              * attach - Connect to the hardware.\n'
        f'              * detach - Disconnect from the hardware.\n'
        f'\n'
        f'Optional arguments:\n'
        f'  -h/--help    Show the help text and exit.\n'
        f'\n'
    )
    sh(f'cd {dir} && {cmd}')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        'Hardware: \n'
        'Switch\n'
    )
    sh(f'cd {dir} && {cmd} attach')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        'Hardware: \n'
        'Attach\n'
    )
    sh(f'cd {dir} && {cmd} detach')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        'Hardware: \n'
        'Detach\n'
    )


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
        f'{COMMAND} HW [STATE]\n'
        f'\n'
        f'{HELP}\n'
        f'\n'
        f'Positional arguments:\n'
        f'  HW         A hardware to use.\n'
        f'             Allowed values:\n'
        f'              * hardware1\n'
        f'              * hardware2 - Hardware number 2\n'
        f'  [STATE]    The state to set.\n'
        f'             Default: switch\n'
        f'             Allowed values:\n'
        f'              * switch - Change the connection state.\n'
        f'              * attach - Connect to the hardware.\n'
        f'              * detach - Disconnect from the hardware.\n'
        f'\n'
        f'Optional arguments:\n'
        f'  -h/--help    Show the help text and exit.\n'
        f'\n'
    )
    sh(f'cd {dir} && {cmd} hardware1')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        'Hardware: hardware1\n'
        'Switch\n'
    )
    sh(f'cd {dir} && {cmd} hardware1 attach')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        'Hardware: hardware1\n'
        'Attach\n'
    )
    sh(f'cd {dir} && {cmd} hardware2 detach')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == (
        'Hardware: hardware2\n'
        'Detach\n'
    )


def test_0002(capfd):
    check_0002(capfd, COMMAND)
    check_0002(capfd, CMD)
