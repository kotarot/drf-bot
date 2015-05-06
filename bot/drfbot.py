#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@DRFbot
Bot本体
"""

from datetime import datetime
import re
import sys
import os

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

# トークンへ分割する
# トークンとはスペースとかハイフンとかで区切られたかたまり
def split_into_tokens(text):
    # テキストはHTMLエスケープされてるので
    # "&gt;" --> ">" と "&lt;" --> "<"
    # だけ修正
    text = text.replace("&gt;", ">").replace("&lt;", "<")
    tokens = repatter_token.split(text)
    print("tokens: ", tokens)
    # @メンション部と空文字は除外する
    trimedtokens = []
    for token in tokens:
        if token != "@DRFbot" and token != "@drfbot" and token != "":
            trimedtokens.append(token)
    print("trimedtokens: ", trimedtokens)
    return trimedtokens


# トークンを"コーナー"トークンへ分割する
def split_into_corner_tokens(tokens):
    #print("tokens: ", tokens)
    corners = []
    for token in tokens:
        token = token.upper()
        matched = repatter_corner.match(token)
        if matched:
            corners.append(matched.group())
    print("corners: ", corners)
    return corners


# トークンを"エッジ"トークンへ分割する
def split_into_edge_tokens(tokens):
    #print("tokens: ", tokens)
    edges = []
    for token in tokens:
        token = token.upper()
        matched = repatter_edge.match(token)
        if matched:
            edges.append(matched.group())
    print("edges: ", edges)
    return edges


# コーナー文字の修正 (URF -> UFR 等)
def correctify_corners(tokens):
    corrects = {
        "URF": "UFR", "UFL": "ULF", "ULB": "UBL", "UBR": "UBR",
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
        return ""

    cycle = "DRF->" + tokens[0] + "->" + tokens[1]
    cyclekey = (tokens[0], tokens[1])
    if cyclekey in DRFbuffer:
        if DRFbuffer[cyclekey][0] == "X":
            return cycle + " は3-cycleじゃないよ... ٩(๑`ȏ´๑)۶"
        else:
            return cycle + " は " + DRFbuffer[cyclekey][0] + " (" +  DRFbuffer[cyclekey][1] + ") だよ (๑˃̵ᴗ˂̵)و"
    else:
        return cycle + " はちょっとまだ準備できてないよ... ٩(๑`ȏ´๑)۶"


# DFバッファのエッジ3-cycle手順検索
def search_df(tokens):
    length = len(tokens)

    # リストの先頭がバッファ対応文字なら削除
    if (0 < length and tokens[0] == "DF"):
        del tokens[0]
        length = length - 1

    # 形式が間違っている
    if (length < 2):
        return ""

    return "エッジの3-cycleはちょっとまだ準備できてないよ... ٩(๑`ȏ´๑)۶"


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    # オプション
    print("[Info] argvs: ", argvs)
    print("[Info] argc: ", argc)
    if (1 < argc) and (argvs[1] == "--test"):
        mode_test = True
    else:
        mode_test = False
    print("[Info] mode_test: ", mode_test)

    # Twitter OAuth 認証
    auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    # REST
    t = Twitter(auth=auth)

    # 再起動つぶやく
    if not mode_test:
        start_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        status = "起床なう (σω-)。о゜" + start_time + " #DRFbot"
        t.direct_messages.new(user="kotarotrd", text=status)
    #    try:
    #        t.statuses.update(status=status)
    #    except TwitterError as e:
    #        print("[Exception] TwitterError!")
    #        print(e)
    #    except TwitterHTTPError as e:
    #        print("[Exception] TwitterHTTPError!")
    #        print(e)

    # User streams
    twitter_stream = TwitterStream(auth=auth, domain="userstream.twitter.com")
    for msg in twitter_stream.user():
        print("[Info] Timeline updated!")
        print(msg)

        # @メンション の対応
        is_mention = False
        if ("id" in msg) and ("entities" in msg) and ("user_mentions" in msg["entities"]):
            user_mentions = msg["entities"]["user_mentions"]
            for user_mention in user_mentions:
                if user_mention["screen_name"] == "DRFbot":
                    is_mention = True

        if is_mention:
            id = msg["id"]
            screen_name = msg["user"]["screen_name"]
            user_name = msg["user"]["name"]
            print("[Info] Mentioned from @" + screen_name + " (id=" + str(id)+ ")")

            # 返信用テキスト
            reply_text = ""

            # トークンへ分割する
            tokens = split_into_tokens(msg["text"])
            tokens_size = len(tokens)

            # (Pattern 0) 再起動
            if (not mode_test) and (screen_name == "kotarotrd") and ("寝ろ" in msg["text"]):
                now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                status = "ｵﾌﾄｩﾝ…ｵﾌﾄｩﾝ…ｵﾌt( ˘ω˘)ｽﾔｧ " + now_time + " #DRFbot"
                try:
                    t.statuses.update(status=status)
                except TwitterError as e:
                    print("[Exception] TwitterError!")
                    print(e)
                except TwitterHTTPError as e:
                    print("[Exception] TwitterHTTPError!")
                    print(e)
                sys.exit(0)

            # (Pattern 1) スペシャルケース 1 いろいろ
            elif ("有能" in msg["text"]):
                reply_text = "えへへ (ﾉ≧ڡ≦)"
            elif ("賢い" in msg["text"] or "かしこい" in msg["text"]):
                reply_text = "まあね ˉ̞̭ ( ›◡ु‹ ) ˄̻ ̊"
            elif ("すごい" in msg["text"]):
                reply_text = "知ってた"
            elif ("おい" in msg["text"] or "ねえ" in msg["text"] or "あのさ" in msg["text"]):
                reply_text = "はいっ w|;ﾟﾛﾟ|w ...何でしょうか？"

            # (Pattern 2) スペシャルケース 2 : HuaLong
            elif ("HuaLong" in msg["text"] or "hualong" in msg["text"]):
                reply_text = "HuaLongは神"

            # (Pattern 4) スペシャルケース 4 : 世界大会
            elif ("世界大会" in msg["text"]):
                reply_text = user_name + "はルービックキューブ世界大会に行きまぁす"

            # (Pattern 5) スペシャルケース 5 : 数字
            #elif repatter_digits.search(msg["text"]):
            #    d = int(repatter_digits.search(msg["text"]).group(0))
            #    if prime.is_prime(d):
            #        reply_text = screen_name + " " + str(d) + " は素数だよ"
            #    else:
            #        reply_text = screen_name + " " + str(d) + " は素数じゃないよ"

            # (Pattern 6) スペシャルケース 6 : 思います
            elif ("思います" in msg["text"] or "思う" in msg["text"] or "思いました" in msg["text"] or "思った" in msg["text"] or
                  "では？" in msg["text"] or "どう？" in msg["text"] or "どうですか" in msg["text"] or "どうでしょう" in msg["text"]):
                reply_text = "なるほど～♬"

            # (Pattern 7) スペシャルケース 7 : せやな
            elif ("せやな" in msg["text"] or "せやね" in msg["text"]):
                reply_text = "せやろか？"

            # タイムぽいのに反応
            if 0 < tokens_size:
                if repatter_time_fast.match(tokens[0]):
                    reply_text = "早いね"
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
                reply_text = search_drf(corners)

            # (Pattern B) DFバッファのエッジ3-cycle
            if reply_text == "":
                # エッジトークンへの分割
                edges = split_into_edge_tokens(tokens)
                # DFバッファのエッジ3-cycle手順検索
                reply_text = search_df(edges)

            # (Pattern C) 世界/日本記録
            if reply_text == "" and 1 < tokens_size:
                reply_text = wcadb.find(tokens[0], tokens[1])

            # 適当にリプライ
            if reply_text == "":
                reply_text = "( ᵅั ᴈ ᵅั;)～♬"

            # 文字列生成してリプライ
            if reply_text != "" and str(id) != "":
                status = "@" + screen_name + " " + reply_text
                print("status: ", status)
                print("in_reply_to_status_id: ", str(id))
                if not mode_test:
                    try:
                        t.statuses.update(status=status, in_reply_to_status_id=id)
                    except TwitterError as e:
                        print("[Exception] TwitterError!")
                        print(e)
                    except TwitterHTTPError as e:
                        print("[Exception] TwitterHTTPError!")
                        print(e)
