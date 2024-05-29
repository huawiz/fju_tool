# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\pyqtUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClassHelper(object):

    def setupUi(self, ClassHelper):

        ClassHelper.setObjectName("ClassHelper")
        ClassHelper.setGeometry(100, 100, 1024, 916)
        ClassHelper.setFixedSize(ClassHelper.size())
        #ClassHelper.resize(1072, 748)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ClassHelper.sizePolicy().hasHeightForWidth())
        ClassHelper.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(ClassHelper)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 511, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.updateButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.updateButton.setObjectName("updateButton")
        self.horizontalLayout.addWidget(self.updateButton)
        self.loadButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.loadButton.setObjectName("loadButton")
        self.horizontalLayout.addWidget(self.loadButton)
        self.mapButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.mapButton.setObjectName("mapButton")
        self.horizontalLayout.addWidget(self.mapButton)
        self.scheduleText = QtWidgets.QTextBrowser(self.centralwidget)
        self.scheduleText.setGeometry(QtCore.QRect(0, 70, 1024, 900))
        self.scheduleText.setObjectName("scheduleText")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(529, 0, 541, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.timeLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.timeLabel.setObjectName("timeLabel")
        self.verticalLayout.addWidget(self.timeLabel)
        self.currentClassLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.currentClassLabel.setObjectName("currentClassLabel")
        self.verticalLayout.addWidget(self.currentClassLabel)
        ClassHelper.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ClassHelper)
        #self.statusbar.setObjectName("statusbar")
        #ClassHelper.setStatusBar(self.statusbar)

        self.retranslateUi(ClassHelper)
        QtCore.QMetaObject.connectSlotsByName(ClassHelper)

    def retranslateUi(self, ClassHelper):
        _translate = QtCore.QCoreApplication.translate
        ClassHelper.setWindowTitle(_translate("ClassHelper", "課表小助手"))
        self.updateButton.setText(_translate("ClassHelper", "更新課表"))
        self.loadButton.setText(_translate("ClassHelper", "載入課表"))
        self.mapButton.setText(_translate("ClassHelper", "開啟學校地圖"))
        self.timeLabel.setText(_translate("ClassHelper", "現在時間:"))
        self.currentClassLabel.setText(_translate("ClassHelper", "下一節課:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ClassHelper = QtWidgets.QMainWindow()
    ui = Ui_ClassHelper()
    ui.setupUi(ClassHelper)
    ClassHelper.show()
    sys.exit(app.exec_())
