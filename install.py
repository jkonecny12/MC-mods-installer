#!/usr/bin/env python3

import downloader
import updater as updatelib
import os
import subprocess
import platform

# links to files
FORGE_LINK_LINUX_INSTALL='http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.7.10-10.13.2.1230/forge-1.7.10-10.13.2.1230-installer.jar'
FORGE_LINK_WIN_INSTALL='http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.7.10-10.13.2.1230/forge-1.7.10-10.13.2.1230-installer-win.exe'

MOD_SERVER = 'http://www.mod-buildcraft.com/releases/BuildCraft/6.3.1/buildcraft-6.3.1.jar'

PACKET_SEEKERS = 'http://packetseekers.dvratil.cz/MC-files/'
MOD_FILE = 'mods.csv'

WIN_FOLDER = os.path.expanduser('%appdata%/.minecraft/mods/')
LINUX_FOLDER = os.path.expanduser('~/.minecraft/mods/')


# read character from command line on any system
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


def get_current_os():
    """Get current system string and all linux like system set as Linux string.
    Windows string will be Windows
    """
    current_os = platform.system()

    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        return 'Linux'
    else:
        return current_os


def ask_answer(question):
    """'Print question and ask user to y/n input.
    Return True or False
    """
    print(question + ' [y/n]')

    c = kbhit()

    if c == 'y':
        return True
    else:
        return False


def install_forge():
    """Download and install forge.
    It will use installer depending on the platform.
    """
    if not ask_answer('Do you want to download and install Forge?'):
        return

    current_os = get_current_os()

    if current_os == 'Linux':
        download_forge_link = FORGE_LINK_LINUX_INSTALL
    elif current_os == 'Windows':
        download_forge_link = FORGE_LINK_WIN_INSTALL
    else:
        print(current_os + ' system is not supported')
        exit(1)

    download = downloader.Downloader()
    filename = download.download_file(download_forge_link, 'forge')

    if current_os == 'Linux':
        subprocess.call(['java', '-jar', filename])
    elif current_os == 'Windows':
        subprocess.call([filename])

    os.remove(filename)


def install_mods():
    """Download and install mods to minecraft mod folder.
    """
    current_os = get_current_os()
#    downloadObj = downloader.Downloader()
    mcdir = ''

    if current_os == 'Linux':
        mcdir = LINUX_FOLDER
    elif current_os == 'Windows':
        mcdir = WIN_FOLDER
    else:
        print(current_os + ' system is not supported')
        exit(1)

#    print(MOD_SERVER)
#    print('size: ' + downloadObj.getFileSize(MOD_SERVER))
#    filename = downloadObj.downloadFile(MOD_SERVER)
#    print('local size: ' + str(os.path.getsize(filename)))

    updater = updatelib.Updater()
    updater.set_paths(PACKET_SEEKERS + MOD_FILE, mcdir)
    if not updater.resolve_files():
        print('Local folder "' + mcdir + '" cannot be found!', file=sys.stderr)
        return


if __name__ == "__main__":
    install_forge()

    install_mods()

