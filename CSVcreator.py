#!/usr/bin/env python3

import os
import csv
import re
import utils

if __name__ == "__main__":

    pattern = re.compile(r'(.*?).\d', flags=re.I)

    files = os.listdir('.')
    filesHash = {}

    print(files)

    for f in files:
        if f.startswith('\.'):
            print(f + ' skipped')
            continue

        result = pattern.match(f)

        if result:
            fHash = utils.md5sum(f)
            print(result.groups())
            filesHash[result.group()] = (result.group(), f, fHash)

    print(filesHash)
