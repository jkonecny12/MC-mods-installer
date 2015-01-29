#!/usr/bin/env python3

import os
import csv
import re
import utils

COMPUTE_FOLDER = './test_files/'
CSV_NAME = 'mods.csv'

def createCSVfile(data):
    with open(CSV_NAME, 'w', newline='') as csvfile:
        writter = csv.writer(csvfile, delimiter=';')

        for row in data:
            writter.writerow(row)

if __name__ == "__main__":

    pattern = re.compile(r'(.*?).\d*[.]', flags=re.I)

    files = os.listdir(COMPUTE_FOLDER)
    filesHash = []


    for f in files:
        if f.startswith('\.'):
            print(f + ' skipped')
            continue

        print('Creating csv file for file: ' +  f)

        result = pattern.match(f)

        if result:
            fHash = utils.md5sum(COMPUTE_FOLDER + f)
            filesHash.append((result.group(1), f, fHash))

    createCSVfile(filesHash)
