import os
import re
import subprocess
import threading
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from core import config, logger
from core.threads.recordingThread import UpdateThread
from view.QtDesinger.recordInfoUI import Ui_Form


class RecordInfoWin(QMainWindow, Ui_Form):
    def __init__(self, roomid, url, title, close_callback, *args, **kwargs):
        super(RecordInfoWin, self).__init__(*args, **kwargs)
        self.logger = logger.getInstance(__name__)
        self.conf = config.getInstance()
        self.update_thread = UpdateThread()
        # self.update_thread.signal_upd_filesize.connect(self.signal_upd_filesize_handler)
        # self.update_thread.signal_upd_timestr.connect(self.signal_upd_timestr_handler)
        self.update_thread.signal_upd_state.connect(self.signal_upd_state_handler)
        self.update_thread.signal_closed.connect(self.signal_closed_handler)
        self.url = url
        self.roomid = roomid
        self.title = title
        self.close_callback = close_callback
        self.setupUi(self)
        self.setWindowTitle(title)
        self.logger.debug(f"录制窗体初始化完成")

    def updUrl(self, url):
        self.logger.debug(f"update url:{url}")
        self.url = url

    def record(self):
        self.logger.debug(f"开始录制 {self.title}")
        cmd = self.buildCmd()
        self.logger.debug(cmd)
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0, shell=True)
        self.update_thread.set_process(process)
        self.update_thread.start()
        self.logger.debug(f"监视线程已启动 {self.title}")

    def signal_closed_handler(self, str):

        if str == '0':
            self.logger.debug(f"收到自动退出信号，{self.title} 再次尝试录制")
            self.timestrLabel.setText("waiting")
            self.record()
            return

        self.update_thread = None
        if str == '1':
            self.logger.debug(f"收到手动退出信号，{self.title} 录制结束 ")
        else:
            self.logger.debug(f"无效链接，{self.title} 录制结束 ")
        self.close()


    # def signal_upd_filesize_handler(self, size):
    #     self.filesizeLabel.setText(size)
    #
    # def signal_upd_timestr_handler(self, timestr):
    #     self.timestrLabel.setText(timestr)

    def signal_upd_state_handler(self, size, timestr, bitrate):
        self.filesizeLabel.setText(size)
        self.timestrLabel.setText(timestr)
        self.bitrateLabel.setText(bitrate)

    def buildCmd(self):
        timestr = time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        self.filename = self.roomid + "_" + self.title + timestr
        self.filepath = self.conf.get_record_file_path()
        self.filepathLabel.setText(os.path.join(self.filepath, self.filename))
        return self.conf.get_record_cmd_template() \
            .replace('${urlpath}', self.url) \
            .replace('${filepath}', self.filepath) \
            .replace('${filename}', self.filename)

    def closeEvent(self, event):
        self.logger.debug("触发关闭事件")
        if self.update_thread is not None:
            self.logger.debug("关闭线程")
            self.update_thread.stop()
            event.ignore()
            return

        self.logger.debug("窗口关闭")
        self.close_callback(self.roomid)
        event.accept()


