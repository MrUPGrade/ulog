#!/bin/bash

set -e

PYTHONDONTWRITEBYTECODE="True"
export PYTHONDONTWRITEBYTECODE


if [ ! -z $1 ]
then

    find . -iname *.pyc -delete
    rm -Rf .cache

    if [ ! -z $PIP_PROXY ]
    then
        pip install -q --trusted-host $PIP_PROXY -i http://$PIP_PROXY:3141/root/pypi/+simple/ .[test]
    else
        pip install -q .[test]
    fi

    if [ "$1" = "unittest" ]
    then
        sudo -u executor py.test --junitxml=/src/test_${PY_VER}_output.xml ./tests/unittests/
    elif [ "$1" = "cov" ]
    then
        sudo -u executor coverage run -m py.test ./tests/unittests/
        sudo -u executor coverage html
    fi
else
    exec "$@"
fi

