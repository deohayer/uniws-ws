#!/bin/bash

set -e

# Push the tag.
rm -rf release
mkdir -p release
git clone git@github.com:deohayer/uniws.git release/uniws
git -C release/uniws tag $1
git -C release/uniws push --tags
git tag $1
git push --tags

# Push the wheel.
cp pyproject.toml release/pyproject.toml
cd release
python3 -m build -wn .
twine upload -r pypi dist/*
