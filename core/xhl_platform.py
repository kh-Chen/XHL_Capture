import json
import time
import brotli
import requests
from core import base64_crypt, logger, tools, config


logger = logger.getInstance(__name__)


# rep = requests.get("https://0djxrjui.shdkw1o.com/OpenAPI/v1/index/ping")
# if rep.status_code == requests.codes.ok:
#     en_categorys_json = rep.content.decode("UTF-8")
#     print(en_categorys_json)
#
# jwturl = f"https://0djxrjui.shdkw1o.com/ws?jwt_token={token}&ver=1.10.2"
# jwt_headers = {
#     "Upgrade": "websocket",
#     "Connection": "Upgrade",
#     "Sec-WebSocket-Key": "oa37+1fnzu5iWmlh4bH0pw==",
#     "Sec-WebSocket-Version": "13",
#     "Sec-WebSocket-Extensions": "permessage-deflate",
#     "knockknock": "synergy",
#     "Sec-WebSocket-Accept-Encoding": "brotli",
#     "Accept-Encoding": "br,gzip",
#     "Host": "0djxrjui.shdkw1o.com",
#     "User-Agent": "okhttp/4.8.0"
# }
#
# jwturl_rep = requests.get(jwturl, headers=jwt_headers)
# if jwturl_rep.status_code == requests.codes.ok:
#     jwturl_rep_json = jwturl_rep.content.decode("UTF-8")
#     print(jwturl_rep_json)
# else:
#     print(jwturl_rep.status_code)

def get_all_follow():
    # / OpenAPI / v1 / user / followees?uid = 99452869 & page = 1
    roomlist = []
    try:
        conf = config.getInstance()
        token = conf.get_XHL_token()
        Butter2 = conf.get_XHL_Butter2()
        baseurl = conf.get_XHL_baseurl()
        headers = build_header(token, Butter2)
        page = 1
        while True:
            allfollowurl = f"{baseurl}OpenAPI/v1/user/followees?uid=99452869&page={page}"
            allfollowurl_rep = requests.get(allfollowurl, timeout=(5, 10), headers=headers)

            if allfollowurl_rep.status_code == requests.codes.ok:
                # requests在安装brotli后,自动解压br,无需调用brotli.decompress
                # data = brotli.decompress(response.content)
                content = allfollowurl_rep.content.decode('UTF-8')
                datas = json.loads(content)["data"]
                rooms = datas["list"]
                page_cnt = datas["page_cnt"]
                for room in rooms:
                    temp = {
                        "id": room["id"],
                        "title": room["nickname"],
                        "lastlogtime": room["lastlogtime"]
                    }

                    roomlist.append(temp)
                if page_cnt > page:
                    page += 1
                else:
                    break
            else:
                logger.info(f'http re code: {allfollowurl_rep.status_code}')
                logger.info(f'http content: {allfollowurl_rep.content.decode("UTF-8")}')
                break
    except Exception as r:
        logger.info(f'get_all_follow 发生未知错误 {r}')
    return roomlist


def get_online_friends():
    conf = config.getInstance()
    token = conf.get_XHL_token()
    Butter2 = conf.get_XHL_Butter2()
    baseurl = conf.get_XHL_baseurl()

    headers = build_header(token, Butter2)

    try:
        friendsurl = f"{baseurl}OpenAPI/v1/anchor/onlineFriends?page=1&isPk=0"
        friendsurl_rep = requests.get(friendsurl, timeout=(5, 10), headers=headers)

        if friendsurl_rep.status_code == requests.codes.ok:
            # requests在安装brotli后,自动解压br,无需调用brotli.decompress
            # data = brotli.decompress(response.content)
            content = friendsurl_rep.content.decode('UTF-8')
            rooms = json.loads(content)["data"]
            roomlist = []
            for room in rooms:
                temp = {
                    "id": room["id"],
                    "title": room["nickname"]
                }
                roomlist.append(temp)
            return roomlist
        else:
            logger.info(f'http re code: {friendsurl_rep.status_code}')
            logger.info(f'http content: {friendsurl_rep.content.decode("UTF-8")}')
    except Exception as r:
        logger.info(f'get_hot_list 发生未知错误 {r}')
    return []


def get_hot_list():
    conf = config.getInstance()
    token = conf.get_XHL_token()
    Butter2 = conf.get_XHL_Butter2()
    baseurl = conf.get_XHL_baseurl()

    headers = build_header(token, Butter2)
    roomlist = []
    roomtitlecache = config.getInstance().get_roomtitlecache()
    try:
        page = 1
        size = 50
        while True:
            hoturl = f"{baseurl}OpenAPI/v1/anchor/hot?page={page}&size={size}&order=time&isPk=0"
            hoturl_rep = requests.get(hoturl, timeout=(5, 10), headers=headers)
            if hoturl_rep.status_code == requests.codes.ok:
                # requests在安装brotli后,自动解压br,无需调用brotli.decompress
                # data = brotli.decompress(response.content)
                content = hoturl_rep.content.decode('UTF-8')
                datas = json.loads(content)["data"]
                rooms = datas["list"]
                for room in rooms:
                    temp = {
                        "id": room["id"],
                        "title": room["nickname"]
                    }
                    roomtitlecache[room['id']] = room["nickname"]
                    roomlist.append(temp)
                if len(rooms) >= size:
                    page += 1
                else:
                    break
            else:
                logger.info(f'http re code: {hoturl_rep.status_code}')
                logger.info(f'http content: {hoturl_rep.content.decode("UTF-8")}')
                break
    except Exception as r:
        logger.info(f'get_hot_list 发生未知错误 {r}')
    config.getInstance().set_roomtitlecache(roomtitlecache)
    return roomlist


