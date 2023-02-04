from abc import ABCMeta, abstractmethod

import paramiko

from core import logger, config


class Actions:
    __metaclass__ = ABCMeta

    def __init__(self, window):
        self.logger = logger.getInstance(__name__)
        self.conf = config.getInstance()
        self.window = window
        self.play_thread_pool = {}
        self.recordwins = {}
        self.playerwins = {}

        if self.conf.get_value_by_key("RTMPServer", "hostname") != "":
            self.ssh = paramiko.SSHClient()
            know_host = paramiko.AutoAddPolicy()
            self.ssh.set_missing_host_key_policy(know_host)
            self.ssh.connect(
                hostname=self.conf.get_value_by_key("RTMPServer", "hostname"),
                port=self.conf.get_value_by_key("RTMPServer", "port"),
                username=self.conf.get_value_by_key("RTMPServer", "username"),
                password=self.conf.get_value_by_key("RTMPServer", "password")
            )
        else:
            self.ssh = None

    @abstractmethod
    def get_room_list(self):
        raise NotImplementedError("Must override get_room_list")

    @abstractmethod
    def get_room_url(self, room):
        raise NotImplementedError("Must override get_room_url")

    def get_table_data(self):
        roomlist = self.get_room_list()
        self.logger.debug(f"refresh room list count {len(roomlist)}")
        if len(roomlist) == 0:
            self.window.setTip("加载房间列表失败")
            return

        watchroomlist = self.conf.get_watchroomlist()
        sendStreamIds = self.getsendStreamIds()
        playingroomids_t = list(self.play_thread_pool.keys()) + \
                           list(self.playerwins.keys()) + \
                           list(self.recordwins.keys()) + \
                           sendStreamIds

        playingroomids = list(set(playingroomids_t))
        self.logger.debug(f"playingroomids: {playingroomids}")
        newroomids = []
        for room in roomlist:
            newroomids.append(str(room['id']))

        playinghiderooms = []
        playingshowrooms = []
        for playingroomid in playingroomids:
            if playingroomid in sendStreamIds:
                status = '转推中'
            else:
                status = '运行中'
            if playingroomid not in newroomids:
                olditem = self.window.tableWidget.findItems(str(playingroomid), Qt.MatchExactly)
                ip = self.conf.get_value_by_key("RTMPServer", "hostname")
                if len(olditem) != 0:
                    rowindex = olditem[0].row()
                    oldtitle = self.window.tableWidget.item(rowindex, 1).text()
                    if playingroomid in sendStreamIds:
                        oldurl = f"rtmp://{ip}:1935/live/{playingroomid} "
                    else:
                        oldurl = self.window.tableWidget.item(rowindex, 3).text()
                else:
                    oldurl = f"rtmp://{ip}:1935/live/{playingroomid} "
                    oldtitle = '未知'
                playinghiderooms.append({
                    'id': str(playingroomid),
                    'title': oldtitle,
                    'status': status,
                    'video': oldurl
                })
            else:
                for room in roomlist:
                    roomid = str(room['id'])
                    if roomid == playingroomid:
                        room['status'] = status
                        playingshowrooms.append(room)
                        self.get_room_url(room)
                        if roomid in self.play_thread_pool.keys():
                            self.play_thread_pool[roomid].updUrl(str(room['video']))
                        elif roomid in self.playerwins.keys():
                            self.playerwins[roomid].updUrl(str(room['video']))
                        elif roomid in self.recordwins.keys():
                            self.recordwins[roomid].updUrl(str(room['video']))
                        break
        self.logger.debug(f"playingroom handle done")
        watchingrooms = []
        normalrooms = []
        for room in roomlist:
            if 0 < len(room['video']) < 60:
                continue
            roomid = str(room['id'])
            if roomid not in sendStreamIds and roomid in playingroomids:
                continue

            if roomid in watchroomlist.keys():
                if roomid not in sendStreamIds:
                    room['status'] = '已关注'
                    watchingrooms.append(room)
                    watchroomlist[room['id']] = room['title']

                self.window.watchingroomautohanler(room)
            else:
                room['status'] = ''
                normalrooms.append(room)

        self.logger.debug(f"房间分类完成")
        self.conf.set_watchroomlist(watchroomlist)
        return playinghiderooms, playingshowrooms, watchingrooms, normalrooms

    def getsendStreamIds(self):
        ids = []
        if self.ssh is not None:
            stdin, stdout, stderr = self.ssh.exec_command("ps -eo command | grep localhost | grep -v grep")
            restr = stdout.read().decode()
            restrs = restr.split("\n")

            for cmdline in restrs:
                if cmdline != '':
                    index1 = cmdline.rfind('/') + 1
                    ids.append(cmdline[index1:])

        return ids

    def add_play_thread(self, key, thread):
        self.play_thread_pool[key] = thread

    def del_play_thread(self, key):
        del self.play_thread_pool[key]

    def find_play_thread(self, key):
        if key not in self.play_thread_pool.keys():
            return None
        else:
            return self.play_thread_pool[key]

    def add_palayer_win(self, key, win):
        self.playerwins[key] = win

    def del_palayer_win(self, key):
        del self.playerwins[key]

    def find_player_win(self, key):
        if key not in self.playerwins.keys():
            return None
        else:
            return self.playerwins[key]

    def add_record_win(self, key, win):
        self.recordwins[key] = win

    def del_record_win(self, key):
        del self.recordwins[key]

    def find_record_win(self, key):
        if key not in self.recordwins.keys():
            return None
        else:
            return self.recordwins[key]

    def close(self):
        for key in self.play_thread_pool.keys():
            self.play_thread_pool[key].stop()

        if self.ssh is not None:
            self.ssh.close()