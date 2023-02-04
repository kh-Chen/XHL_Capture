import json
import time

import requests

from core import base64_crypt, logger, tools, config

HTTP_SCHEME = "http://"
linkForPickDomain = (
    "https://c502d384e3a0.oss-cn-beijing.aliyuncs.com/down/interface.txt",
    "https://app-api.vqapi.com/index.php",
    "https://app-api.vqapi.net/index.php")

variables = {}
logger = logger.getInstance(__name__)

errorjson = tools.getFilePathByRelativePath("error.json")

def getBaseUrl():
    for url in linkForPickDomain:
        redata = requests.get(url)
        if redata.status_code == requests.codes.ok:
            baseurldatas = redata.json()
            break

    for baseurldata in baseurldatas['data']:
        redata = requests.get(baseurldata['url'])
        if redata.status_code == requests.codes.ok:
            variables['baseurl'] = baseurldata['url']
            break


def getUrlForRoomList():
    if 'baseurl' not in variables.keys():
        getBaseUrl()

    categorys_url = variables['baseurl'] + "index/live/live_categorys"
    params = {}
    jsonstr = json.dumps(params)
    enstr = base64_crypt.getInstance().encrypt(jsonstr)

    categorys_rep = requests.post(url=categorys_url, params={"params": enstr})
    if categorys_rep.status_code == requests.codes.ok:
        en_categorys_json = categorys_rep.content.decode("UTF-8")
        categorys_json = base64_crypt.getInstance().decrypt(en_categorys_json)
        categorys = json.loads(categorys_json)
        remen = categorys['lists'][0]
        variables['remenurl'] = remen['url']


def getRoomList():
    if "roomlistcache_time" in variables.keys():
        if (int(time.time())-variables['roomlistcache_time']) <= 10:
            logger.debug(f"get room list using cache.")
            return variables['roomlistcache']

    roomlist_json = ""
    try:
        if 'remenurl' not in variables.keys():
            getUrlForRoomList()

        r = requests.get(variables['remenurl'], stream=True)
        b = "".encode()
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                b = b+chunk

        enstr = b.decode("UTF-8")
        roomlist_json = base64_crypt.getInstance().decrypt(enstr)
        roomlist = json.loads(roomlist_json)
        listdata = roomlist['data']
        variables['roomlistcache'] = listdata
        variables['roomlistcache_time'] = int(time.time())

        roomtitlecache = config.getInstance().get_roomtitlecache()

        outdatanum = 0
        curnum = 0
        for room in listdata[:]:
            roomtitlecache[room['id']] = room['title']
            url = room['video']
            index = url.find("wsTime=")
            if index != -1:
                urltime = url[index + 7:index + 7 + 10]
                if variables['roomlistcache_time'] - int(urltime) > (60 * 5):
                    outdatanum += 1
                    listdata.remove(room)
                    continue

                indexsign = url.find("&sign=")
                room['video'] = url[0:indexsign]
            else:
                listdata.remove(room)
                continue
            curnum += 1

        config.getInstance().set_roomtitlecache(roomtitlecache)
        logger.info(f"new room list outdatanum: {outdatanum}, curnum: {curnum} ")
        return listdata
    except Exception as r:
        logger.debug(f"未知错误 {r}")
        if roomlist_json != "":
            with open(errorjson, "a", encoding='UTF-8') as file:
                file.write(roomlist_json)
                file.write(
                    "\r\n--------------------------------------------------------------------------------------\r\n")

        return []







# if __name__ == '__main__':
#     list = getRoomList()
#     logger.get_log().debug(list)
#     base64_crypt.destoryInstance()
