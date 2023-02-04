import logging
import os
import platform
import time

from core import tools

instancts = {}
# timestr = time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
timestr = time.strftime("_%Y-%m-%d", time.localtime(time.time()))


def getInstance(loggername):
    if loggername in instancts.keys():
        return instancts[loggername].get_log()
    else:
        instanct = Logger(loggername)
        instancts[loggername] = instanct
        return instanct.get_log()


class Logger:
    def __init__(self, loggername):

        # 创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        logname = ""
        if platform.system() == 'Windows':
            logname = os.path.join(tools.getProcessPath(), f"logs/out{timestr}.log")
        elif platform.system() == 'Linux':
            logname = os.path.join("/var/log/xhlCRS", f"out{timestr}.log")

        if not os.path.exists(os.path.dirname(logname)):
            os.mkdir(os.path.dirname(logname))
        fh = logging.FileHandler(logname, encoding='utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        fh.setLevel(logging.INFO)

        # 创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s] --- %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(logging.Formatter('%(message)s'))

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger