#!/bin/bash

set -e

if [[ -z "$1" ]]; then
    echo "Version is not provided.";
    exit 1
fi

# Push the tag.
git -C uniws checkout main
git -C uniws pull
git checkout main
git pull
git -C uniws tag $1
git tag $1
git -C uniws push --tags
git push --tags

# Push the wheel.
rm -rf dist
python3 -m build -wn .
twine upload -r pypi dist/*
rm -rf dist
