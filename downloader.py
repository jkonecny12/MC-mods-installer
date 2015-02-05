#!/usr/bin/env python3

import urllib.request
import terminalsize

class Downloader:
    """Download file and show progress in command line
    """


    def __init__(self):
        self.fileName = ''


    def _report_download(self, blocks_download, block_size, file_size):
        """Print progress of the actual download
        """
        size_downloaded = int(block_size * blocks_download / 1024)
        total_size = int(file_size / 1024)
        percent_down = 0.0

        if size_downloaded != 0:
            percent_down = size_downloaded / total_size

        term_width = terminalsize.get_terminal_size()[0]

        if not size_downloaded < total_size:
            size_downloaded = total_size

        leftmsg = (self.fileName + '  [')
        rightmsg = '] ' + str(size_downloaded) + ' / ' + str(total_size) + ' KB'
        leftsize = len(leftmsg)
        console_space = term_width - (leftsize + 20) # plus 16 to have a reserve from end with right message for showing size
        show_num_sharps = int(console_space * percent_down)

        print(leftmsg.ljust(show_num_sharps + leftsize, '#').ljust(console_space + leftsize) + rightmsg, end='\r')

        if not size_downloaded < total_size:
            print('')


    def download_file(self, link, name = "", silent = False):
        """Download file and register for creating graphical progress
        """
        if not silent:
            if not name:
                self.fileName = link.split('/')[-1]
            else:
                self.fileName = name

            (filename, headers) = urllib.request.urlretrieve(link, reporthook=self._report_download)

        else:
            (filename, headers) = urllib.request.urlretrieve(link)

        return filename


    def getFileSize(self, link):
        """Get size of the file on given link
        """
        site = urllib.request.urlopen(link)
        meta = site.info()

        #print(int(meta.get('Content-Length')))

        return meta.get('Content-Length')

