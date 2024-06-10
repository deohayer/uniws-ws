from .helpers import *


def test_0000(capfd):
    # Availability.
    sh('uniws hw -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == \
        (''
         'uniws hw {...}\n'
         '\n'
         'Work with the hardware.\n'
         '\n'
         'Commands:\n'
         '  connect     Manage the connection to hardware.\n'
         '  power       Manage the power state of hardware.\n'
         '  shell       Execute a command or start a session.\n'
         '  download    Download from the hardware.\n'
         '  upload      Upload to the hardware.\n'
         '  action      Perform a workspace-specific action.\n'
         '\n'
         'Optional arguments:\n'
         '  -h/--help    Show the help text and exit.\n'
         '\n'
         '')
