#!/usr/bin/env python3

import downloader as downloadLib
import csv
import hashlib
import os
import sys
import logging

LOG_LEVEL = logging.DEBUG


class Updater:
    "Download csv file with Excel format with pattern:"
    "<base_file_name>;<server_file_name>;<MD5Checksum>\\n"
    "Compare files for update (bad MD5 or missing and return it the list."
    "Update files which user want to update."

    def __init__(self):
        self.serverCSVPath = ""
        self.localFolderPath = ""
        self.parsedCSVFile = {}
        self.updateFiles = []
        self.missingFiles = []
        self.identicalFiles = []

        logging.basicConfig(stream=sys.stderr, level=LOG_LEVEL)

    def _clearLists(self):
        self.parsedCSVFile = {}
        self.updateFiles = []
        self.missingFiles = []
        self.identicalFiles = []

    def _computeMD5(self, filename):
        "Compute MD5 hash from given file"
        with open(filename, mode='r') as hashfile:
            md5 = hashlib.md5()
            for buf in hashfile.read(128):
                md5.update(buf.encode())

        return md5.hexdigest()

    def setPaths(self, serverCSVPath, localFolderPath):
        "Set path to server CSV file and local MC folder"
        self.serverCSVPath = serverCSVPath
        self.localFolderPath = localFolderPath

    def resolveFiles(self):
        "Download and parse server CSV file and compute MD5Checksums for local file"
        "If everything is allright return True, otherwise return False"

        self._clearLists()

        if self.serverCSVPath == "":
            return False

        downloader = downloadLib.Downloader()

        filename = downloader.downloadFile(self.serverCSVPath, silent=True)

        try:
            fileList = os.listdir(self.localFolderPath)
        except FileNotFoundError:
            return False

        print(fileList)

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                print(row)
                netFileBaseName = row[0]
                self.parsedCSVFile[netFileBaseName] = row

                for lFile in fileList:
                    if lFile.startswith(netFileBaseName):
# Need to add MD5 checksum control to append file to right list
                        self.updateFiles.append(netFileBaseName)
                    else:
                        self.missingFiles.append(netFileBaseName)

        logging.debug('Updater: files are resolved')
        logging.debug('UpdateFiles: ' + self.updateFiles)
        logging.debug('MissingFiles: ' + self.missingFiles)
        logging.debug('IdenticalFiles: ' + self.identicalFiles)

        return True


    def getUpdateList(self):
        return self.updateFiles

    def getMissingList(self):
        return self.missingFiles

    def getIdenticalFiles(self):
        return self.identicalFiles
