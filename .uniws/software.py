import toml
from uniws import *


def software() -> 'list[Software]':
    return [Workspace()]


DIR_DIST = f'{DIR_TMP}/dist'
DIR_TEST = f'{DIR_BIN}/test'
DIR_OUT = f'{DIR_TMP}/test'
DOCKERS = {
    '3.6': '18.04',
    '3.7': '19.10',
    '3.8': '20.04',
    '3.9': '21.10',
    '3.10': '22.04',
    '3.11': '23.10',
    '3.12': '24.04',
}


class Workspace(Software):
    def __init__(self) -> 'None':
        super().__init__('')
        self.app_download = Fetch()
        self.app_install = Install()
        self.app_test = Test()
        self.app_action = Release()


class Fetch(App):
    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
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
        sh(f'true'
           f' && rm -rf {DIR_TMP}/dist'
           f' && python3 -m build -wn {DIR_TMP}'
           f' && pip3 install --no-deps --force-reinstall {DIR_TMP}/dist/*'
           f';')


class Test(App):
    def __init__(self) -> 'None':
        super().__init__()
        self.arg_versions = Arg(name='VERSIONS',
                                count='*',
                                choices=[x for x in DOCKERS],
                                default=[x for x in DOCKERS])
        self.args.append(self.arg_versions)
        self.arg_filter = Arg(name='PATTERN',
                              sopt='f',
                              lopt='filter',
                              default='test_*.py')
        self.args.append(self.arg_filter)

    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
        sh(f'true'
           f' && rm -rf {DIR_DIST}'
           f' && python3 -m build -wn {DIR_TMP}'
           f' && chmod 644 {DIR_DIST}/*')
        versions: list[str] = args[self.arg_versions]
        filter: str = args[self.arg_filter]
        result = True
        results = {x: True for x in versions}
        for x in versions:
            sep = '-' * 50
            print(sep)
            print(f'Preparing image for {x}.')
            sh(f'true'
               f' && docker build'
               f'      --build-arg VERSION={DOCKERS[x]}'
               f'      --tag uniws:{x}'
               f'      {DIR_TEST} > /dev/null'
               f';')
            out = f'\${{HOME}}/out'
            print(f'Testing {x}.')
            cmd = (f'true'
                   f' && source \${{HOME}}/venv/bin/activate'
                   f' && python3 -m pip install /tmp/uniws/tmp/dist/* > /dev/null'
                   f' && cp -r /tmp/uniws/bin/test \${{HOME}}'
                   f' && mkdir -p {out}'
                   f' && for TEST in \${{HOME}}/test/{filter}; do'
                   f'        [[ ! -f \${{TEST}} ]] && break;'
                   f'        export TEST_NAME=\$(basename \${{TEST}});'
                   f'        export TEST_LOG={out}/\${{TEST_NAME}}.log;'
                   f'        export TEST_TXT={out}/\${{TEST_NAME}}.txt;'
                   f'        python3 -m pytest -vv \${{TEST}} > \${{TEST_LOG}};'
                   f'        if [[ \$? != 0 ]]; then'
                   f'            echo FAIL > \${{TEST_TXT}};'
                   f'            touch {out}/failed;'
                   f'            mv {out}/failed /tmp/uniws/tmp/test/{x}/failed;'
                   f'            chmod 777 /tmp/uniws/tmp/test/{x}/failed;'
                   f'        else'
                   f'            echo PASS > \${{TEST_TXT}};'
                   f'        fi;'
                   f'        printf \'%-43s : %s\\n\' \${{TEST_NAME}} \$(cat \${{TEST_TXT}});'
                   f'        chmod 777 {out}/\${{TEST_NAME}}.*;'
                   f'        mv {out}/\${{TEST_NAME}}.* /tmp/uniws/tmp/test/{x}/;'
                   f'    done'
                   f';')
            sh(f'true'
               f' && rm -rf {DIR_TMP}/test/{x}'
               f' && mkdir -p {DIR_TMP}/test/{x}'
               f' && chmod 777 {DIR_TMP}/test/{x}')
            sh(f'docker run'
               f'    --rm'
               f'    --volume="{DIR_UWS}:/tmp/uniws"'
               f'    --volume="/etc/group:/etc/group:ro"'
               f'    --volume="/etc/passwd:/etc/passwd:ro"'
               f'    --volume="/etc/shadow:/etc/shadow:ro"'
               f'    uniws:{x}'
               f'    /bin/bash -c "{cmd}"'
               f';')
            results[x] = not os.path.exists(f'{DIR_TMP}/test/{x}/failed')
        print(sep)
        for k, v in results.items():
            result = result and v
            print(f'Result {k:36} : {"PASS" if v else "FAIL"}')
        print(f'Result {"":36} : {"PASS" if result else "FAIL"}')


class Release(App):
    def __call__(
        self,
        args: 'dict[Arg]' = None,
        apps: 'list[App]' = None,
    ) -> 'None':
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
