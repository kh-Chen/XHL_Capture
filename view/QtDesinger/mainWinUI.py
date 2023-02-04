# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWinUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1050, 410)
        self.previewBtn = QtWidgets.QPushButton(Form)
        self.previewBtn.setGeometry(QtCore.QRect(80, 10, 60, 20))
        self.previewBtn.setObjectName("previewBtn")
        self.recordBtn = QtWidgets.QPushButton(Form)
        self.recordBtn.setGeometry(QtCore.QRect(220, 10, 60, 20))
        self.recordBtn.setObjectName("recordBtn")
        self.refreshBtn = QtWidgets.QPushButton(Form)
        self.refreshBtn.setGeometry(QtCore.QRect(10, 10, 60, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshBtn.sizePolicy().hasHeightForWidth())
        self.refreshBtn.setSizePolicy(sizePolicy)
        self.refreshBtn.setObjectName("refreshBtn")
        self.autoRefreshBox = QtWidgets.QCheckBox(Form)
        self.autoRefreshBox.setGeometry(QtCore.QRect(750, 10, 65, 20))
        self.autoRefreshBox.setObjectName("autoRefreshBox")
        self.watchRoomBox = QtWidgets.QCheckBox(Form)
        self.watchRoomBox.setGeometry(QtCore.QRect(820, 10, 65, 20))
        self.watchRoomBox.setObjectName("watchRoomBox")
        self.playBtn = QtWidgets.QPushButton(Form)
        self.playBtn.setGeometry(QtCore.QRect(150, 10, 60, 20))
        self.playBtn.setObjectName("playBtn")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 40, 1031, 351))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.handleBox = QtWidgets.QComboBox(Form)
        self.handleBox.setGeometry(QtCore.QRect(890, 10, 70, 20))
        self.handleBox.setObjectName("handleBox")
        self.editfollowBtn = QtWidgets.QPushButton(Form)
        self.editfollowBtn.setGeometry(QtCore.QRect(430, 10, 60, 20))
        self.editfollowBtn.setObjectName("editfollowBtn")
        self.addfollowBtn = QtWidgets.QPushButton(Form)
        self.addfollowBtn.setGeometry(QtCore.QRect(290, 10, 60, 20))
        self.addfollowBtn.setObjectName("addfollowBtn")
        self.tipLabel = QtWidgets.QLabel(Form)
        self.tipLabel.setGeometry(QtCore.QRect(10, 392, 731, 16))
        self.tipLabel.setText("")
        self.tipLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tipLabel.setObjectName("tipLabel")
        self.sendStreamBtn = QtWidgets.QPushButton(Form)
        self.sendStreamBtn.setGeometry(QtCore.QRect(360, 10, 60, 20))
        self.sendStreamBtn.setObjectName("sendStreamBtn")
        self.sourceBox = QtWidgets.QComboBox(Form)
        self.sourceBox.setGeometry(QtCore.QRect(970, 10, 70, 20))
        self.sourceBox.setObjectName("sourceBox")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.previewBtn.setText(_translate("Form", "预览"))
        self.recordBtn.setText(_translate("Form", "录制"))
        self.refreshBtn.setText(_translate("Form", "刷新"))
        self.autoRefreshBox.setText(_translate("Form", "自动刷新"))
        self.watchRoomBox.setText(_translate("Form", "自动处理"))
        self.playBtn.setText(_translate("Form", "播放"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "房号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "标题"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "状态"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "链接"))
        self.editfollowBtn.setText(_translate("Form", "关注列表"))
        self.addfollowBtn.setText(_translate("Form", "关注"))
        self.sendStreamBtn.setText(_translate("Form", "转推流"))
