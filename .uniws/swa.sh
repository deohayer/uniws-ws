#!/bin/bash

# $1 - a request: '?' - list components, '!' - execute the command.
# $@ - a list of components. If empty, the entire workspace is assumed.

set -e
ROOT="$(realpath $(dirname "${BASH_SOURCE[0]}")/..)"

if [[ $1 == '?' ]]; then
    # TODO: Populate the components, if any.
    LIST=()
    for ITEM in "${LIST[@]}"; do
        echo ${ITEM}
    done
fi

if [[ $1 == '!' ]]; then
    VERSION=( $(grep "version" "${ROOT}/code/pyproject.toml") )
    VERSION=${VERSION[2]//\"}
    RELEASE_ROOT="${ROOT}/out/uniws-ws"
    RELEASE_REPO="${RELEASE_ROOT}/code/uniws"
    rm -rf "${RELEASE_ROOT}"
    git clone \
        --recurse-submodules \
        --branch main \
        "git@github.com:deohayer/uniws-ws.git" \
        "${RELEASE_ROOT}"
    git -C "${RELEASE_ROOT}" tag "${VERSION}"
    git -C "${RELEASE_ROOT}" push --tags
    git -C "${RELEASE_REPO}" tag "${VERSION}"
    git -C "${RELEASE_REPO}" push --tags
    rm -rf "${RELEASE_ROOT}/code/dist"
    python3 -m build -wn "${RELEASE_ROOT}/code"
    twine upload -r pypi "${RELEASE_ROOT}/code/dist/"*
fi
