#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@DRFbot
スクランブルを投稿する
"""


import subprocess
import sys
import os

# Python Twitter Tools
# https://github.com/sixohsix/twitter
from twitter import *


# Configurations from 環境変数
CONSUMER_KEY        = os.environ.get("DRFBOT_CONSUMER_KEY")
CONSUMER_SECRET     = os.environ.get("DRFBOT_CONSUMER_SECRET")
ACCESS_TOKEN        = os.environ.get("DRFBOT_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("DRFBOT_ACCESS_TOKEN_SECRET")


# スクランブル生成
def gen_scramble(type_scramble):
    cmd = "%s/chample -n 1 -t %s -ns" % (os.environ.get("PATH_TO_CHAMPLE"), type_scramble)
    return subprocess.check_output(cmd.split(" ")).decode("utf-8").rstrip()


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    # オプション
    print("[Info] argvs: ", argvs)
    print("[Info] argc: ", argc)
    type_scramble = 0
    if 1 < argc:
        if argvs[1] == "corner":
            type_scramble = 1
        elif argvs[1] == "edge":
            type_scramble = 2
    print("[Info] type_scramble: ", type_scramble)

    # スクランブル生成
    scramble = gen_scramble(type_scramble)
    print("[Info] scramble: ", scramble)

    # Twitter OAuth 認証 + REST
    auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    t = Twitter(auth=auth)
    status = "今日のスクランブルだけどやってみれば？\n" + scramble
    try:
        t.statuses.update(status=status)
    except TwitterError as e:
        print("[Exception] TwitterError!")
        print(e)
    except TwitterHTTPError as e:
        print("[Exception] TwitterHTTPError!")
        print(e)
