import os
import subprocess
import time

import psutil

from core import logger, config


class Actions:
    def __init__(self):
        self.logger = logger.getInstance(__name__)
        self.conf = config.getInstance()

    def scanroom(self):
        print()

    def showRecordingRooms(self):
        rooms = self.getRecordingRooms()
        if len(rooms) == 0:
            self.logger.info("no recording room found.")
        else:
            for room in rooms:
                self.logger.info(f"pid:{room['pid']}\tstart at {room['time']}\troom id:{room['id']}\ttitle:{room['title']}")

    def killroom(self, roomid):
        roomids = roomid.split(",")
        rooms = self.getRecordingRooms()
        for idstr in roomids:
            flag = False
            for room in rooms:
                if idstr == room["id"]:
                    flag = True
                    self.logger.info(f"room {idstr} record process found, pid:{room['pid']}")
                    self.killpid(room['pid'])
                    self.logger.info(f"room {idstr} record process has been killed.")
                    break
            if not flag:
                self.logger.info(f"room {idstr} record process not found")

    def printFollowRooms(self):
        watchroomlist = self.conf.get_watchroomlist()
        for key in watchroomlist.keys():
            self.logger.info(f"{key}: {watchroomlist[key]}")


    '''-----------------------------------api-----------------------------------'''
    def buildCmd(self, roomid, title, url, is_cache=False):
        if url is None:
            return None
        else:
            nowtime = int(time.time())
            index = url.find("wsTime=")
            if index != -1:
                urltime = url[index + 7:index + 7 + 10]
                if nowtime - int(urltime) > (60 * 5):
                    self.logger.info(f"room id: {roomid}, title:{title} url is out of date. ")
                    return None

        timestr = time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        filename = roomid + "_" + title + timestr
        filename = "cached"+filename if is_cache else filename
        filepath = self.conf.get_record_file_path()
        cmdstr = self.conf.get_record_cmd_template() \
            .replace('${urlpath}', url) \
            .replace('${filepath}', filepath) \
            .replace('${filename}', filename)
        return f"nohup {cmdstr} >/dev/null 2>&1 &"

    def clearEmptyFile(self, dir_path):
        fl = os.listdir(dir_path)
        nowtime = int(time.time())
        for file in fl:
            real_path = os.path.join(dir_path, file)
            fsize = int(os.path.getsize(real_path))
            if fsize == 0 and nowtime - int(os.path.getmtime(real_path)) > (60 * 5):
                self.logger.info(f"delete empty file {real_path} ")
                os.remove(real_path)

    def getRecordingIds(self):
        rooms = self.getRecordingRooms()
        ids = []
        for room in rooms:
            ids.append(room['id'])
        return ids

    def getRecordingRooms(self):
        filepath = self.conf.get_record_file_path()
        rooms = []
        restrs = self.getRecordingCmds()

        nowtime = int(time.time())
        for runningcmdstr in restrs:
            if runningcmdstr == '':
                continue
            index = runningcmdstr.find(filepath)
            endindex = runningcmdstr.rfind(".")
            filename = runningcmdstr[index + len(filepath):endindex]
            room = {}
            strs = filename.split("_")
            room["pid"] = runningcmdstr.split()[0]
            room["id"] = strs[0]
            room["title"] = strs[1]
            room["time"] = f"{strs[2]}-{strs[3]}-{strs[4]} {strs[5]}:{strs[6]}:{strs[7]}"
            room["filefullpath"] = runningcmdstr[index:]

            # self.logger.info(f"filefullpath: {room['filefullpath']}")
            # self.logger.info(os.path.exists(room["filefullpath"]))
            # self.logger.info(f"nowtime {nowtime}")
            # self.logger.info(f"filetime {int(os.path.getmtime(room['filefullpath']))}")

            if not os.path.exists(room["filefullpath"]) \
                    or nowtime - int(os.path.getmtime(room["filefullpath"])) > (60 * 5):
                self.logger.info(f"room id: {room['id']}, title:{room['title']}, pid:{room['pid']} is zombie process. kill it...")
                self.killpid(room["pid"])
                if os.path.exists(room["filefullpath"]) and os.path.getsize(room["filefullpath"]) < 10:
                    self.logger.info("delete empty file "+room["filefullpath"])
                    os.remove(room["filefullpath"])
                continue

            rooms.append(room)

        return rooms

    def killpid(self, pid):
        cmd = f"kill {pid}"
        self.logger.info(f"send stop signal to {pid}")
        os.system(cmd)
        time.sleep(1)
        if psutil.pid_exists(int(pid)):
            self.logger.info(f"force kill process {pid}")
            cmd1 = f"kill -9 {pid}"
            os.system(cmd1)

    def getRecordingCmds(self):
        filepath = self.conf.get_record_file_path()
        cmd = f"ps -eo pid,command | grep {filepath} | grep -v grep"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0, shell=True)
        restr = process.stdout.read().decode()
        return restr.split("\n")