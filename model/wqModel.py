from abc import ABC

from core import logger, weiqun_platform
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
        roomlist = weiqun_platform.getRoomList()
        for room in roomlist:
            room['video'] = room['video'].split()[0]
        return roomlist

    def get_room_url(self, room):
        pass

    def get_room_info(self, row):
        roomid = self.window.tableWidget.item(row, 0).text()
        title = self.window.tableWidget.item(row, 1).text()
        url = self.window.tableWidget.item(row, 3).text()
        return roomid, title, url


