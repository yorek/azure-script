#!/bin/sh

rm -rf dist
rm -rf build

python setup.py sdist bdist_wheel

rm -rf build
