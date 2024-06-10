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
    # Build the wheel.
    rm -rf "${ROOT}/code/dist"
    python3 -m build -wn "${ROOT}/code"
    chmod 644 "${ROOT}/code/dist/"*
    # Dokcer-Ubuntu versions. Associative array does not preserve order.
    VERSIONS=(
        "3.6 18.04"
        "3.7 19.10"
        "3.8 20.04"
        "3.9 21.10"
        "3.10 22.04"
        "3.11 23.10"
        "3.12 24.04"
    )
    RESULTS=()
    for i in "${!VERSIONS[@]}"; do
        # Split Python and Ubuntu versions.
        VERPAIR=(${VERSIONS[$i]})
        PYTHON="${VERPAIR[0]}"
        DOCKER="${VERPAIR[1]}"
        # Define directories for local, mount, and docker.
        ROOT_MOUNT="/tmp/uniws"
        OUT_LOCAL="${ROOT}/out/test/${PYTHON}"
        OUT_MOUNT="${ROOT_MOUNT}/out/test/${PYTHON}"
        OUT_HOME="\${HOME}/out"
        TEST_MOUNT="${ROOT_MOUNT}/test"
        TEST_HOME="\${HOME}/test"
        # Re-create local output directory specific to version
        rm -rf "${OUT_LOCAL}"
        mkdir -p "${OUT_LOCAL}"
        chmod 777 "${OUT_LOCAL}"
        # Print banner.
        echo "--------------------------------------------------"
        echo "Python ${PYTHON} (Ubuntu ${DOCKER})"
        # Prepare Docker image.
        echo "Prepare image."
        docker build \
            --build-arg VERSION=${DOCKER} \
            --tag uniws:${PYTHON} \
            "${ROOT}/test" > /dev/null
        # Execute tests in Docker.
        echo "Execute tests."
        docker run \
            --rm \
            --volume="${ROOT}:${ROOT_MOUNT}" \
            uniws:${PYTHON} \
            /bin/bash -c "true \
                &&  source \${HOME}/venv/bin/activate \
                &&  python3 -m pip install ${ROOT_MOUNT}/code/dist/* > /dev/null \
                &&  mkdir -p ${TEST_HOME} \
                &&  cp -RaT ${TEST_MOUNT} ${TEST_HOME} \
                &&  mkdir -p ${OUT_HOME} \
                &&  for TEST in \${HOME}/test/test_*.py; do \
                        export TEST_NAME=\$(basename \${TEST}); \
                        export TEST_LOG=${OUT_HOME}/\${TEST_NAME}.log; \
                        export TEST_TXT=${OUT_HOME}/\${TEST_NAME}.txt; \
                        python3 -m pytest -vv \${TEST} > \${TEST_LOG}; \
                        if [[ \$? != 0 ]]; then \
                            echo "FAIL" > \${TEST_TXT}; \
                            touch ${OUT_HOME}/failed; \
                            mv ${OUT_HOME}/failed ${OUT_MOUNT}/failed; \
                            chmod 777 ${OUT_MOUNT}/failed; \
                        else \
                            echo PASS > \${TEST_TXT}; \
                        fi; \
                        printf '%-43s : %s\\n' \${TEST_NAME} \$(cat \${TEST_TXT}); \
                        chmod 777 ${OUT_HOME}/\${TEST_NAME}.*; \
                        mv ${OUT_HOME}/\${TEST_NAME}.* ${OUT_MOUNT}/; \
                    done \
                "
        set +e
        [[ -f "${OUT_LOCAL}/failed" ]]
        RESULTS[$i]=$?
        set -e
    done
    echo "--------------------------------------------------"
    # Print global results.
    GLOBAL=PASS
    for i in "${!VERSIONS[@]}"; do
        VERPAIR=(${VERSIONS[$i]})
        PYTHON="${VERPAIR[0]}"
        DOCKER="${VERPAIR[1]}"
        if [[ ${RESULTS[$i]} == 1 ]]; then
            RESULT=PASS
        else
            RESULT=FAIL
            GLOBAL=FAIL
        fi
        printf 'Result %-36s : %s\n' ${PYTHON} ${RESULT}
    done
    printf 'Result %-36s : %s\n' "" ${GLOBAL}
fi
