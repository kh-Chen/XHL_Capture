import argparse
import sys

from core import logger, tools, config, base64_crypt
from jpype._core import startJVM, shutdownJVM
from jpype._jvmfinder import getDefaultJVMPath

from service import wqService, xhlService

if __name__ == '__main__':
    mylogger = logger.getInstance(__name__)
    conf = config.getInstance()

    parser = argparse.ArgumentParser(description="Demo of argparse")
    parser.add_argument('-d', '--decrypt', dest='decrypt', default="",
                        help="decrypt str")
    parser.add_argument('-m', '--mode', dest='mode', default="",
                        help="show recording rooms")
    parser.add_argument('-l', '--list-recording', dest='list_recording', action="store_true",
                        help="show recording rooms")
    parser.add_argument('-a', '--all-rooms', dest='all_rooms', action="store_true",
                        help="show all rooms")
    parser.add_argument('-s', '--scan-rooms', dest='scan_rooms', action="store_true",
                        help="scan room and record watching room")
    parser.add_argument('-r', '--record', dest='record', default='',
                        help="start recording room by roomid")
    parser.add_argument('-i', '--room-info', dest='roominfo', default='',
                        help="show room info")
    parser.add_argument('-k', '--kill-recording', dest='kill_recording', default='',
                        help="stop recording room by roomid")
    parser.add_argument('-f', '--follow', dest='follow', default='',
                        help="change follow, input roomid")
    parser.add_argument('-fl', '--follow-list', dest='showfollowlist', action="store_true",
                        help="change follow, input roomid")
    parser.add_argument('-xhlfl', '--xhl-follow-list', dest='showxhlfollowlist', action="store_true",
                        help="change follow, input roomid")
    parser.add_argument('-url', dest='baseurl', default='',
                        help="start recording room use input url")

    mylogger.debug("start...")
    args = parser.parse_args()

    if args.scan_rooms or args.all_rooms or args.record != '' or args.roominfo != '' or args.decrypt != '':
        jarpath = tools.getFilePathByRelativePath("crypt.jar")
        startJVM(getDefaultJVMPath(), f"-Djava.class.path={jarpath}")

    mode = conf.get_mode() if args.mode == "" else args.mode

    if mode == "1":
        ac = wqService.Actions()
    elif mode == "2":
        ac = xhlService.Actions()
    else:
        mylogger.info(f"mode {mode} error.")
        sys.exit()

    if args.decrypt != '':
        print(base64_crypt.getInstance().AES_decrypt(args.decrypt))

    if args.follow != '':
        ac.addDelFollow(args.follow)

    if args.showfollowlist:
        ac.printFollowRooms()

    if args.showxhlfollowlist:
        ac.showAllXHLFollowers()

    if args.scan_rooms:
        ac.scanroom()

    if args.all_rooms:
        ac.showAllRooms()

    if args.list_recording:
        ac.showRecordingRooms()

    if args.kill_recording != '':
        ac.killroom(args.kill_recording)

    if args.record != '':
        ac.start_record(args.record, url=args.baseurl)

    if args.roominfo != '':
        ac.getRoomInfo(args.roominfo)

    if args.scan_rooms or args.all_rooms or args.record != '' or args.roominfo != '' or args.decrypt != '':
        shutdownJVM()
        mylogger.debug("JVM shutdown")

    sys.exit()
