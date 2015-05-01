#!/bin/bash

PIDS=(`ps aux | grep drfbot | grep python | grep -v grep | awk '{ print $2; }'`)
echo ${PIDS}
