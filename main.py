import re
import sys
import time

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from jpype._core import startJVM, shutdownJVM
from jpype._jvmfinder import getDefaultJVMPath

from core import config, logger, tools, base64_crypt
from view.mainWin import MainWin


if __name__ == '__main__':
    config.getInstance()
    mylogger = logger.getInstance(__name__)

    jarpath = tools.getFilePathByRelativePath("crypt.jar")
    startJVM(getDefaultJVMPath(), f"-Djava.class.path={jarpath}")

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    re = app.exec_()
    # a=""
    # print(base64_crypt.getInstance().AES_decrypt(a))
    shutdownJVM()

    sys.exit(re)
#
# if __name__ == '__main__':
#     print(time.localtime(time.time()))