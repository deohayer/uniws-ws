from .helpers import *


def test_0000(capfd):
    # Availability.
    sh('uniws sw -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == \
        (''
         'uniws sw {...}\n'
         '\n'
         'Work with the software.\n'
         '\n'
         'Commands:\n'
         '  fetch      Fetch the software.\n'
         '  build      Build the software.\n'
         '  install    Install the software.\n'
         '  test       Test the software.\n'
         '  clean      Clean the software.\n'
         '  action     Perform a workspace-specific action.\n'
         '\n'
         'Optional arguments:\n'
         '  -h/--help    Show the help text and exit.\n'
         '\n'
         '')
