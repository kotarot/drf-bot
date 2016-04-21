#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WCAデータベースに関するなにか
"""

import io
import os
import sys

import pymysql
import pymysql.cursors

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# Configurations from 環境変数
MYSQL_HOST     = os.environ.get("WCADB_MYSQL_HOST")
MYSQL_USERNAME = os.environ.get("WCADB_MYSQL_USERNAME")
MYSQL_PASSWORD = os.environ.get("WCADB_MYSQL_PASSWORD")
MYSQL_DATABASE = os.environ.get("WCADB_MYSQL_DATABASE")


# 競技名
wca_events_alt = {
    # 222
    "222": "222", "2x2x2": "222", "2×2×2": "222",
    "22" : "222", "2x2"  : "222", "2×2"   : "222",
    "2"  : "222",

    # 333
    "333": "333", "3x3x3": "333", "3×3×3": "333",
    "33" : "333", "3x3"  : "333", "3×3"   : "333",
    "3"  : "333", "ルービックキューブ": "333",

    # 444
    "444": "444", "4x4x4": "444", "4×4×4": "444",
    "44" : "444", "4x4"  : "444", "4×4"   : "444",
    "4"  : "444",

    # 555
    "555": "555", "5x5x5": "555", "5×5×5": "555",
    "55" : "555", "5x5"  : "555", "5×5"   : "555",
    "5"  : "555",

    # 666
    "666": "666", "6x6x6": "666", "6×6×6": "666",
    "66" : "666", "6x6"  : "666", "6×6"   : "666",
    "6"  : "666",

    # 777
    "777": "777", "7x7x7": "777", "7×7×7": "777",
    "77" : "777", "7x7"  : "777", "7×7"   : "777",
    "7"  : "777",

    # 333fm
    "333fm": "333fm", "333FM": "333fm",
    "33fm" : "333fm", "33FM" : "333fm",
    "3fm"  : "333fm", "3FM"  : "333fm",
    "fm"   : "333fm", "FM"   : "333fm",
    "333fmc": "333fm", "333FMC": "333fm",
    "33fmc" : "333fm", "33FMC" : "333fm",
    "3fmc"  : "333fm", "3FMC"  : "333fm",
    "fmc"   : "333fm", "FMC"   : "333fm",
    "333最少手数": "333fm", "3x3x3最少手数": "333fm", "3×3×3最少手数": "333fm",
    "33最少手数" : "333fm", "3x3最少手数"  : "333fm", "3×3最少手数"   : "333fm",
    "3最少手数"  : "333fm",
    "最少手数": "333fm", "ルービックキューブ最少手数": "333fm",

    # 333bf
    "333bf": "333bf", "333BF": "333bf",
    "33bf" : "333bf", "33BF" : "333bf",
    "3bf"  : "333bf", "3BF"  : "333bf",
    "bf"   : "333bf", "BF"   : "333bf",
    "333bld": "333bf", "333BLD": "333bf",
    "33bld" : "333bf", "33BLD" : "333bf",
    "3bld"  : "333bf", "3BLD"  : "333bf",
    "bld"   : "333bf", "BLD"   : "333bf",
    "333目隠し": "333bf", "3x3x3目隠し": "333bf", "3×3×3目隠し": "333bf",
    "33目隠し" : "333bf", "3x3目隠し"  : "333bf", "3×3目隠し"   : "333bf",
    "3目隠し"  : "333bf",
    "目隠し": "333bf", "ルービックキューブ目隠し": "333bf",

    # 444bf
    "444bf": "444bf", "444BF": "444bf",
    "44bf" : "444bf", "44BF" : "444bf",
    "4bf"  : "444bf", "4BF"  : "444bf",
    "444bld": "444bf", "444BLD": "444bf",
    "44bld" : "444bf", "44BLD" : "444bf",
    "4bld"  : "444bf", "4BLD"  : "444bf",
    "444目隠し": "444bf", "4x4x4目隠し": "444bf", "4×4×4目隠し": "444bf",
    "44目隠し" : "444bf", "4x4目隠し"  : "444bf", "4×4目隠し"   : "444bf",
    "4目隠し"  : "444bf",

    # 555bf
    "555bf": "555bf", "555BF": "555bf",
    "55bf" : "555bf", "55BF" : "555bf",
    "5bf"  : "555bf", "5BF"  : "555bf",
    "555bld": "555bf", "555BLD": "555bf",
    "55bld" : "555bf", "55BLD" : "555bf",
    "5bld"  : "555bf", "5BLD"  : "555bf",
    "555目隠し": "555bf", "5x5x5目隠し": "555bf", "5×5×5目隠し": "555bf",
    "55目隠し" : "555bf", "5x5目隠し"  : "555bf", "5×5目隠し"   : "555bf",
    "5目隠し"  : "555bf",

    # 333mbf
    "333mbf": "333mbf", "333MBF": "333mbf",
    "33mbf" : "333mbf", "33MBF" : "333mbf",
    "3mbf"  : "333mbf", "3MBF"  : "333mbf",
    "333mbld": "333mbf", "333MBLD": "333mbf",
    "33mbld" : "333mbf", "33MBLD" : "333mbf",
    "3mbld"  : "333mbf", "3MBLD"  : "333mbf",
    "333multi": "333mbf", "333MULTI": "333mbf",
    "33multi" : "333mbf", "33MULTI" : "333mbf",
    "3multi"  : "333mbf", "3MULTI"  : "333mbf",
    "multi"   : "333mbf", "MULTI"   : "333mbf",
    "333複数目隠し": "333mbf", "3x3x3複数目隠し": "333mbf", "3×3×3複数目隠し": "333mbf",
    "33複数目隠し" : "333mbf", "3x3複数目隠し"  : "333mbf", "3×3複数目隠し"   : "333mbf",
    "3複数目隠し"  : "333mbf", "複数目隠し"     : "333mbf",
    "333マルチ目隠し": "333mbf", "3x3x3マルチ目隠し": "333mbf", "3×3×3マルチ目隠し": "333mbf",
    "33マルチ目隠し" : "333mbf", "3x3マルチ目隠し"  : "333mbf", "3×3マルチ目隠し"   : "333mbf",
    "3マルチ目隠し"  : "333mbf", "マルチ目隠し"     : "333mbf",
    "333マルチ": "333mbf", "3x3x3マルチ": "333mbf", "3×3×3マルチ": "333mbf",
    "33マルチ" : "333mbf", "3x3マルチ"  : "333mbf", "3×3マルチ"   : "333mbf",
    "3マルチ"  : "333mbf", "マルチ"     : "333mbf",
    "ルービックキューブ複数目隠し": "333mbf", "ルービックキューブマルチ目隠し": "333mbf", "ルービックキューブマルチ": "333mbf",
}

# 記録種類
wca_records_alt = {
    # NR
    "NR": "nr", "nr": "nr",
    "日本記録": "nr",

    # CR (AsR)
    #"CR": "cr", "cr": "cr",
    #"AsR": "cr", "asr": "cr", "ASR": "cr",
    #"アジア記録": "cr",

    # WR
    "WR": "wr", "wr": "wr",
    "世界記録": "wr"
}


# Returns WCA events (id, name) as a list.
#def wca_events(connection):
#    cursor = connection.cursor()
#    cursor.execute('SELECT id, name FROM Events WHERE rank < 900')
#    events = cursor.fetchall()
#    return [(event[0], event[1]) for event in events]


# 記録変換
def conv(val, event):
    if event == "333fm":
        return str(val)

    elif event == "333mbf":
        valstr = str(val)
        diff = 99 - int(valstr[0:2])
        isec = int(valstr[2:7])
        imin = isec // 60
        isec = isec % 60
        time = "%d:%02d" % (imin, isec)
        missed = int(valstr[7:9])
        solved = diff + missed
        attempted = solved + missed
        return str(solved) + "/" + str(attempted) + " " + time

    else:
        valstr = str(val)
        if len(valstr) < 3:
            return "0." + valstr
        else:
            millisec = valstr[-2:]
            isec = int(valstr[0:-2])
            imin = isec // 60
            isec = isec % 60
            if 0 < imin:
                return "%d:%02d.%s" % (imin, isec, millisec)
            else:
                return "%d.%s" % (isec, millisec)


# 「競技種目」と「記録種類」からデータを返す
def record(event, rtype):
    if rtype == "wr":
        (single, average) = record_wr(event)
        if average != None:
            return "Single: " + conv(single["best"], event) + " by " + single["name"] + " / " +\
                   "Average: " + conv(average["best"], event) + " by " + average["name"]
        else:
            return "Single: " + conv(single["best"], event) + " by " + single["name"]

    #elif rtype == "cr":
    #    return record_cr(event)

    elif rtype == "nr":
        (single, average) = record_nr(event)
        if average != None:
            return "Single: " + conv(single["best"], event) + " by " + single["name"] + " / " +\
                   "Average: " + conv(average["best"], event) + " by " + average["name"]
        else:
            return "Single: " + conv(single["best"], event) + " by " + single["name"]

    else:
        return ""


def record_wr(event):
    connection = pymysql.connect(host=MYSQL_HOST,
                                 user=MYSQL_USERNAME,
                                 passwd=MYSQL_PASSWORD,
                                 db=MYSQL_DATABASE,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        cursor = connection.cursor()
        single = None
        average = None

        sql = """SELECT `eventId`, `best`, `worldRank`, `continentRank`, `countryRank`, `name`, `countryId`
                 FROM `RanksSingle`
                 LEFT OUTER JOIN `Persons`
                 ON `RanksSingle`.`personId`=`Persons`.`id`
                 WHERE `eventId`=%s AND `worldRank`=1"""
        cursor.execute(sql, (event,))
        single = cursor.fetchone()
        print("WR(single): ", single)

        if event != "444bf" and event != "555bf" and event != "333mbf":
            sql = """SELECT `eventId`, `best`, `worldRank`, `continentRank`, `countryRank`, `name`, `countryId`
                     FROM `RanksAverage`
                     LEFT OUTER JOIN `Persons`
                     ON `RanksAverage`.`personId`=`Persons`.`id`
                     WHERE `eventId`=%s AND `worldRank`=1"""
            cursor.execute(sql, (event,))
            average = cursor.fetchone()
            print("WR(average): ", average)

    finally:
        connection.close()
        return (single, average)


def record_nr(event):
    connection = pymysql.connect(host=MYSQL_HOST,
                                 user=MYSQL_USERNAME,
                                 passwd=MYSQL_PASSWORD,
                                 db=MYSQL_DATABASE,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        cursor = connection.cursor()
        single = None
        average = None

        sql = """SELECT `eventId`, `best`, `worldRank`, `continentRank`, `countryRank`, `name`, `countryId`
                 FROM `RanksSingle`
                 LEFT OUTER JOIN `Persons`
                 ON `RanksSingle`.`personId`=`Persons`.`id`
                 WHERE `eventId`=%s AND `countryRank`=1 AND `countryId`='Japan'"""
        cursor.execute(sql, (event,))
        single = cursor.fetchone()
        print("NR(single): ", single)

        if event != "444bf" and event != "555bf" and event != "333mbf":
            sql = """SELECT `eventId`, `best`, `worldRank`, `continentRank`, `countryRank`, `name`, `countryId`
                     FROM `RanksAverage`
                     LEFT OUTER JOIN `Persons`
                     ON `RanksAverage`.`personId`=`Persons`.`id`
                     WHERE `eventId`=%s AND `countryRank`=1 AND `countryId`='Japan'"""
            cursor.execute(sql, (event,))
            average = cursor.fetchone()
            print("NR(average): ", average)

    finally:
        connection.close()
        return (single, average)


# トークンを2つ受け取って「競技種目」と「記録種類」が想定される形式で1つずつ含まれていれば
# その結果を返す
def find(token1, token2):
    if (token1 in wca_events_alt) and (token2 in wca_records_alt):
        return record(wca_events_alt[token1], wca_records_alt[token2])
    elif (token1 in wca_records_alt) and (token2 in wca_events_alt):
        return record(wca_events_alt[token2], wca_records_alt[token1])
    else:
        return ""


if __name__ == '__main__':

    # テスト
    print("--")
    print(find("ルービックキューブ", "世界記録"))
    print("--")
    print(find("333", "WR"))
    print("--")
    print(find("2", "WR"))
    print("--")
    print(find("WR", "4x4"))
    print("--")
    print(find("日本記録", "7×7×7"))
    print("--")
    print(find("目隠し", "世界記録"))
    print("--")
    print(find("複数目隠し", "日本記録"))
    print("--")
    print(find("マルチ", "NR"))
    print("--")
    print(find("ウォッカ", "テキーラ"))
    print("--")
    print(find("日本記録", "ルービックキューブ"))
    print("--")

    #events = wca_events(connection)
    #print(events)
