#!/bin/bash -l

cd ${PATH_TO_DRFBOT}

/usr/local/bin/python3 bot/scramble.py $1

cd -
