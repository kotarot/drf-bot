#!/bin/bash -l

cd ${PATH_TO_DRFBOT}

/usr/local/bin/python3 scripts/scramble.py $1

cd -
