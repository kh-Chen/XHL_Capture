import os
import subprocess

from core import weiqun_platform, logger
from service import baseService


class Actions(baseService.Actions):
    def __init__(self):
        super(Actions, self).__init__()
        self.logger = logger.getInstance(__name__)

    def scanroom(self):
        self.logger.info("scanroom start...")
        roomlist = weiqun_platform.getRoomList()
        if len(roomlist) == 0:
            self.logger.info("room list is empty.")
            return
        self.logger.info(f"get current room list length {len(roomlist)}")
        recordingIds = self.getRecordingIds()
        watchroomlist = self.conf.get_watchroomlist()
        self.logger.debug(f"recordingIds: {recordingIds}")
        self.logger.debug(f"watchroomlist.keys: {list(watchroomlist.keys())}")
        for room in roomlist:
            if room['id'] in watchroomlist.keys():
                watchroomlist[room['id']] = room['title']
                self.logger.info(f"find watching room id: {room['id']}, title:{room['title']}")
                if room['id'] not in recordingIds:
                    self.logger.info(f"start record room id: {room['id']}, title:{room['title']}")
                    cmdstr = self.buildCmd(room['id'], room['title'], room['video'])
                    if cmdstr is not None:
                        subprocess.Popen(cmdstr, preexec_fn=os.setsid, bufsize=0, shell=True)
                else:
                    self.logger.info(f"room id: {room['id']} is already recording")

        self.conf.set_watchroomlist(watchroomlist)
        self.logger.info("scanroom end...")

    def start_record(self, roomidinput, url):
        recordingIds = self.getRecordingIds()
        if roomidinput in recordingIds:
            self.logger.info(f"room id: {roomidinput} is already recording")
            return

        if url != '':
            roomtitlecache = self.conf.get_roomtitlecache()
            title = roomtitlecache[roomidinput] if roomidinput in roomtitlecache.keys() else "未知"
            self.logger.info(f"start record room id: {roomidinput}, title:{title}, use input url")
            cmdstr = self.buildCmd(roomidinput, title, url)
            if cmdstr is not None:
                subprocess.Popen(cmdstr, preexec_fn=os.setsid, bufsize=0, shell=True)
        else:
            flag = False
            self.logger.info(f"searching room {roomidinput} info...")
            roomlist = weiqun_platform.getRoomList()
            for room in roomlist:
                if room['id'] == roomidinput:
                    self.logger.info(f"find room info: {room}")
                    self.logger.info(f"start record room id: {room['id']}, title:{room['title']}")
                    cmdstr = self.buildCmd(room['id'], room['title'], room['video'])
                    if cmdstr is not None:
                        subprocess.Popen(cmdstr, preexec_fn=os.setsid, bufsize=0, shell=True)
                    flag = True
                    break
            if not flag:
                self.logger.info(f"room id: {roomidinput} not found")

    def showAllRooms(self):
        rooms = weiqun_platform.getRoomList()
        if len(rooms) == 0:
            self.logger.info("room list is empty.")
        else:
            for room in rooms:
                self.logger.info(f"id:{room['id']}\ttitle:{room['title']}")

    def getRoomInfo(self, roomidinput):
        roomlist = weiqun_platform.getRoomList()
        flag = False
        for room in roomlist:
            if room['id'] == roomidinput:
                self.logger.info(f"find room info: \n{room}")
                flag = True
                break
        if not flag:
            self.logger.info(f"room id: {roomidinput} not found")

    def addDelFollow(self, roomidinput):
        watchroomlist = self.conf.add_del_watchroomlist(roomidinput, "")
        if roomidinput in watchroomlist.keys():
            self.logger.info(f"add follow {roomidinput} done.")
        else:
            self.logger.info(f"delete follow {roomidinput} done.")
