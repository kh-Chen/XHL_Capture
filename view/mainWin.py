import time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView, QTableWidgetItem

from core import config, logger, tools

from core.threads.playingThread import PlayThread
from model import xhlModel, wqModel
from view.QtDesinger.mainWinUI import Ui_Form
from view.playerWin import PlayerWin
from view.recordInfoWin import RecordInfoWin


class MainWin(QMainWindow, Ui_Form):
    def __init__(self, *args, **kwargs):
        self.conf = config.getInstance()
        self.logger = logger.getInstance(__name__)

        super(MainWin, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('小狐狸直播监听V1.0')
        self.timer = QTimer()  # 计时器
        self.timer.timeout.connect(self.refreshTable)

        self.tableWidget.setRowHeight(0, 30)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(0, 70)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setColumnWidth(2, 50)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只有行选中
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.tableWidget.setColumnWidth(0, 70)
        # self.tableWidget.setColumnWidth(1, 80)
        # self.tableWidget.setColumnWidth(2, 40)
        # self.tableWidget.setColumnWidth(3, 389)
        self.handleBox.addItem("预览", "preview")
        self.handleBox.addItem("播放", "play")
        self.handleBox.addItem("录制", "record")

        self.sourceBox.addItem("微群", "weiqun")
        self.sourceBox.addItem("官方", "xhl")

        self.refreshBtn.clicked.connect(self.refreshTable)
        self.previewBtn.clicked.connect(self.previewBtnHeadler)
        self.playBtn.clicked.connect(self.playBtnHandler)
        self.recordBtn.clicked.connect(self.recordBtnHandle)
        self.addfollowBtn.clicked.connect(self.addfollowBtnHandler)
        self.editfollowBtn.clicked.connect(self.editfollowBtnHandler)
        self.sendStreamBtn.clicked.connect(self.sendStreamBtnHandler)

        self.autoRefreshBox.stateChanged.connect(self.autoRefreshBoxChanged)
        self.autoRefreshBox.setChecked(True)

    def get_model(self):
        handle = self.sourceBox.currentData()
        if handle == 'xhl':
            return xhlModel.getInstance(self)
        elif handle == 'weiqun':
            return wqModel.getInstance(self)

    def refreshTable(self):
        oldselectroomid = ''
        if self.tableWidget.currentItem():
            row = self.tableWidget.currentRow()
            oldselectroomid = self.tableWidget.item(row, 0).text()

        playinghiderooms, playingshowrooms, watchingrooms, normalrooms = self.get_model().get_table_data()

        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()

        for room in playinghiderooms:
            self.tableinsertdata(room, QColor(255, 0, 0))
        for room in playingshowrooms:
            self.tableinsertdata(room, QColor(0, 255, 0))
        for room in watchingrooms:
            self.tableinsertdata(room, QColor(0, 0, 255))
        for room in normalrooms:
            self.tableinsertdata(room, None)
        self.logger.debug(f"房间刷新完成")
        # self.conf.set_watchroomlist(watchroomlist)
        if oldselectroomid != '':
            olditem = self.tableWidget.findItems(str(oldselectroomid), Qt.MatchExactly)
            if len(olditem) != 0:
                self.tableWidget.selectRow(olditem[0].row())

        self.setTip("房间列表已刷新")

    def tableinsertdata(self, room, color):
        index = self.tableWidget.rowCount()
        self.tableWidget.insertRow(index)
        self.tableWidget.setItem(index, 0, QTableWidgetItem(str(room['id'])))
        self.tableWidget.setItem(index, 1, QTableWidgetItem(str(room['title'])))
        self.tableWidget.setItem(index, 2, QTableWidgetItem(str(room['status'])))
        self.tableWidget.setItem(index, 3, QTableWidgetItem(str(room['video'])))
        if color is not None:
            self.tableWidget.item(index, 0).setForeground(QBrush(color))
            self.tableWidget.item(index, 1).setForeground(QBrush(color))
            self.tableWidget.item(index, 2).setForeground(QBrush(color))
            self.tableWidget.item(index, 3).setForeground(QBrush(color))

        self.tableWidget.setRowHeight(index, 14)

    def watchingroomautohanler(self, room):
        watchflag = self.watchRoomBox.isChecked()

        if watchflag:
            handle = self.handleBox.currentData()
            self.logger.debug(f"自动处理房间： {room['title']}")
            if handle == 'play':
                self.logger.debug(f"播放： {room['title']}")
                self.play(room['id'], room['video'], room['title'])
            elif handle == 'preview':
                self.logger.debug(f"预览： {room['title']}")
                self.preview(room['id'], room['video'], room['title'])
            elif handle == 'record':
                self.logger.debug(f"录制： {room['title']}")
                self.recordurl(room['id'], room['video'], room['title'])

    def autoRefreshBoxChanged(self):
        if self.autoRefreshBox.isChecked():
            self.timer.start(int(self.conf.get_auto_refresh_time_interval()))
        else:
            self.timer.stop()

    def playBtnHandler(self):
        if self.tableWidget.currentItem():
            row = self.tableWidget.currentRow()
            roomid, title, url = self.get_model().get_room_info(row)
            self.play(roomid, url, title)

    def play(self, roomid, url, title):
        if self.get_model().find_play_thread(roomid) is None:
            self.logger.info(f"调用外部播放器..")
            p = PlayThread()
            self.get_model().add_play_thread(roomid, p)
            p.signal_closed.connect(self.playProcessExit)
            p.updUrl(url)
            p.set_title(title)
            p.set_roomid(roomid)
            cmd, pname = p.buildcmd()
            pid = tools.runCmdRePid(cmd, pname)
            self.logger.info(f"找到pid {pid}")
            p.set_pid(pid)
            p.start()
        else:
            self.logger.debug(f"房间已处理且正在生效中，本次忽略")

    def playProcessExit(self, roomid):
        self.logger.debug(f"playProcessExit {roomid}")
        self.get_model().del_play_thread(roomid)

    def previewBtnHeadler(self):
        if self.tableWidget.currentItem():
            row = self.tableWidget.currentRow()
            roomid, title, url = self.get_model().get_room_info(row)
            self.preview(roomid, url, title)

    def preview(self, roomid, url, title):
        if self.get_model().find_player_win(roomid) is None:
            pw = PlayerWin(roomid=roomid, title=title, close_callback=self.playerWinClosed)
            pw.show()
            pw.play(url)
            self.get_model().add_palayer_win(roomid, pw)
            self.logger.debug(f"房间已成功处理")
        else:
            self.logger.debug(f"房间已处理且正在生效中，本次忽略")

    def playerWinClosed(self, roomid):
        self.logger.debug(f"playerWinClosed {roomid}")
        self.get_model().del_palayer_win(roomid)

    def recordBtnHandle(self):
        if self.tableWidget.currentItem():
            row = self.tableWidget.currentRow()
            roomid, title, url = self.get_model().get_room_info(row)
            self.recordurl(roomid, url, title)

    def recordurl(self, roomid, url, title):
        if self.get_model().find_record_win(roomid) is None:
            riw = RecordInfoWin(roomid=roomid, title=title, url=url, close_callback=self.recordWinClosed)
            riw.show()
            self.get_model().add_record_win(roomid, riw)
            riw.record()
            self.logger.debug(f"房间已成功处理")
        else:
            self.logger.debug(f"房间已处理且正在生效中，本次忽略")

    def recordWinClosed(self, roomid):
        self.logger.debug(f"recordWinClosed {roomid}")
        self.get_model().del_record_win(roomid)
        self.setTip(f"房间 {roomid} 录制已结束")

    def addfollowBtnHandler(self):
        if self.tableWidget.currentItem():
            row = self.tableWidget.currentRow()
            roomid = self.tableWidget.item(row, 0).text()
            title = self.tableWidget.item(row, 1).text()
            self.conf.add_del_watchroomlist(roomid, title)

    def sendStreamBtnHandler(self):
        if self.tableWidget.currentItem():
            row = self.tableWidget.currentRow()
            roomid = self.tableWidget.item(row, 0).text()
            ids = self.getsendStreamIds()
            if roomid in ids:
                cmd = f"kill -9 `ps -eo pid,command | grep {roomid} | grep -v grep | awk '{{print $1}}'`"
                self.ssh.exec_command(cmd)
                self.logger.debug(f"run ssh: {cmd}")
                self.setTip("已停止转推流命令")
            else:
                url = self.tableWidget.item(row, 3).text()
                cmdstr = self.conf.get_value_by_key('forward', 'forward_cmd_template') \
                    .replace('${urlpath}', url) \
                    .replace('${roomid}', roomid)
                cmd = f"{cmdstr} 2> /dev/null &"
                self.ssh.exec_command(cmd)
                self.logger.debug(f"run ssh: {cmd}")
                self.setTip("已发送转推流命令")

    def editfollowBtnHandler(self):
        print()

    def setTip(self, tipstr):
        timestr = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(time.time()))
        self.tipLabel.setText(timestr + tipstr)

    def closeEvent(self, event):
        if hasattr(self, 'autoRefreshThread'):
            self.autoRefreshThread.stop()

        self.get_model().close()

        self.logger.debug(f"主窗口退出")
        event.accept()
