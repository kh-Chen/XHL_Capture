import re

from PyQt5.QtCore import QThread, pyqtSignal

from core import logger


class UpdateThread(QThread):
    # signal_upd_filesize = pyqtSignal(str)
    # signal_upd_timestr = pyqtSignal(str)
    signal_upd_state = pyqtSignal(str, str, str)
    signal_closed = pyqtSignal(str)

    def __init__(self, parent=None):
        super(UpdateThread, self).__init__(parent)
        self.logger = logger.getInstance(__name__)
        self.process = None
        self.exitflag = 0

    def set_process(self, process):
        self.process = process

    def run(self) -> None:
        opened = False
        self.exitflag = 0
        if self.process is not None:
            while self.process.poll() is None:
                line = self.process.stderr.read(512).decode("UTF-8")
                size_res = re.search(r'\ssize=(\s*)(?P<size>\S+)', line)
                if size_res is not None:
                    size = size_res.groupdict()['size']
                    opened = True
                else:
                    size = ""
                time_res = re.search(r'\stime=(?P<time>\S+)', line)
                if time_res is not None:
                    timestr = time_res.groupdict()['time']
                else:
                    timestr = ""
                bitrate_res = re.search(r'\sbitrate=(\s*)(?P<bitrate>\S+)', line)
                if bitrate_res is not None:
                    bitrate = bitrate_res.groupdict()['bitrate']
                else:
                    bitrate = ""
                if size != '' or timestr != '' or bitrate != '':
                    self.signal_upd_state.emit(size, timestr, bitrate)
        self.logger.debug("ffmpeg结束，发射退出信号")
        if opened:
            self.signal_closed.emit(str(self.exitflag))
        else:
            self.signal_closed.emit("2")

    def stop(self):
        try:
            if not self.process.stdin.closed:
                self.exitflag = 1
                self.logger.debug("通知ffmpeg结束")
                self.process.stdin.write(b'q')
        except Exception as r:
            self.logger.debug(f'UpdateThread.stop 发生未知错误 {r}')