#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
天気関係
"""

import codecs
from datetime import datetime
import urllib.request


# 単体実行で天気のAPIを叩いてJSONをローカルに保存
# 基本的には1日1回実行する
if __name__ == '__main__':
    res = urllib.request.urlopen("http://api.openweathermap.org/data/2.5/forecast/daily?q=Tokyo,jp&units=metric")
    f = codecs.open("weather-forecast.json", "w", "utf-8")
    f.write(res.read().decode("utf-8"))
    f.close()
