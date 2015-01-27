#!/usr/bin/env python3

import downloader as downloadLib
import csv

class Updater:
    "Download csv file with Excel format with pattern:"
    "<base_file_name>;<server_file_name>;<MD5Checksum>\\n"
    "Compare files for update (bad MD5 or missing and return it the list."
    "Update files which user want to update."

    def __init__(self):
        self.serverCSVPath = ""
        self.localFolderPath = ""
        self.updateFiles = []
        self.missingFiles = []
        self.identicalFiles = []

    def setPaths(self, serverCSVPath, localFolderPath):
        self.serverCSVPath = serverCSVPath
        self.localFolderPath = localFolderPath

    def resolveFiles(self):
        "Download and parse server CSV file and compute MD5Checksums for local file"
        "If everything is allright return True, otherwise return False"

        if self.serverCSVPath == "":
            return False

        downloader = downloadLib.Downloader()

        filename = downloader.downloadFile(self.serverCSVPath, silent=True)

        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                print(row)


    def getUpdateList(self):
        return self.updateFiles

    def getMissingList(self):
        return self.missingFiles

    def getIdenticalFiles(self):
        return self.identicalFiles
