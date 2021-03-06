#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DRFバッファのコーナー3-cycle手順
"""

import argparse
import codecs
import csv
from jinja2 import Environment, FileSystemLoader
import os
import random

# Python Twitter Tools
# https://github.com/sixohsix/twitter
from twitter import *


# Configurations from 環境変数
CONSUMER_KEY        = os.environ.get("DRFBOT_CONSUMER_KEY")
CONSUMER_SECRET     = os.environ.get("DRFBOT_CONSUMER_SECRET")
ACCESS_TOKEN        = os.environ.get("DRFBOT_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("DRFBOT_ACCESS_TOKEN_SECRET")


# Other Configurations
PATH_TO_DRFBOT = "%s/.." % os.path.abspath(os.path.dirname(__file__))
mode_test = False


################################
#### CONSTANTS #################
################################
UFR = 0
ULF = 1
UBL = 2
URB = 3
FDR = 4
FLD = 5
FUL = 6
FRU = 7
LDF = 8
LBD = 9
LUB = 10
LFU = 11
BDL = 12
BRD = 13
BUR = 14
BLU = 15
RDB = 16
RFD = 17
RUF = 18
RBU = 19
DBR = 20
DLB = 21
DFL = 22
DRF = 23

cornersl = ['あ', 'い',  'う', 'か',
            'き', 'く', 'こ', 'し',
            'す', 'た', 'つ', 'て',
            'と', 'な', 'に', 'の',
            'は', 'も', 'ら', 'り',
            'る', 'れ', 'ん', '-']
cornerss = ['UFR', 'ULF', 'UBL', 'URB',
            'FDR', 'FLD', 'FUL', 'FRU',
            'LDF', 'LBD', 'LUB', 'LFU',
            'BDL', 'BRD', 'BUR', 'BLU',
            'RDB', 'RFD', 'RUF', 'RBU',
            'DBR', 'DLB', 'DFL', 'DRF']
cornersidx = {'UFR':  0, 'ULF':  1, 'UBL':  2, 'URB':  3,
              'FDR':  4, 'FLD':  5, 'FUL':  6, 'FRU':  7,
              'LDF':  8, 'LBD':  9, 'LUB': 10, 'LFU': 11,
              'BDL': 12, 'BRD': 13, 'BUR': 14, 'BLU': 15,
              'RDB': 16, 'RFD': 17, 'RUF': 18, 'RBU': 19,
              'DBR': 20, 'DLB': 21, 'DFL': 22, 'DRF': 23}

# セットアップ用プレムーブ (バッファが動くものは除外)
premoves = ["U", "U2", "U'",
            "L", "L2", "L'",
            "B", "B2", "B'"]
################################


# 3-cycleの(バッファ以外の)位置とMoveを受け取って
# Moveの実行後に位置がどこに移動するか返す
def movepos(cx, cy, move):
    return (moveposone(cx, move), moveposone(cy, move))

def moveposone(pos, move):
    rot = {
        "U": 1, "U2": 2, "U'": 3,
        "F": 1, "F2": 2, "F'": 3,
        "L": 1, "L2": 2, "L'": 3,
        "B": 1, "B2": 2, "B'": 3,
        "R": 1, "R2": 2, "R'": 3,
        "D": 1, "D2": 2, "D'": 3,
    }

    u_face = [UFR, ULF, UBL, URB]
    u_rowc = [FRU, LFU, BLU, RBU]
    u_row  = [RUF, FUL, LUB, BUR]
    f_face = [FDR, FLD, FUL, FRU]
    f_rowc = [DRF, LDF, ULF, RUF]
    f_row  = [RFD, DFL, LFU, UFR]
    l_face = [LDF, LBD, LUB, LFU]
    l_rowc = [DFL, BDL, UBL, FUL]
    l_row  = [FLD, DLB, BLU, ULF]
    b_face = [BDL, BRD, BUR, BLU]
    b_rowc = [DLB, RDB, URB, LUB]
    b_row  = [LBD, DBR, RBU, UBL]
    r_face = [RDB, RFD, RUF, RBU]
    r_rowc = [DBR, FDR, UFR, BUR]
    r_row  = [BRD, DRF, FRU, URB]
    d_face = [DBR, DLB, DFL, DRF]
    d_rowc = [BRD, LBD, FLD, RFD]
    d_row  = [RDB, BDL, LDF, FDR]

    if move == "U" or move == "U2" or move == "U'":
        if pos in u_face:
            return u_face[(u_face.index(pos) + rot[move]) % 4]
        elif pos in u_rowc:
            return u_rowc[(u_rowc.index(pos) + rot[move]) % 4]
        elif pos in u_row:
            return u_row[(u_row.index(pos) + rot[move]) % 4]
    if move == "F" or move == "F2" or move == "F'":
        if pos in f_face:
            return f_face[(f_face.index(pos) + rot[move]) % 4]
        elif pos in f_rowc:
            return f_rowc[(f_rowc.index(pos) + rot[move]) % 4]
        elif pos in f_row:
            return u_row[(f_row.index(pos) + rot[move]) % 4]
    if move == "L" or move == "L2" or move == "L'":
        if pos in l_face:
            return l_face[(l_face.index(pos) + rot[move]) % 4]
        elif pos in l_rowc:
            return l_rowc[(l_rowc.index(pos) + rot[move]) % 4]
        elif pos in l_row:
            return l_row[(l_row.index(pos) + rot[move]) % 4]
    if move == "B" or move == "B2" or move == "B'":
        if pos in b_face:
            return b_face[(b_face.index(pos) + rot[move]) % 4]
        elif pos in b_rowc:
            return b_rowc[(b_rowc.index(pos) + rot[move]) % 4]
        elif pos in b_row:
            return b_row[(b_row.index(pos) + rot[move]) % 4]
    if move == "R" or move == "R2" or move == "R'":
        if pos in r_face:
            return r_face[(r_face.index(pos) + rot[move]) % 4]
        elif pos in r_rowc:
            return r_rowc[(r_rowc.index(pos) + rot[move]) % 4]
        elif pos in r_row:
            return r_row[(r_row.index(pos) + rot[move]) % 4]
    if move == "D" or move == "D2" or move == "D'":
        if pos in d_face:
            return d_face[(d_face.index(pos) + rot[move]) % 4]
        elif pos in d_rowc:
            return d_rowc[(d_rowc.index(pos) + rot[move]) % 4]
        elif pos in d_row:
            return d_row[(d_row.index(pos) + rot[move]) % 4]

    return pos


# 3-cycleチェック
def check_cycle(cx, cy):
    # 同じ文字
    if cx == cy:
        return ("X", "<same>")
    # バッファ絡み
    elif cx == FDR or cx == RFD or cx == DRF or cy == FDR or cy == RFD or cy == DRF:
        return ("X", "<buffer>")
    # UFR/FRU/RUF
    elif (cx == UFR and (cy == FRU or cy == RUF)) or (cx == FRU and (cy == UFR or cy == RUF)) or (cx == RUF and (cy == UFR or cy == FRU)):
        return ("X", "<UFR>")
    # ULF/LFU/FUL
    elif (cx == ULF and (cy == FUL or cy == LFU)) or (cx == FUL and (cy == ULF or cy == LFU)) or (cx == LFU and (cy == ULF or cy == FUL)):
        return ("X", "<ULF>")
    # UBL/BLU/LUB
    elif (cx == UBL and (cy == LUB or cy == BLU)) or (cx == LUB and (cy == UBL or cy == BLU)) or (cx == BLU and (cy == UBL or cy == LUB)):
        return ("X", "<UBL>")
    # URB/RBU/BUR
    elif (cx == URB and (cy == BUR or cy == RBU)) or (cx == BUR and (cy == URB or cy == RBU)) or (cx == RBU and (cy == URB or cy == BUR)):
        return ("X", "<URB>")
    # DFL/FLD/LDF
    elif (cx == DFL and (cy == FLD or cy == LDF)) or (cx == FLD and (cy == DFL or cy == LDF)) or (cx == LDF and (cy == DFL or cy == FLD)):
        return ("X", "<DFL>")
    # DLB/LBD/BDL
    elif (cx == DLB and (cy == LBD or cy == BDL)) or (cx == LBD and (cy == DLB or cy == BDL)) or (cx == BDL and (cy == DLB or cy == LBD)):
        return ("X", "<DLB>")
    # DBR/BRD/RDB
    elif (cx == DBR and (cy == BRD or cy == RDB)) or (cx == BRD and (cy == DBR or cy == RDB)) or (cx == RDB and (cy == DBR or cy == BRD)):
        return ("X", "<DBR>")

    return ("", "")


# D面インターチェンジパターン
def pattern_interchange_d(cx, cy, premove):
    interchange = {
        DBR: "D'",
        DLB: "D2",
        DFL: "D"
    }
    insert = {
        RUF: "R U R'",
        LFU: "R U' R'",
        BLU: "R U2 R'",
        FRU: "F' U' F", # "y L' U' L y'",
        BUR: "F' U F", # "y L' U L y'",
        LUB: "F' U2 F", # "y L' U2 L y'",
        UFR: "R2 U R2 U' R2"
    }
    # インサート手順の手数 (持ち替え含む)
    insert_cost = {
        RUF: 3,
        LFU: 3,
        BLU: 3,
        FRU: 5,
        BUR: 5,
        LUB: 5,
        UFR: 5
    }

    # D面インターチェンジ (1)
    if (cx == DBR or cx == DLB or cx == DFL) and (cy == RUF or cy == LFU or cy == BLU or cy == FRU or cy == BUR or cy == LUB or cy == UFR):
        if premove == "":
            return ("[" + insert[cy] + ", " + interchange[cx] + "]", "D面インターチェンジ", insert_cost[cy])
        else:
            return ("[" + premove + ": " + insert[cy] + ", " + interchange[cx] + "]", "1手セットアップ＋D面インターチェンジ", insert_cost[cy])

    # D面インターチェンジ (2)
    elif (cy == DBR or cy == DLB or cy == DFL) and (cx == RUF or cx == LFU or cx == BLU or cx == FRU or cx == BUR or cx == LUB or cx == UFR):
        if premove == "":
            return ("[" + interchange[cy] + ", " + insert[cx] + "]", "D面インターチェンジ", insert_cost[cx])
        else:
            return ("[" + premove + ": " + interchange[cy] + ", " + insert[cx] + "]", "1手セットアップ＋D面インターチェンジ", insert_cost[cx])

    return ("", "", -1)


# U面インターチェンジパターン
def pattern_interchange_u(cx, cy, premove):
    pos_on_u = {
        UFR: 0, FRU: 0, RUF: 0,
        ULF: 1, LFU: 1, FUL: 1,
        UBL: 2, BLU: 2, LUB: 2,
        URB: 3, RBU: 3, BUR: 3
    }

    # U面インターチェンジ (1)
    if (cx == UFR or cx == ULF or cx == UBL or cx == URB) and (cy == UFR or cy == ULF or cy == UBL or cy == URB):
        if cx == UFR: setup = ""
        elif cx == ULF: setup = "U'"
        elif cx == UBL: setup = "U2"
        elif cx == URB: setup = "U"
        insert = "R2 D' R2 D R2" #insert = "R' F' R2 F R"
        d = pos_on_u[cy] - pos_on_u[cx]
        if d == 1 or d == -3: interchange = "U'"
        elif d == 2 or d == -2: interchange = "U2"
        elif d == 3 or d == -1: interchange = "U"
        if premove == "":
            if setup == "":
                return ("[" + insert + ", " + interchange + "]", "U面インターチェンジ", 5)
            elif cy == UFR:
                return ("[" + setup + ", " + insert + "]", "U面インターチェンジ", 5)
            else:
                return ("[" + setup + ": " + insert + ', ' + interchange + "]", "U面インターチェンジ", 7)
        else:
            if setup == "":
                return ("[" + premove + ": " + insert + ", " + interchange + "]", "1手セットアップ＋U面インターチェンジ", 5)
            elif cy == UFR:
                return ("[" + premove + ": " + setup + ", " + insert + "]", "1手セットアップ＋U面インターチェンジ", 5)
            else:
                return ("[" + premove + " " + setup + ": " + insert + ', ' + interchange + "]", "1手セットアップ＋U面インターチェンジ", 7)

    # U面インターチェンジ (2)
    elif (cx == FRU or cx == LFU or cx == BLU or cx == RBU) and (cy == FRU or cy == LFU or cy == BLU or cy == RBU):
        if cx == FRU: setup = "U2"
        elif cx == LFU: setup = "U"
        elif cx == BLU: setup = ""
        elif cx == RBU: setup = "U'"
        insert = "L' D2 L"
        d = pos_on_u[cy] - pos_on_u[cx]
        if d == 1 or d == -3: interchange = "U'"
        elif d == 2 or d == -2: interchange = "U2"
        elif d == 3 or d == -1: interchange = "U"
        if premove == "":
            if setup == "":
                return ("[" + insert + ", " + interchange + "]", "U列インターチェンジ", 3)
            elif (cy == BLU):
                return ("[" + setup + ", " + insert + "]", "U列インターチェンジ", 3)
            else:
                return ("[" + setup + ": " + insert + ', ' + interchange + "]", "U列インターチェンジ", 5)
        else:
            if setup == "":
                return ("[" + premove + ": " + insert + ", " + interchange + "]", "1手セットアップ＋U列インターチェンジ", 3)
            elif (cy == BLU):
                return ("[" + premove + ": " + setup + ", " + insert + "]", "1手セットアップ＋U列インターチェンジ", 3)
            else:
                return ("[" + premove + " " + setup + ": " + insert + ', ' + interchange + "]", "1手セットアップ＋U列インターチェンジ", 5)

    # U面インターチェンジ (3)
    elif (cx == RUF or cx == FUL or cx == LUB or cx == BUR) and (cy == RUF or cy == FUL or cy == LUB or cy == BUR):
        if cx == RUF: setup = ""
        elif cx == FUL: setup = "U'"
        elif cx == LUB: setup = "U2"
        elif cx == BUR: setup = "U"
        insert = "R' D' R"
        d = pos_on_u[cy] - pos_on_u[cx]
        if d == 1 or d == -3: interchange = "U'"
        elif d == 2 or d == -2: interchange = "U2"
        elif d == 3 or d == -1: interchange = "U"
        if premove == "":
            if setup == "":
                return ("[" + insert + ", " + interchange + "]", "U列インターチェンジ", 3)
            elif cy == RUF:
                return ("[" + setup + ", " + insert + "]", "U列インターチェンジ", 3)
            else:
                return ("[" + setup + ": " + insert + ', ' + interchange + "]", "U列インターチェンジ", 5)
        else:
            if setup == "":
                return ("[" + premove + ": " + insert + ", " + interchange + "]", "1手セットアップ＋U列インターチェンジ", 3)
            elif cy == RUF:
                return ("[" + premove + ": " + setup + ", " + insert + "]", "1手セットアップ＋U列インターチェンジ", 3)
            else:
                return ("[" + premove + " " + setup + ": " + insert + ', ' + interchange + "]", "1手セットアップ＋U列インターチェンジ", 5)

    return ("", "", -1)


# L面インターチェンジパターン
def pattern_interchange_l(cx, cy, premove):
    pos_on_l = {
        ULF: 0, LFU: 0, FUL: 0,
        UBL: 1, BLU: 1, LUB: 1,
        DLB: 2, LBD: 2, BDL: 2,
        DFL: 3, FLD: 3, LDF: 3
    }

    # L面インターチェンジ (1)
    if (cx == LFU or cx == LUB or cx == LBD or cx == LDF) and (cy == LFU or cy == LUB or cy == LBD or cy == LDF):
        if cx == LFU: setup = ""
        elif cx == LUB: setup = "L"
        elif cx == LBD: setup = "L2"
        elif cx == LDF: setup = "L'"
        insert = "U' R U"
        d = pos_on_l[cy] - pos_on_l[cx]
        if d == 1 or d == -3: interchange = "L"
        elif d == 2 or d == -2: interchange = "L2"
        elif d == 3 or d == -1: interchange = "L'"
        if premove == "":
            if setup == "":
                return ("[" + insert + ", " + interchange + "]", "L面インターチェンジ", 3)
            elif cy == LFU:
                return ("[" + setup + ", " + insert + "]", "L面インターチェンジ", 3)
            else:
                return ("[" + setup + ": " + insert + ", " + interchange + "]", "L面インターチェンジ", 5)
        else:
            if setup == "":
                return ("[" + premove + ": " + insert + ", " + interchange + "]", "1手セットアップ＋L面インターチェンジ", 3)
            elif cy == LFU:
                return ("[" + premove + ": " + setup + ", " + insert + "]", "1手セットアップ＋L面インターチェンジ", 3)
            else:
                return ("[" + premove + " " + setup + ": " + insert + ", " + interchange + "]", "1手セットアップ＋L面インターチェンジ", 5)

    # L面インターチェンジ (2)
    elif (cx == ULF or cx == BLU or cx == DLB or cx == FLD) and (cy == ULF or cy == BLU or cy == DLB or cy == FLD):
        if cx == ULF: setup = "D"
        elif cx == BLU: setup = "D2"
        elif cx == DLB: setup = "D'"
        elif cx == FLD: setup = ""
        insert = "R2 U R2 U' R2"
        d = pos_on_l[cy] - pos_on_l[cx]
        if d == 1 or d == -3: interchange = "D"
        elif d == 2 or d == -2: interchange = "D2"
        elif d == 3 or d == -1: interchange = "D'"
        if premove == "":
            if setup == "":
                return ("[z': " + insert + ", " + interchange + "]", "L列インターチェンジ", 5)
            elif cy == ULF:
                return ("[z': " + setup + ", " + insert + "]", "L列インターチェンジ", 5)
            else:
                return ("[z' " + setup + ": " + insert + ", " + interchange + "]", "L列インターチェンジ", 7)
        else:
            if setup == "":
                return ("[" + premove + " z: " + insert + ", " + interchange + "]", "1手セットアップ＋L列インターチェンジ", 5)
            elif cy == ULF:
                return ("[" + premove + " z: " + setup + ", " + insert + "]", "1手セットアップ＋L列インターチェンジ", 5)
            else:
                return ("[" + premove + " z " + setup + ": " + insert + ", " + interchange + "]", "1手セットアップ＋L列インターチェンジ", 7)

    # L面インターチェンジ (3)
    elif (cx == FUL or cx == UBL or cx == BDL or cx == DFL) and (cy == FUL or cy == UBL or cy == BDL or cy == DFL):
        if cx == FUL: setup = "L'"
        elif cx == UBL: setup = ""
        elif cx == BDL: setup = "L"
        elif cx == DFL: setup = "L2'"
        insert = "U R2 U'"
        d = pos_on_l[cy] - pos_on_l[cx]
        if d == 1 or d == -3: interchange = "L"
        elif d == 2 or d == -2: interchange = "L2"
        elif d == 3 or d == -1: interchange = "L'"
        if premove == "":
            if setup == "":
                return ("[" + insert + ", " + interchange + "]", "L列インターチェンジ", 3)
            elif cy == UBL:
                return ("[" + setup + ", " + insert + "]", "L列インターチェンジ", 3)
            else:
                return ("[" + setup + ": " + insert + ", " + interchange + "]", "L列インターチェンジ", 5)
        else:
            if setup == "":
                return ("[" + premove + ": " + insert + ", " + interchange + "]", "1手セットアップ＋L列インターチェンジ", 3)
            elif cy == UBL:
                return ("[" + premove + ": " + setup + ", " + insert + "]", "1手セットアップ＋L列インターチェンジ", 3)
            else:
                return ("[" + premove + " " + setup + ": " + insert + ", " + interchange + "]", "1手セットアップ＋L列インターチェンジ", 5)

    return ("", "", -1)


# B面インターチェンジパターン
def pattern_interchange_b(cx, cy, premove):
    pos_on_b = {
        UBL: 0, BLU: 0, LUB: 0,
        URB: 1, RBU: 1, BUR: 1,
        DBR: 2, BRD: 2, RDB: 2,
        DLB: 3, LBD: 3, BDL: 3
    }

    # B面インターチェンジ (1)
    if (cx == BLU or cx == BUR or cx == BRD or cx == BDL) and (cy == BLU or cy == BUR or cy == BRD or cy == BDL):
        if cx == BLU: setup = "R'"
        elif cx == BUR: setup = ""
        elif cx == BRD: setup = "R"
        elif cx == BDL: setup = "R2'"
        insert = "U L' U'"
        d = pos_on_b[cy] - pos_on_b[cx]
        if d == 1 or d == -3: interchange = "R"
        elif d == 2 or d == -2: interchange = "R2"
        elif d == 3 or d == -1: interchange = "R'"
        if premove == "":
            if setup == "":
                return ("[y: " + insert + ", " + interchange + "]", "B面インターチェンジ", 3)
            elif cy == BUR:
                return ("[y: " + setup + ", " + insert + "]", "B面インターチェンジ", 3)
            else:
                return ("[y " + setup + ": " + insert + ", " + interchange + "]", "B面インターチェンジ", 5)
        else:
            if setup == "":
                return ("[" + premove + " y: " + insert + ", " + interchange + "]", "1手セットアップ＋B面インターチェンジ", 3)
            elif cy == BUR:
                return ("[" + premove + " y: " + setup + ", " + insert + "]", "1手セットアップ＋B面インターチェンジ", 3)
            else:
                return ("[" + premove + " y " + setup + ": " + insert + ", " + interchange + "]", "1手セットアップ＋B面インターチェンジ", 5)

    # B面インターチェンジ (2)
    elif (cx == LUB or cx == URB or cx == RDB or cx == DLB) and (cy == LUB or cy == URB or cy == RDB or cy == DLB):
        if cx == LUB: setup = "D2"
        elif cx == URB: setup = "D'"
        elif cx == RDB: setup = ""
        elif cx == DLB: setup = "D"
        insert = "R2 U R2 U' R2"
        d = pos_on_b[cy] - pos_on_b[cx]
        if d == 1 or d == -3: interchange = "D"
        elif d == 2 or d == -2: interchange = "D2"
        elif d == 3 or d == -1: interchange = "D'"
        if premove == "":
            if setup == "":
                return ("[x: " + insert + ", " + interchange + "]", "B列インターチェンジ", 5)
            elif cy == RDB:
                return ("[x: " + setup + ", " + insert + "]", "B列インターチェンジ", 5)
            else:
                return ("[x " + setup + ": " + insert + ", " + interchange + "]", "B列インターチェンジ", 7)
        else:
            if setup == "":
                return ("[" + premove + " x: " + insert + ", " + interchange + "]", "1手セットアップ＋B列インターチェンジ", 5)
            elif cy == RDB:
                return ("[" + premove + " x: " + setup + ", " + insert + "]", "1手セットアップ＋B列インターチェンジ", 5)
            else:
                return ("[" + premove + " x " + setup + ": " + insert + ", " + interchange + "]", "1手セットアップ＋B列インターチェンジ", 7)

    # B面インターチェンジ (3)
    elif (cx == UBL or cx == RBU or cx == DBR or cx == LBD) and (cy == UBL or cy == RBU or cy == DBR or cy == LBD):
        if cx == UBL: setup = ""
        elif cx == RBU: setup = "R"
        elif cx == DBR: setup = "R2"
        elif cx == LBD: setup = "R"
        insert = "U' L2 U"
        d = pos_on_b[cy] - pos_on_b[cx]
        if d == 1 or d == -3: interchange = "R"
        elif d == 2 or d == -2: interchange = "R2"
        elif d == 3 or d == -1: interchange = "R'"
        if premove == "":
            if setup == "":
                return ("[y: " + insert + ", " + interchange + "]", "B列インターチェンジ", 3)
            elif cy == RDB:
                return ("[y: " + setup + ", " + insert + "]", "B列インターチェンジ", 3)
            else:
                return ("[y " + setup + ": " + insert + ", " + interchange + "]", "B列インターチェンジ", 5)
        else:
            if setup == "":
                return ("[" + premove + " y: " + insert + ", " + interchange + "]", "1手セットアップ＋B列インターチェンジ", 3)
            elif cy == RDB:
                return ("[" + premove + " y: " + setup + ", " + insert + "]", "1手セットアップ＋B列インターチェンジ", 3)
            else:
                return ("[" + premove + " y " + setup + ": " + insert + ", " + interchange + "]", "1手セットアップ＋B列インターチェンジ", 5)

    return ("", "", -1)


# A-permパターン
def pattern_aperm(cx, cy, premove):
    setup = ""
    algorithm = ""

    # A-permのパターン (F面)
    if cx == RUF and cy == ULF:
        algorithm = "R2 U2 R D R' U2 R D' R"
        comment = "F面A-perm"
    elif cx == ULF and cy == RUF:
        algorithm = "R' D R' U2 R D' R' U2 R2"
        comment = "F面A-perm"
    elif cx == RUF and cy == LDF:
        algorithm = "R U' R D2 R' U R D2 R2"
        comment = "F面A-perm"
    elif cx == LDF and cy == RUF:
        algorithm = "R2 D2 R' U' R D2 R' U R'"
        comment = "F面A-perm"
    elif cx == ULF and cy == LDF:
        algorithm = "L2 D2 L U L' D2 L U' L"
        comment = "F面A-perm"
    elif cx == LDF and cy == ULF:
        algorithm = "L' U L' D2 L U' L' D2 L2"
        comment = "F面A-perm"

    # A-permのパターン (R面)
    elif cx == FRU and cy == URB:
        setup = "y"
        algorithm = "U' R U' L2 U R' U' L2 U2"
        comment = "R面A-perm"
    elif cx == URB and cy == FRU:
        setup = "y"
        algorithm = "U2 L2 U R U' L2 U R' U"
        comment = "R面A-perm"
    elif cx == FRU and cy == BRD:
        setup = "y"
        algorithm = "L' U L' D2 L U' L' D2 L2"
        comment = "R面A-perm"
    elif cx == BRD and cy == FRU:
        setup = "y"
        algorithm = "L2 D2 L U L' D2 L U' L"
        comment = "R面A-perm"
    elif cx == URB and cy == BRD:
        setup = "y"
        algorithm = "R2 D2 R' U' R D2 R' U R'"
        comment = "R面A-perm"
    elif cx == BRD and cy == URB:
        setup = "y"
        algorithm = "R U' R D2 R' U R D2 R2"
        comment = "R面A-perm"

    # A-permのパターン (D面)
    elif cx == DBR and cy == DLB:
        setup = "x"
        algorithm = "R2 D2 R' U' R D2 R' U R'"
        comment = "D面A-perm"
    elif cx == DLB and cy == DBR:
        setup = "x"
        algorithm = "R U' R D2 R' U R D2 R2"
        comment = "D面A-perm"
    elif cx == DBR and cy == DFL:
        setup = "x"
        algorithm = "R' D R' U2 R D' R' U2 R2"
        comment = "D面A-perm"
    elif cx == DFL and cy == DBR:
        setup = "x"
        algorithm = "R2 U2 R D R' U2 R D' R"
        comment = "D面A-perm"
    elif cx == DLB and cy == DFL:
        setup = "x"
        algorithm = "U' R U' L2 U R' U' L2 U2"
        comment = "D面A-perm"
    elif cx == DFL and cy == DLB:
        setup = "x"
        algorithm = "U2 L2 U R U' L2 U R' U"
        comment = "D面A-perm"

    if algorithm != "":
        if premove == "":
            if setup == "":
                return ("[" + algorithm + "]", comment)
            else:
                return ("[" + setup + ": " + algorithm + "]", comment)
        else:
            if setup == "":
                return ("[" + premove + ": " + algorithm + "]", "1手セットアップ＋" + comment)
            else:
                return ("[" + premove + " " + setup + ": " + algorithm + "]", "1手セットアップ＋" + comment)
    else:
        return ("", "")


################################
# 手順生成
alg = {}
for cx in range(0, 24):
    for cy in range(0, 24):
        alg[(cx, cy)] = []

        # 3-cycleチェック
        res = check_cycle(cx, cy)
        if res[0] != "":
            alg[(cx, cy)].append(res)
            continue

        ################################
        #### インターチェンジパターン
        without_setups_high = []
        without_setups_low = []
        with_setups_high = []
        with_setups_low = []

        # B面インターチェンジ
        res_b = pattern_interchange_b(cx, cy, "")
        if res_b[0] != "":
            without_setups_high.append(res_b)

        # 1手セットアップ＋B面インターチェンジ
        else:
            for premove in premoves:
                (ncx, ncy) = movepos(cx, cy, premove)
                res = pattern_interchange_b(ncx, ncy, premove)
                if res[0] != "":
                    if res[2] <= 3:
                        with_setups_high.insert(0, (res[0], res[1], 2 + res[2]))
                    else:
                        with_setups_low.insert(0, (res[0], res[1], 2 + res[2]))

        # L面インターチェンジ
        res_l = pattern_interchange_l(cx, cy, "")
        if res_l[0] != "":
            without_setups_high.append(res_l)

        # 1手セットアップ＋L面インターチェンジ
        else:
            for premove in premoves:
                (ncx, ncy) = movepos(cx, cy, premove)
                res = pattern_interchange_l(ncx, ncy, premove)
                if res[0] != "":
                    if res[2] <= 3:
                        with_setups_high.insert(0, (res[0], res[1], 2 + res[2]))
                    else:
                        with_setups_low.insert(0, (res[0], res[1], 2 + res[2]))

        # U面インターチェンジ
        res_u = pattern_interchange_u(cx, cy, "")
        if res_u[0] != "":
            without_setups_high.append(res_u)

        # 1手セットアップ＋U面インターチェンジ
        else:
            for premove in premoves:
                (ncx, ncy) = movepos(cx, cy, premove)
                res = pattern_interchange_u(ncx, ncy, premove)
                if res[0] != "":
                    if res[2] <= 3:
                        with_setups_high.insert(0, (res[0], res[1], 2 + res[2]))
                    else:
                        with_setups_low.insert(0, (res[0], res[1], 2 + res[2]))

        # D面インターチェンジ
        res_d = pattern_interchange_d(cx, cy, "")
        if res_d[0] != "":
            without_setups_high.append(res_d)

        # 1手セットアップ＋D面インターチェンジ
        else:
            for premove in premoves:
                (ncx, ncy) = movepos(cx, cy, premove)
                res = pattern_interchange_d(ncx, ncy, premove)
                if res[0] != "":
                    if res[2] <= 3:
                        with_setups_high.insert(0, (res[0], res[1], 2 + res[2]))
                    else:
                        with_setups_low.insert(0, (res[0], res[1], 2 + res[2]))

        alg[(cx, cy)] = without_setups_high + without_setups_low + with_setups_high + with_setups_low


        # A-permのパターン
        res_a = pattern_aperm(cx, cy, "")
        if res_a[0] != "":
            alg[(cx, cy)].insert(0, res_a)

        # 1手セットアップ＋A-permのパターン
        else:
            for premove in premoves:
                (ncx, ncy) = movepos(cx, cy, premove)
                res = pattern_aperm(ncx, ncy, premove)
                if res[0] != "":
                    # A-permの優先度をちょっと下げる
                    if len(alg[(cx, cy)]) == 0 or 5 < alg[(cx, cy)][0][2]:
                        alg[(cx, cy)].insert(0, res)
                    else:
                        alg[(cx, cy)].append(res)

# カスタム手順を CSV から読み込む
alg_custom = {}
with codecs.open('%s/csv/customs.csv' % PATH_TO_DRFBOT, 'r', 'utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for line in reader:
        if line[0] == '1':
            k = (cornersidx[line[1]], cornersidx[line[2]]) # key: (cx, cy)
            v = (line[3], line[4]) # value: (algorithm, description)
            if k not in alg_custom:
                alg_custom[k] = [v]
            else:
                alg_custom[k].insert(0, v)
# 個別対応 カスタム手順はCSVから結合
for k, v in alg_custom.items():
    if k not in alg:
        alg[k] = v
    else:
        alg[k] = v + alg[k]

for cx in range(0, 24):
    for cy in range(0, 24):
        if len(alg[(cx, cy)]) == 0:
            alg[(cx, cy)].append(("T", "<TODO>"))


# 検索用に文字列をキーにした辞書で返す
def get():
    buffer = {}
    for cx in range(0, 24):
        for cy in range(0, 24):
            buffer[(cornerss[cx], cornerss[cy])] = alg[(cx, cy)][0]
    return buffer


def show_all():
    num_todo = 0

    for cx in range(0, 24):
        print("    # " + cornerss[cx] + " : " + cornersl[cx])
        for cy in range(0, 24):
            algs = []
            for a in alg[(cx, cy)]:
                algs.append('("' + a[0] + '", "' + a[1] + '")')
            print('    ("' + cornerss[cx] + '", "' + cornerss[cy] + '"): [' + ", ".join(algs) + '],')

            if len(alg[(cx, cy)]) == 1 and alg[(cx, cy)][0][0] == "T":
                num_todo = num_todo + 1

        print("");

    print("Number of TODO: ", num_todo)
    print("")


# 手順をランダム選択
def select_random_alg():
    while True:
        x, y = random.randint(0, 23), random.randint(0, 23)
        a = alg[(x, y)][0]
        if a[0][0] != "X":
            cycle = (cornerss[x], cornerss[y])
            return (cycle, a[0], a[1])


def random_post():
    ra = select_random_alg()
    status = "DRF->%s->%s:\n%s (%s)\n\n(´-`).｡oO( もっといい手順あれば教えて!! ) #今日のDRFbuffer" % (ra[0][0], ra[0][1], ra[1], ra[2])
    imgfilename = "%s/cubeimages/DRF_%s_%s.png" % (PATH_TO_DRFBOT, ra[0][0], ra[0][1])
    print("[Info] status: ", status)
    print("[Info] imgfilename: ", imgfilename)

    with open(imgfilename, "rb") as imagefile:
        params = {"media[]": imagefile.read(), "status": status}

    # Twitter OAuth 認証 + REST
    if not mode_test:
        auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
        t = Twitter(auth=auth)
        try:
            t.statuses.update_with_media(**params)
        except TwitterError as e:
            print("[Exception] TwitterError!")
            print(e)
        except TwitterHTTPError as e:
            print("[Exception] TwitterHTTPError!")
            print(e)


# 手順一覧のHTMLを生成する
def gen_html(filename):
    rows = []
    for x in range(0, 24):
        first = True
        for y in range(0, 24):
            a = alg[(x, y)][0]
            if a[0][0] != "X":
                if first:
                    first = False
                    rows.append("<tr class=\"first\"><td>(DRF %s %s)</td><td>%s</td><td>%s</td></tr>" % (cornerss[x], cornerss[y], a[0], a[1]))
                else:
                    rows.append("<tr><td>(DRF %s %s)</td><td>%s</td><td>%s</td></tr>" % (cornerss[x], cornerss[y], a[0], a[1]))

    env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
    tpl = env.get_template('index.tpl')
    html = tpl.render({'rows': rows})
    with codecs.open(filename, 'w', 'utf-8') as f:
        f.write(html)


# 単体実行では標準出力に表示
# "--random-post" オプションでランダム投稿
if __name__ == '__main__':
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(description='DRF bot: algorithm script')
    parser.add_argument('--test', '-t', default=False, action='store_true',
                        help='set up with test mode (default: False)')
    parser.add_argument('--random-post', '-r', default=False, action='store_true',
                        help='post a ramdom algorithm (default: False)')
    parser.add_argument('--gen-html', '-g', default=None, type=str,
                        help='generate list of algorithms in html to the given path to file (default: None)')
    args = parser.parse_args()

    mode_test = args.test
    print("[Info] mode_test:", mode_test)

    if args.random_post:
        random_post()
    elif args.gen_html:
        gen_html(args.gen_html)
    else:
        show_all()
