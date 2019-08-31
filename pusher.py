import inspect
import os
import time
from ftplib import FTP

os.system('cls')


def time_to_string(g):
    return '{:0>2}{:0>2}{:0>2}{:0>2}{:0>2}'.format(
        g.tm_year % 100, g.tm_mon, g.tm_mday, g.tm_hour, g.tm_min
    )


ftp = FTP('81.13.173.100', 'markettkpoe', '123456')

with os.scandir() as dir_entries:
    for entry in dir_entries:
        info = entry.stat()
        time_last_modif = time_to_string(time.gmtime(info.st_mtime + 7200))
        last_id = 0
        if entry.name == 'main.py':
            path = '1.0\\{}'.format(time_last_modif)
            if not os.path.exists(path):
                os.mkdir(path)
                print('FOLDER {} CREATED'.format(time_last_modif))

                new_filename = '{}_{}.py'.format(
                    entry.name[::-1][3:][::-1], time_last_modif)
                os.system('copy {} 1.0\\{}\\{}'.format(
                    entry.name, time_last_modif, new_filename))
                print('FILE COPIED')

                file = open(
                    '1.0/{}/{}'.format(time_last_modif, new_filename), 'rb')

                ftp.mkd('/markettkpoe/1.0/{}'.format(time_last_modif))
                ftp.sendcmd('CWD /markettkpoe/1.0/{}'.format(time_last_modif))
                ftp.storbinary('STOR {}'.format(new_filename), file)

                file.close()


ftp.dir('/markettkpoe/1.0')
ftp.close()

os.system('PAUSE')
