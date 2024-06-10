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
    git -C ${ROOT} checkout develop
    git -C ${ROOT} submodule update --init
    git -C ${ROOT}/code/uniws checkout develop
fi
