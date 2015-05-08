#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ローカルのVisualCubeで画像を生成する
"""

import urllib.request


VCUBE_URL = "http://cube.terabo.net/visualcube/visualcube.php"

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

CORNERS = [
    'UFR', 'ULF', 'UBL', 'URB',
    'FDR', 'FLD', 'FUL', 'FRU',
    'LDF', 'LBD', 'LUB', 'LFU',
    'BDL', 'BRD', 'BUR', 'BLU',
    'RDB', 'RFD', 'RUF', 'RBU',
    'DBR', 'DLB', 'DFL', 'DRF'
]


# フェイスレットの色を文字列で返す
def facelet_colors(x, y):
    # フェイスレットのインデックス
    facelet_index = {
        UFR: 8,  ULF: 6,  UBL: 0,  URB: 2,
        FDR: 26, FLD: 24, FUL: 18, FRU: 20,
        LDF: 44, LBD: 42, LUB: 36, LFU: 38,
        BDL: 53, BRD: 51, BUR: 45, BLU: 47,
        RDB: 17, RFD: 15, RUF: 9,  RBU: 11,
        DBR: 35, DLB: 33, DFL: 27, DRF: 29
    }

    # スケルトン (DRFのみ赤)
    skel = "wtwtttwtwwtwtttwtwwtwtttwtwstrtttstsststttstsststttsts"

    # xとyの位置をマゼンタにする
    skel = replace_at_index(skel, facelet_index[x], "m")
    skel = replace_at_index(skel, facelet_index[y], "m")

    return skel


def replace_at_index(string, index, letter):
    return string[:index] + letter + string[index + 1:]


# 「バッファ→x→y」のサイクルの矢印を表す文字列を返す
def arrows_definition(x, y):
    # フェイスレットの位置を表す
    facelet_pos = {
        UFR: "U8", ULF: "U6", UBL: "U0", URB: "U2",
        FDR: "F8", FLD: "F6", FUL: "F0", FRU: "F2",
        LDF: "L8", LBD: "L6", LUB: "L0", LFU: "L2",
        BDL: "B8", BRD: "B6", BUR: "B0", BLU: "B2",
        RDB: "R8", RFD: "R6", RUF: "R0", RBU: "R2",
        DBR: "D8", DLB: "D6", DFL: "D0", DRF: "D2"
    }

    return "D2%s-s6-d,%s%s-s6-d,%sD2-s6-d" % (facelet_pos[x], facelet_pos[x], facelet_pos[y], facelet_pos[y])


# DRFバッファの画像生成
def generate_drfbuffer():
    for x in range(0, 24):
        for y in range(0, 24):
            params = []

            params.append("fmt=png")
            params.append("r=y25x-34")
            params.append("size=480")
            params.append("cc=l")
            params.append("fo=80")
            params.append("co=15")
            params.append("fc=" + facelet_colors(x, y))
            params.append("arw=" + arrows_definition(x, y))

            paramsstr = "&".join(params)
            url = "%s?%s" % (VCUBE_URL, paramsstr)

            print(url)
            res = urllib.request.urlopen(url);
            filename = "DRF_%s_%s.png" % (CORNERS[x], CORNERS[y])
            f = open(filename, "wb")
            f.write(res.read())
            f.close()


if __name__ == '__main__':
    generate_drfbuffer()
