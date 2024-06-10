from uniws.shell import sh


def test_0000(capfd):
    # Availability.
    sh('uniws -h')
    out, err = capfd.readouterr()
    assert err == ''
    assert out == \
        (''
         'uniws {...}\n'
         '\n'
         'Uniform workspace CLI.\n'
         '\n'
         'Commands:\n'
         '  setup    Manage app. Add shortcuts and completion.\n'
         '  reset    Manage app. Remove shortcuts and revert changes.\n'
         '  init     Initialize a new workspace.\n'
         '  sw       Work with the software.\n'
         '  hw       Work with the hardware.\n'
         '\n'
         'Optional arguments:\n'
         '  -h/--help    Show the help text and exit.\n'
         '\n'
         '')
