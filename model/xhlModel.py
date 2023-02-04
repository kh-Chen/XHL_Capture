from abc import ABC

from core import logger, xhl_platform
from model import baseModel

instanct = None


def getInstance(window):
    global instanct
    if not isinstance(instanct, Actions):
        instanct = Actions(window)
    return instanct


class Actions(baseModel.Actions, ABC):
    def __init__(self, window):
        super(Actions, self).__init__(window)
        self.logger = logger.getInstance(__name__)

    def get_room_list(self):
        roomlist = xhl_platform.get_hot_list()
        for room in roomlist:
            room['video'] = ''
        return roomlist

    def get_room_url(self, room):
        info = xhl_platform.get_room_info_by_roomid(room['id'])
        room['video'] = info['video']

    def get_room_info(self, row):
        roomid = self.window.tableWidget.item(row, 0).text()
        title = self.window.tableWidget.item(row, 1).text()
        info = xhl_platform.get_room_info_by_roomid(roomid)
        url = ""
        if info is None or "video" not in info.keys():
            self.logger.info(f"get room url error. id: {roomid}, title:{title}")
        else:
            url = info['video']

        return roomid, title, url
