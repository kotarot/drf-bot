#!/bin/bash -l

cd ${PATH_TO_DRFBOT}

BOTPROC=`ps aux | grep drfbot | grep python | grep -v grep | awk '{ print $2; }'`

if [ ! ${BOTPROC} ]
then
    nohup ./start.sh > /dev/null 2>&1 < /dev/null &
fi

cd -
