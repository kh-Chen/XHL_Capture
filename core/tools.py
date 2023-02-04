import os
import platform
import subprocess
import sys
from time import sleep

import psutil

from core import logger


def get_pid(pname):
    pids = []
    for proc in psutil.process_iter():
        if proc.name() == pname:
            pids.append(proc.pid)
            continue
    return pids


def runCmdRePid(cmd, processname):
    mylogger = logger.getInstance(__name__)
    pids = get_pid(processname)
    subprocess.Popen(cmd, stdin=subprocess.PIPE, bufsize=0, shell=True)

    while True:
        ppids = get_pid(processname)
        for tmppid in ppids:
            if tmppid not in pids:
                return tmppid
        sleep(0.5)


def getFilePathByRelativePath(relativePath):
    repath = os.path.join(getProcessPath(), relativePath)
    if platform.system() == 'Windows':
        return repath
    elif platform.system() == 'Linux':
        if os.path.exists(repath):
            return repath
        else:
            return os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), relativePath)


def getProcessPath():
    if platform.system() == 'Windows':
        return os.path.dirname(os.path.realpath(sys.argv[0]))
    elif platform.system() == 'Linux':
        p = os.readlink(f'/proc/{os.getpid()}/exe')
        return os.path.split(p)[0]
