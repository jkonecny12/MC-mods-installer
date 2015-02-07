#!/usr/bin/env python3

import os
import csv
import re
import utils

COMPUTE_FOLDER = './mods_folder/'
CSV_NAME = 'mods.csv'

DEFAULT_SERVER = 'http://packetseekers.dvratil.cz/MC-files/'

def create_csv_file(data):
    """Create an csv file from files in data array
    """
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
            filesHash.append((result.group(1), DEFAULT_SERVER + f, fHash))

    create_csv_file(filesHash)

