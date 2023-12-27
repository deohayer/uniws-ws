#!/bin/bash

set -e
python3 -m build -wn .
pip3 install --no-deps --force-reinstall dist/*
