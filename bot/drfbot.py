#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@DRFbot
Bot本体
"""

from datetime import datetime
import csv
import re
import sys
import os
import random

# Python Twitter Tools
# https://github.com/sixohsix/twitter
from twitter import *

# DRFバッファ手順
import algdrf

# 自作いろいろ
#import prime
import wcadb


# Configurations from 環境変数
CONSUMER_KEY        = os.environ.get("DRFBOT_CONSUMER_KEY")
CONSUMER_SECRET     = os.environ.get("DRFBOT_CONSUMER_SECRET")
ACCESS_TOKEN        = os.environ.get("DRFBOT_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("DRFBOT_ACCESS_TOKEN_SECRET")


# Other Configurations
DRFBOT_SCREEN_NAME = "DRFbot"
ADMIN_SCREEN_NAME  = "kotarotrd"
PATH_TO_DRFBOT = "%s/.." % os.path.abspath(os.path.dirname(__file__))


# For logging
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import datetime
d = datetime.datetime.today()
logfilename = "%s%s%s-%s%s%s" % (d.year, d.month, d.day, d.hour, d.minute, d.second)

logger.addHandler(logging.FileHandler("%s/logs/%s.log" % (PATH_TO_DRFBOT, logfilename), "a+"))
logger.info("DRFbot has just started.")


# トークン分割のパターン
repatter_token  = re.compile(r'[\s,\->　]')
# コーナーの文字列パターン
repatter_corner = re.compile(r'[UFRLBD]{3}')
# エッジの文字列パターン
repatter_edge   = re.compile(r'[UFRLBD]{2}')
# 数字のパターン
#repatter_digits = re.compile(r'[0-9]+')
# タイムっぽい
repatter_time_fast = re.compile(r'[1-2]?[0-9]\.[0-9]+')
repatter_time_mama = re.compile(r'[3-5][0-9]\.[0-9]+')
repatter_time_slow = re.compile(r'[1-9][0-9]*:[0-9]+\.[0-9]+')
repatter_time_zako = re.compile(r'DNF|dnf')

# DRFバッファのコーナー3-cycle手順の辞書
# 辞書はタプルをキーにして手順を文字列として持つ
DRFbuffer = algdrf.get()

# リプライの辞書/リスト
replies = {}
random_replies = []


# トークンへ分割する
# トークンとはスペースとかハイフンとかで区切られたかたまり
def split_into_tokens(text):
    # テキストはHTMLエスケープされてるので
    # "&gt;" --> ">" と "&lt;" --> "<"
    # だけ修正
    text = text.replace("&gt;", ">").replace("&lt;", "<")
    tokens = repatter_token.split(text)
    logger.info("tokens: %s", tokens)
    # @メンション部と空文字は除外する
    trimedtokens = []
    for token in tokens:
        if token != "@DRFbot" and token != "@drfbot" and token != "":
            trimedtokens.append(token)
    logger.info("trimedtokens: %s", trimedtokens)
    return trimedtokens


# トークンを"コーナー"トークンへ分割する
def split_into_corner_tokens(tokens):
    #print("tokens: ", tokens)
    corners = []
    for token in tokens:
        token = token.upper()
        if repatter_corner.match(token):
            corners.append(matched.group())
    logger.info("corners: %s", corners)
    return corners


# トークンを"エッジ"トークンへ分割する
def split_into_edge_tokens(tokens):
    #print("tokens: ", tokens)
    edges = []
    for token in tokens:
        token = token.upper()
        if repatter_edge.match(token):
            edges.append(matched.group())
    logger.info("edges: %s", edges)
    return edges


# コーナー文字の修正 (URF -> UFR 等)
def correctify_corners(tokens):
    corrects = {
        "URF": "UFR", "UFL": "ULF", "ULB": "UBL", "UBR": "URB",
        "FRD": "FDR", "FDL": "FLD", "FLU": "FUL", "FUR": "FRU",
        "LFD": "LDF", "LDB": "LBD", "LBU": "LUB", "LUF": "LFU",
        "BLD": "BDL", "BDR": "BRD", "BRU": "BUR", "BUL": "BLU",
        "RBD": "RDB", "RDF": "RFD", "RFU": "RUF", "RUB": "RBU",
        "DRB": "DBR", "DBL": "DLB", "DLF": "DFL", "DFR": "DRF"
    }

    ret = []
    for token in tokens:
        if token in corrects:
            ret.append(corrects[token])
        else:
            ret.append(token)
    return ret


# DRFバッファのコーナー3-cycle手順検索
def search_drf(tokens):
    length = len(tokens)

    # コーナー文字の修正 (URF -> UFR 等)
    tokens = correctify_corners(tokens)

    # リストの先頭がバッファ対応文字なら削除
    if (0 < length and tokens[0] == "DRF"):
        del tokens[0]
        length = length - 1

    # 形式が間違っている
    if (length < 2):
        return {"cycle": None, "text": ""}

    cycle = "DRF->" + tokens[0] + "->" + tokens[1]
    cyclekey = (tokens[0], tokens[1])
    if cyclekey in DRFbuffer:
        if DRFbuffer[cyclekey][0] == "X":
            return {"cycle": None, "text": cycle + " は3-cycleじゃないよ... ٩(๑`ȏ´๑)۶"}
        else:
            return {"cycle": (tokens[0], tokens[1]), "text": cycle + " は " + DRFbuffer[cyclekey][0] + " (" +  DRFbuffer[cyclekey][1] + ") だよ (๑˃̵ᴗ˂̵)و"}
    else:
        return {"cycle": None, "text": cycle + " はちょっとまだ準備できてないよ... ٩(๑`ȏ´๑)۶"}


# DFバッファのエッジ3-cycle手順検索
def search_df(tokens):
    length = len(tokens)

    # リストの先頭がバッファ対応文字なら削除
    if (0 < length and tokens[0] == "DF"):
        del tokens[0]
        length = length - 1

    # 形式が間違っている
    if (length < 2):
        return {"cycle": None, "text": ""}

    return {"cycle": (tokens[0], tokens[1]), "text": "エッジの3-cycleはちょっとまだ準備できてないよ... ٩(๑`ȏ´๑)۶"}


# リプライテキスト
def get_reply_text(text):
    for k, v in replies.items():
        if k in text:
            return v
    return ""


# ランダムリプライテキスト
def get_random_reply_text():
    return random.choice(random_replies)


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    # オプション
    logger.info("[Info] argvs: %s", argvs)
    logger.info("[Info] argc: %s", argc)
    if (1 < argc) and (argvs[1] == "--test"):
        mode_test = True
    else:
        mode_test = False
    logger.info("[Info] mode_test: %s", mode_test)

    # CSV読み込み (リプライ)
    with open("%s/csv/replies.csv" % PATH_TO_DRFBOT, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            if line[1] == "":
                random_replies.append(line[2])
            else:
                replies[line[1]] = line[2]

    logger.info("random_replies: %s", random_replies)
    logger.info("replies: %s", replies)

    # Twitter OAuth 認証
    auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    # REST
    t = Twitter(auth=auth)

    # 再起動つぶやく
    if not mode_test:
        start_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        status = "起床なう (σω-)。о゜" + start_time + " #DRFbot"
        t.direct_messages.new(user=ADMIN_SCREEN_NAME, text=status)

    # User streams
    twitter_stream = TwitterStream(auth=auth, domain="userstream.twitter.com")
    for msg in twitter_stream.user():
        logger.info("[Info] Timeline updated!")
        logger.info(msg)

        if "user" in msg:
            screen_name = msg["user"]["screen_name"]
            user_name = msg["user"]["name"]

        # @メンション の対応
        is_mention = False
        if ("id" in msg) and ("entities" in msg) and ("user_mentions" in msg["entities"]):
            user_mentions = msg["entities"]["user_mentions"]
            for user_mention in user_mentions:
                if screen_name != DRFBOT_SCREEN_NAME and user_mention["screen_name"] == DRFBOT_SCREEN_NAME:
                    is_mention = True

        if is_mention:
            id = msg["id"]
            logger.info("[Info] Mentioned from @%s (id=%s)", screen_name, str(id))

            # 返信用テキスト/画像
            reply_text = ""
            reply_imgfilename = ""

            # トークンへ分割する
            tokens = split_into_tokens(msg["text"])
            tokens_size = len(tokens)

            # (Pattern 0) 再起動
            if (not mode_test) and (screen_name == ADMIN_SCREEN_NAME) and ("寝ろ" in msg["text"]):
                now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                status = "ｵﾌﾄｩﾝ…ｵﾌﾄｩﾝ…ｵﾌt( ˘ω˘)ｽﾔｧ " + now_time + " #DRFbot"
                try:
                    t.statuses.update(status=status)
                except TwitterError as e:
                    logger.error("[Exception] TwitterError!")
                    logger.error(e)
                except TwitterHTTPError as e:
                    logger.error("[Exception] TwitterHTTPError!")
                    logger.error(e)
                sys.exit(0)

            # CSVパターンマッチング
            reply_text = get_reply_text(msg["text"])

            # 数字ぽいのに反応
            #elif repatter_digits.search(msg["text"]):
            #    d = int(repatter_digits.search(msg["text"]).group(0))
            #    if prime.is_prime(d):
            #        reply_text = screen_name + " " + str(d) + " は素数だよ"
            #    else:
            #        reply_text = screen_name + " " + str(d) + " は素数じゃないよ"

            # タイムぽいのに反応
            if 0 < tokens_size:
                if repatter_time_fast.match(tokens[0]):
                    reply_text = "速いね"
                elif repatter_time_mama.match(tokens[0]):
                    reply_text = "まあまあだね"
                elif repatter_time_slow.match(tokens[0]):
                    reply_text = "遅いよ"
                elif repatter_time_zako.match(tokens[0]):
                    reply_text = "ざこ"

            # (Pattern A) DRFバッファのコーナー3-cycle
            if reply_text == "":
                # コーナートークンへの分割
                corners = split_into_corner_tokens(tokens)
                # DRFバッファのコーナー3-cycle手順検索
                algorithm = search_drf(corners)
                reply_text = algorithm["text"]
                if algorithm["cycle"] is not None:
                    reply_imgfilename = "%s/cubeimages/DRF_%s_%s.png" % (PATH_TO_DRFBOT, algorithm["cycle"][0], algorithm["cycle"][1])
                    logger.info("imgfilename: %s", reply_imgfilename)

            # (Pattern B) DFバッファのエッジ3-cycle
            if reply_text == "":
                # エッジトークンへの分割
                edges = split_into_edge_tokens(tokens)
                # DFバッファのエッジ3-cycle手順検索
                algorithm = search_df(edges)
                reply_text = algorithm["text"]

            # (Pattern C) 世界/日本記録
            if reply_text == "" and 1 < tokens_size:
                reply_text = wcadb.find(tokens[0], tokens[1])

            # 適当にリプライ
            if reply_text == "":
                reply_text = get_random_reply_text()

            # 文字列生成してリプライ
            if reply_text != "" and str(id) != "":
                status = "@" + screen_name + " " + reply_text
                if reply_imgfilename == "":
                    logger.info("[Info] About to reply")
                    params = {"status": status, "in_reply_to_status_id": str(id)}
                else:
                    logger.info("[Info] About to reply *WITH MEDIA*")
                    with open(reply_imgfilename, "rb") as imagefile:
                        params = {"media[]": imagefile.read(), "status": status, "in_reply_to_status_id": str(id)}

                logger.info("status: %s", params["status"])
                logger.info("in_reply_to_status_id: %s", params["in_reply_to_status_id"])

                if not mode_test:
                    try:
                        if "media[]" not in params:
                            t.statuses.update(**params)
                        else:
                            t.statuses.update_with_media(**params)
                    except TwitterError as e:
                        logger.error("[Exception] TwitterError!")
                        logger.error(e)
                    except TwitterHTTPError as e:
                        logger.error("[Exception] TwitterHTTPError!")
                        logger.error(e)
