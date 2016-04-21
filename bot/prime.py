#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
素数とかなにか
"""

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# 素数判定
# http://d.hatena.ne.jp/pashango_p/20090704/1246692091
def is_prime(q):
    q = abs(q)
    if q == 2: return True
    if q < 2 or q & 1 == 0: return False
    return pow(2, q - 1, q) == 1

if __name__ == '__main__':
    ns = [1, 2, 3, 4, 10, 19, 100, 1000, 1001, 1003, 1007, 1009]

    for n in ns:
        p = is_prime(n)
        print("n=", n)
        print("p=", p)
