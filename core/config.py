import configparser
import json
import os
# from pathlib import Path

from core import logger, tools

instanct = None


def getInstance():
    global instanct
    if not isinstance(instanct, Config):
        instanct = Config()
    return instanct


class Config:
    def __init__(self, path: str = "config.ini"):
        self.logger = logger.getInstance(__name__)
        # path_search_order = (
        #     Path(path),
        #     tools.getFilePathByRelativePath("config.ini")
        # )
        ini_path = tools.getFilePathByRelativePath("config.ini")
        # for p in path_search_order:
        #     if p.is_file():
        #         ini_path = p.resolve()
        #         break
        if ini_path:
            self.logger.debug(f"find config.ini at {ini_path}")
            self.conf = configparser.ConfigParser()
            self.ini_path = ini_path
            self.conf.read(ini_path, encoding="utf-8-sig")
        else:
            self.logger.debug("config.ini not found")

    def get_room_url_cache(self):
        jsonpath = tools.getFilePathByRelativePath("room_urls.json")
        jsonstr = "{}"
        if os.path.exists(jsonpath):
            with open(jsonpath, "r") as f:
                jsonstr = f.read()
        return json.loads(jsonstr)

    def get_last_room_url(self, roomid):
        urls = self.get_room_url_cache()
        if roomid in urls:
            return urls[roomid]
        else:
            return None

    def set_room_url_cache(self, roomid, url):
        jsonpath = tools.getFilePathByRelativePath("room_urls.json")
        urls = self.get_room_url_cache()
        urls[roomid] = url
        with open(jsonpath, "w") as f:
            f.write(json.dumps(urls, indent=3))

    def get_watchroomlist(self):
        jsonpath = tools.getFilePathByRelativePath("follow_rooms.json")
        jsonstr = "{}"
        if os.path.exists(jsonpath):
            with open(jsonpath, "r") as f:
                jsonstr = f.read()

        return json.loads(jsonstr)

    def set_watchroomlist(self, data):
        jsonpath = tools.getFilePathByRelativePath("follow_rooms.json")
        with open(jsonpath, "w") as f:
            f.write(json.dumps(data, indent=3))

    def add_del_watchroomlist(self, roomid, title):
        lists = self.get_watchroomlist()
        if roomid in lists.keys():
            del lists[roomid]
        else:
            lists[roomid] = title

        self.set_watchroomlist(lists)
        return lists

    def get_roomtitlecache(self):
        jsonpath = tools.getFilePathByRelativePath("room_title_cache.json")
        jsonstr = "{}"
        if os.path.exists(jsonpath):
            with open(jsonpath, "r") as f:
                jsonstr = f.read()

        return json.loads(jsonstr)

    def set_roomtitlecache(self, data):
        jsonpath = tools.getFilePathByRelativePath("room_title_cache.json")
        with open(jsonpath, "w") as f:
            f.write(json.dumps(data, indent=3))

    def get_player_path(self):
        return self.conf.get('play', 'player_path')

    def get_play_cmd_template(self):
        return self.conf.get('play', 'play_cmd_template')

    def get_record_cmd_template(self):
        return self.conf.get('record', 'record_cmd_template')

    def get_record_file_path(self):
        return self.conf.get('record', 'record_file_path')

    def get_forward_cmd_template(self):
        return self.conf.get('forward', 'forward_cmd_template')

    def get_auto_refresh_time_interval(self):
        return self.conf.get('main', 'auto_refresh_time_interval')

    def get_mode(self):
        return self.conf.get('main', 'mode')

    def get_XHL_token(self):
        return self.conf.get('XHL', 'token')

    def get_XHL_Butter2(self):
        return self.conf.get('XHL', 'XLiveButter2')

    def get_XHL_baseurl(self):
        return self.conf.get('XHL', 'baseurl')

    def get_value_by_key(self, section, option):
        return self.conf.get(section, option)




