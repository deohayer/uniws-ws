import toml
from uniws import *


def software() -> 'list[Software]':
    return [Workspace()]


class Workspace(Software):
    def __init__(self) -> 'None':
        super().__init__(name='uniws',
                         help='Work with uniws.')
        self.fetch = Fetch()
        self.install = Install()
        self.release = Release()


class Fetch(App):
    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        super().__call__(args, apps)
        sh(f'true'
           f' && git -C {DIR_UWS} checkout develop'
           f' && git -C {DIR_UWS} submodule update --init'
           f' && git -C {DIR_TMP}/uniws checkout develop'
           f';')


class Install(App):
    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        super().__call__(args, apps)
        sh(f'true'
           f' && rm -rf {DIR_TMP}/dist'
           f' && python3 -m build -wn {DIR_TMP}'
           f' && pip3 install --no-deps --force-reinstall {DIR_TMP}/dist/*'
           f';')


class Release(App):
    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        super().__call__(args, apps)
        config = toml.load(f'{DIR_TMP}/pyproject.toml')
        version = config['project']['version']
        root = f'{DIR_TMP}/uniws-ws'
        tmp = f'{root}/tmp'
        repo = f'{tmp}/uniws'
        sh(f'true'
           f' && rm -rf {root}'
           f' && git clone'
           f'      --recurse-submodules'
           f'      --branch main'
           f'      git@github.com:deohayer/uniws-ws.git'
           f'      {root}'
           f' && git -C {root} tag {version}'
           f' && git -C {root} push --tags'
           f' && git -C {repo} tag {version}'
           f' && git -C {repo} push --tags'
           f' && rm -rf {tmp}/dist'
           f' && python3 -m build -wn {tmp}'
           f' && twine upload -r pypi {tmp}/dist/*'
           f';')