def get_room_url_by_roomid(roomid):
    try:
        conf = config.getInstance()
        token = conf.get_XHL_token()
        Butter2 = conf.get_XHL_Butter2()
        baseurl = conf.get_XHL_baseurl()

        headers = build_header(token, Butter2)

        roominfourl = f"{baseurl}OpenAPI/v1/private/getPrivateLimit?uid={roomid}"
        roominfourl_rep = requests.get(roominfourl, timeout=(5, 10), headers=headers)
        if roominfourl_rep.status_code == requests.codes.ok:
            content = roominfourl_rep.content.decode('UTF-8')
            destr = base64_crypt.getInstance().AES_decrypt(content)
            logger.debug(f"roomid {roomid} getPrivateLimit {destr}")
            datas = json.loads(destr)["data"]
            stream = datas["stream"]
            url = stream["pull_url"]
            # index = url.find("&sign=")
            # url = url[0:index]
            config.getInstance().set_room_url_cache(roomid, url)
            # info["video"] = url
            # info["is_cache"] = False
            logger.info(f'roomid {roomid} url: {url}')
            return url, False
        else:
            logger.info(f'http re code: {roominfourl_rep.status_code}')
            logger.info(f'http content: {roominfourl_rep.content.decode("UTF-8")}')
    except Exception as r:
        logger.info(f'get_room_info_by_roomid 发生未知错误 {r}')
        logger.info(f'find old url...')
        url = config.getInstance().get_last_room_url(roomid)
        if url is not None:
            logger.info(f'find old url: {url}')
            return url, True
            # info["video"] = url
            # info["is_cache"] = True
        else:
            logger.info(f'old url not found.')


def get_room_info_by_roomid(roomid):
    info = get_user_info(roomid)
    if info is None:
        return None
    elif info["playing"] == "n":
        return info

    url, is_cache = get_room_url_by_roomid(roomid)
    info["video"] = url
    info["is_cache"] = is_cache
    return info


def get_user_info(roomid):
    try:
        conf = config.getInstance()
        token = conf.get_XHL_token()
        Butter2 = conf.get_XHL_Butter2()
        baseurl = conf.get_XHL_baseurl()
        headers = build_header(token, Butter2)

        infourl = f"{baseurl}OpenAPI/v1/user/profile?uid={roomid}"
        roominfourl_rep = requests.get(infourl, timeout=(5, 10), headers=headers)

        if roominfourl_rep.status_code == requests.codes.ok:
            content = roominfourl_rep.content.decode('UTF-8')
            data = json.loads(content)["data"]
            logger.debug(f"roomid {roomid} info {data}")
            title = data["nickname"]
            starttime = data["starttime"]
            playing = data["broadcasting"]
            followersnum = data["followers_cnt"]
            timeformat = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(starttime)))
            return {
                "id": roomid,
                "title": title,
                "starttime": timeformat,
                "playing": playing,
                "followersnum": followersnum
            }
        else:
            logger.info(f'http re code: {roominfourl_rep.status_code}')
            logger.info(f'http content: {roominfourl_rep.content.decode("UTF-8")}')
    except Exception as r:
        logger.info(f'get_user_info 发生未知错误 {r}')
    return None


def add_follow(roomid):
    try:
        conf = config.getInstance()
        token = conf.get_XHL_token()
        Butter2 = conf.get_XHL_Butter2()
        baseurl = conf.get_XHL_baseurl()
        headers = build_header(token, Butter2)

        infourl = f"{baseurl}OpenAPI/v1/user/follow?uid={roomid}&roomid="
        roominfourl_rep = requests.get(infourl, timeout=(5, 10), headers=headers)

        if roominfourl_rep.status_code == requests.codes.ok:
            content = roominfourl_rep.content.decode('UTF-8')
            logger.info(f'add_follow: {content}')
        else:
            logger.info(f'http re code: {roominfourl_rep.status_code}')
            logger.info(f'http content: {roominfourl_rep.content.decode("UTF-8")}')
    except Exception as r:
        logger.info(f'add_follow 发生未知错误 {r}')


def del_follow(roomid):
    try:
        conf = config.getInstance()
        token = conf.get_XHL_token()
        Butter2 = conf.get_XHL_Butter2()
        baseurl = conf.get_XHL_baseurl()
        headers = build_header(token, Butter2)

        infourl = f"{baseurl}OpenAPI/v1/user/unfollow?uid={roomid}&roomid="
        roominfourl_rep = requests.get(infourl, timeout=(5, 10), headers=headers)

        if roominfourl_rep.status_code == requests.codes.ok:
            content = roominfourl_rep.content.decode('UTF-8')
            logger.info(f'del_follow: {content}')
        else:
            logger.info(f'http re code: {roominfourl_rep.status_code}')
            logger.info(f'http content: {roominfourl_rep.content.decode("UTF-8")}')
    except Exception as r:
        logger.info(f'del_follow 发生未知错误 {r}')


def build_header(token, Butter2):
    return {
        "Accept-Encoding": "br,gzip",
        "Authorization": f"Bearer {token}",
        "Host": "0djxrjui.shdkw1o.com",
        "Connection": "Keep-Alive",
        "User-Agent": "okhttp/4.8.0",
        "X-Live-Butter2": Butter2,
        "X-Accept-Puzzle": "cola,tiger,tiger2,panda",
        "knockknock": "synergy",
        "X-Live-Pretty": "spring"
    }
