import os
import subprocess
import time

from core import xhl_platform, logger
from service import baseService


class Actions(baseService.Actions):
    def __init__(self):
        super(Actions, self).__init__()
        self.logger = logger.getInstance(__name__)

    def scanroom(self):
        self.logger.info("scanroom start...")
        self.clearEmptyFile(self.conf.get_record_file_path())
        roomlist = xhl_platform.get_online_friends()

        # roomlist = xhl_platform.get_hot_list()
        if len(roomlist) == 0:
            self.logger.info("room list is empty.")
            return
        self.logger.info(f"get current room list length {len(roomlist)}")

        recordingIds = self.getRecordingIds()
        # watchroomlist = self.conf.get_watchroomlist()
        self.logger.debug(f"recordingIds: {recordingIds}")
        # self.logger.debug(f"watchroomlist.keys: {list(watchroomlist.keys())}")
        for room in roomlist:
            # if room['id'] in watchroomlist.keys():
            #     watchroomlist[room['id']] = room['title']
            self.logger.info(f"find watching room id: {room['id']}, title:{room['title']}")
            if room['id'] not in recordingIds:
                self.logger.info(f"start record room id: {room['id']}, title:{room['title']}")
                info = xhl_platform.get_room_info_by_roomid(room['id'])
                if info is None or "video" not in info.keys():
                    self.logger.info(f"get room url error. id: {room['id']}, title:{room['title']}")
                    continue
                cmdstr = self.buildCmd(room['id'], room['title'], info['video'], info['is_cache'])
                if cmdstr is not None:
                    subprocess.Popen(cmdstr, preexec_fn=os.setsid, bufsize=0, shell=True)
            else:
                self.logger.info(f"room id: {room['id']} is already recording")
                xhl_platform.get_room_url_by_roomid(room['id'])

            # else:
            # self.logger.info(f"room id: {room['id']} is not follow")
        # self.conf.set_watchroomlist(watchroomlist)
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
            self.logger.info(f"searching room {roomidinput} info...")
            room = xhl_platform.get_room_info_by_roomid(roomidinput)
            if room is not None and "video" in room.keys():
                self.logger.info(f"find room info: {room}")
                self.logger.info(f"start record room id: {room['id']}, title:{room['title']}")
                cmdstr = self.buildCmd(room['id'], room['title'], room['video'], room['is_cache'])
                if cmdstr is not None:
                    subprocess.Popen(cmdstr, preexec_fn=os.setsid, bufsize=0, shell=True)
            else:
                self.logger.info(f"room id: {roomidinput} not found")

    def showAllRooms(self):
        rooms = xhl_platform.get_hot_list()
        if len(rooms) == 0:
            self.logger.info("room list is empty.")
        else:
            for room in rooms:
                self.logger.info(f"id:{room['id']}\ttitle:{room['title']}")

    def showAllXHLFollowers(self):
        lst = xhl_platform.get_all_follow()
        lst.sort(key=lambda item: int(item['id']))
        for room in lst:
            timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(room['lastlogtime'])))
            self.logger.info(f"{timestr} \t {room['id']} \t {room['title']}")

    def getRoomInfo(self, roomidinput):
        room = xhl_platform.get_room_info_by_roomid(roomidinput)
        if room is not None:
            self.logger.info(f"find room info: \n{room}")
        else:
            self.logger.info(f"room id: {roomidinput} not found")

    def addDelFollow(self, roomidinput):
        lists = self.conf.get_watchroomlist()
        if roomidinput in lists.keys():
            del lists[roomidinput]
            self.conf.set_watchroomlist(lists)
            self.logger.info(f"delete follow {roomidinput} done.")
        else:
            info = xhl_platform.get_user_info(roomidinput)
            lists[roomidinput] = info['title']
            self.conf.set_watchroomlist(lists)
            self.logger.info(f"add follow {roomidinput} done.")
