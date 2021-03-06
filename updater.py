#!/usr/bin/env python3

import downloader as downloadLib
import csv
import utils
import os
import sys
import logging

LOG_LEVEL = logging.DEBUG


class Updater:
    """Download csv file with Excel format with pattern:
    <base_file_name>;<server_file_name>;<MD5Checksum>\\n
    Compare files for update (bad MD5 or missing and return it the list.
    Update files which user want to update.
    """


    def __init__(self):
        self._server_csv_path = ""
        self._local_folder_path = ""
        self._parsed_csv_file = {}
        self._update_files = []
        self._missing_files = []
        self._identical_files = []

        logging.basicConfig(stream=sys.stderr, level=LOG_LEVEL)


    def _clear_lists(self):
        self._parsed_csv_file = {}
        self._update_files = []
        self._missing_files = []
        self._identical_files = []


    def set_paths(self, _server_csv_path, _local_folder_path):
        """Set path to server CSV file and local MC folder
        """
        self._server_csv_path = _server_csv_path
        self._local_folder_path = _local_folder_path


    def resolve_files(self):
        """Download and parse server CSV file and compute MD5Checksums for local file
        If everything is allright return True, otherwise return False
        """
        self._clear_lists()

        if self._server_csv_path == "":
            return False

        downloader = downloadLib.Downloader()

        filename = downloader.download_file(self._server_csv_path, silent=True)

        try:
            fileList = os.listdir(self._local_folder_path)
        except FileNotFoundError:
            return False

        print(fileList)

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                print(row)
                net_file_base_name = row[0]
                self._parsed_csv_file[net_file_base_name] = row
                foundFile = False

                for lFile in fileList:
                    if lFile.startswith(net_file_base_name):
                        foundFile = True
                        md5 = utils.md5sum(self._local_folder_path + lFile)

                        if md5 == row[2]:
                            self._identical_files.append(net_file_base_name)
                        else:
                            self._update_files.append(net_file_base_name)

                if not foundFile:
                    self._missing_files.append(net_file_base_name)

        logging.debug('Updater: files are resolved')
        logging.debug('UpdateFiles: ' + ','.join(self._update_files))
        logging.debug('MissingFiles: ' + ','.join(self._missing_files))
        logging.debug('IdenticalFiles: ' + ','.join(self._identical_files))

        return True


    def update_files(self, files_list):
        """Update files in the list in local folder.
        Old files will be deleted!!!
        """
        try:
            localFiles = os.listdir(self._local_folder_path)
        except FileNotFoundError:
            return 0

        counter = 0

        downloader = downloadLib.Downloader()

        for f in localFiles:
            for updateF in files_list:
                if f.startswith(updateF):
                    print('files found')
                    tempfile = downloader.download_file(self._parsed_csv_file[updateF][1])
                    counter += 1
                    os.remove(self._local_folder_path + f)
                    os.move(tempfile, self._local_folder_path + f)

        return counter


    def get_update_list(self):
        return self._update_files


    def get_missing_list(self):
        return self._missing_files


    def get__identical_files(self):
        return self._identical_files


