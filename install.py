#!/usr/bin/env python3

import downloader
import os
import subprocess
import platform

# links to files
forgeLinkLinuxInstall='http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.7.10-10.13.2.1230/forge-1.7.10-10.13.2.1230-installer.jar'
forgeLinkWinInstall='http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.7.10-10.13.2.1230/forge-1.7.10-10.13.2.1230-installer-win.exe'

try:
    from msvcrt import kbhit
except ImportError:
    import termios, fcntl, sys, os
    def kbhit():
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
        try:
            while True:
                try:
                    c = sys.stdin.read(1)
                    if len(c) > 0:
                        return c
                except IOError:
                    return ''
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)



def getCurrentOS():
    'Get current system string and all linux like system set as Linux string.'
    'Windows string will be Windows'
    currentOS = platform.system()

    if currentOS in ['Linux', 'Darwin'] or currentOS.startswith('CYGWIN'):
        return 'Linux'
    else:
        return currentOS


def askAnswer(question):
    'Print question and ask user to y/n input.'
    'Return True or False'
    print(question + ' [y/n]')

    c = kbhit()

    if c == 'y':
        return True
    else:
        return False


def installForge():
    'Download and install forge.'
    'It will use installer depending on the platform.'

    if not askAnswer('Do you want to download and install Forge?'):
        return

    currentOS = getCurrentOS()

    if currentOS == 'Linux':
        downloadForgeLink = forgeLinkLinuxInstall
    elif currentOS == 'Windows':
        downloadForgeLink = forgeLinkWinInstall
    else:
        print(currentOS + ' system is not supported')
        exit(1)

    download = downloader.Downloader()
    filename = download.downloadFile(downloadForgeLink, 'forge')

    if currentOS == 'Linux':
        subprocess.call(['java', '-jar', filename])
    elif currentOS == 'Windows':
        subprocess.call([filename])

    os.remove(filename)



if __name__ == "__main__":
    installForge()

