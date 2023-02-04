import os
import threading

import psutil
from PyQt5.QtCore import QThread, pyqtSignal

from core import config, logger


class PlayThread(QThread):
    signal_closed = pyqtSignal(str)
    def __init__(self, parent=None):
        super(PlayThread, self).__init__(parent)
        self.logger = logger.getInstance(__name__)
        self.conf = config.getInstance()
        self.exitflag = False
        self.logger.info(f"外部播放器监视线程初始化完成")

    def set_pid(self, pid):
        self.logger.debug(f"set_pid:{pid}")
        self.pid = pid

    def updUrl(self, url):
        self.logger.debug(f"update url:{url}")
        self.url = url

    def set_title(self, title):
        self.logger.debug(f"set_title:{title}")
        self.title = title

    def set_roomid(self, roomid):
        self.logger.debug(f"set_roomid:{roomid}")
        self.roomid = roomid

    def buildcmd(self):
        cmd = self.conf.get_play_cmd_template() \
            .replace('${player}', self.conf.get_player_path()) \
            .replace('${urlpath}', self.url)
        pname = os.path.split(self.conf.get_player_path())[1]
        return cmd, pname

    def run(self):
        self.logger.info(f"开始pid监视 pid:{self.pid}")
        while not self.exitflag:
            if self.pid in psutil.pids():
                self.sleep(1)
            else:
                self.logger.info(f"pid监视完成，对应进程已退出 {self.title}, pid:{self.pid}")
                self.signal_closed.emit(self.roomid)
                break
        self.logger.debug(f"线程退出 {self.title}")

    def stop(self):
        self.exitflag = True

