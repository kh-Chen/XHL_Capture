from PyQt5.QtWidgets import QMainWindow

from core import logger
from core.vlc import Player
from view.QtDesinger.playerUI import Ui_Form


class PlayerWin(QMainWindow, Ui_Form):
    def __init__(self, roomid, title, close_callback, *args, **kwargs):
        super(PlayerWin, self).__init__(*args, **kwargs)
        self.logger = logger.getInstance(__name__)
        self.title = title
        self.roomid = roomid
        self.close_callback = close_callback
        self.setupUi(self)
        self.setWindowTitle(title)
        self.player = Player()
        self.player.set_window(self.frame.winId())
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.valueChanged.connect(self.volumeChange)
        self.volumeSlider.setValue(25)
        self.player.add_listener("MediaPlayerTimeChanged", self.timeUpdate)
        self.player.add_listener("MediaPlayerStopped", self.MediaPlayerStoppedEvent)
        self.player.add_listener("MediaPlayerEncounteredError", self.MediaPlayerEncounteredErrorEvent)
        self.player.add_listener("MediaPlayerEndReached", self.MediaPlayerEndReachedEvent)
        self.player.add_listener("MediaPlayerNothingSpecial", self.MediaPlayerNothingSpecialEvent)
        self.logger.debug(f"预览窗体初始化成功 {self.title}")

    def play(self, rtmp_url):
        self.url = rtmp_url
        self.logger.debug(f"预览窗体开始播放 {self.title}")
        self.player.play(rtmp_url)

    def updUrl(self, url):
        self.logger.debug(f"update url:{url}")
        self.url = url

    def timeUpdate(self, event):
        m, s = divmod(self.player.get_time() / 1000, 60)
        h, m = divmod(m, 60)
        self.timeLabel.setText("%02d:%02d:%02d" % (h, m, s))

    def MediaPlayerStoppedEvent(self, event):
        self.logger.debug("MediaPlayerStopped")

    def MediaPlayerEncounteredErrorEvent(self, event):
        self.logger.debug("MediaPlayerEncounteredError")

    def MediaPlayerEndReachedEvent(self, event):
        self.logger.debug("MediaPlayerEndReached")

    def MediaPlayerNothingSpecialEvent(self, event):
        self.logger.debug("MediaPlayerNothingSpecial")

    def volumeChange(self):
        self.player.set_volume(self.volumeSlider.value()+50)

    def closeEvent(self, event):
        self.player.stop()
        self.player.release()
        self.close_callback(self.roomid)
        self.logger.debug(f"预览窗体关闭 {self.title}")
        event.accept()
