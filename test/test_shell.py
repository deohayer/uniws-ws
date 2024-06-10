import pytest
from uniws.shell import sh, ShellResult, ShellError


def check(
    result: 'ShellResult | ShellError',
    capfd: 'object',
    cmd: 'str',
    out: 'str' = '',
    code: 'str' = 0,
    caperr: 'str' = '',
    capout: 'str' = '',
) -> 'None':
    assert result.cmd == cmd
    assert result.out == out
    assert result.code == code
    outerr = capfd.readouterr()
    assert outerr.out == capout
    assert outerr.err == caperr


def test_0000(capfd):
    # Successful execution, implicit capture.
    cmd = 'echo a'
    result = sh(cmd)
    check(result, capfd, cmd, capout='a\n')


def test_0001(capfd):
    # Successful execution, explicit no capture.
    cmd = 'echo a'
    result = sh(cmd, cap=False)
    check(result, capfd, cmd, capout='a\n')


def test_0002(capfd):
    # Successful execution, explicit capture.
    cmd = 'echo a'
    result = sh(cmd, cap=True)
    check(result, capfd, cmd, out='a\n')


def test_0003(capfd):
    # Failed execution, implicit check.
    cmd = 'false'
    with pytest.raises(ShellError) as result:
        sh(cmd)
    check(result.value, capfd, cmd, code=1)


def test_0004(capfd):
    # Failed execution, explicit no check.
    cmd = 'false'
    result = sh(cmd, chk=False)
    check(result, capfd, cmd, code=1)


def test_0005(capfd):
    # Failed execution, explicit check.
    cmd = 'false'
    with pytest.raises(ShellError) as result:
        sh(cmd)
    check(result.value, capfd, cmd, code=1)
