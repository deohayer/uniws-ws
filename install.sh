#!/bin/bash

set -e
rm -rf dist
python3 -m build -wn .
pip3 install --no-deps --force-reinstall dist/*
