#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys


def print_files():
    if len(sys.argv) <= 1:
        print('Usage:', sys.argv[0], '<dir path>')
        return

    dir_ = sys.argv[1]
    dict_ = {}

    for f in os.listdir(dir_):
        if os.path.isfile(os.path.join(dir_, f)):
            dict_[f] = (os.stat(os.path.join(dir_, f))).st_size
    dict_ = sorted(dict_.items(), key=lambda x: (x[1], x[0]), reverse=True)
    for key, value in dict_:
        print(key, '\t', str(value))


if __name__ == "__main__":
    print_files()
