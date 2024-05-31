import sys
import json
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from jinja2 import Environment, FileSystemLoader
import os
from ui.mainUI import UIClassHelper  # 导入自动生成的 UI 类
from ui.loginUI import LoginDialog  # 导入自定义的登录对话框类
from src import scraper, coursedata, map


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 使用 PyQt 生成的 UI
        self.ui = UIClassHelper()
        self.ui.setupUi(self)

        # 连接点击事件
        self.ui.updateButton.clicked.connect(self.showLogin)
        self.ui.mapButton.clicked.connect(self.openMap)

        self.scheduleData = self.getScheduleData()
        self.loadSchedule()
        
        # 初始化时间
        self.initTimeWidget()

    def getScheduleData(self):
        filePath = os.path.join(os.getcwd(), "data/courseData.json")
        # 检查文件是否存在
        if not os.path.exists(filePath):
            # 如果文件不存在，创建一个空的 JSON 文件
            os.makedirs(os.path.dirname(filePath), exist_ok=True)
            with open(filePath, "w", encoding="utf8") as f:
                json.dump([], f)

        # 打开文件并加载数据
        try:
            with open(filePath, "r", encoding="utf8") as f:
                scheduleData = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            scheduleData = []

        return scheduleData
    
    def initTimeWidget(self):
        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)  # 每秒刷新一次

        # 更新时间显示
        self.updateTime()

    def updateTime(self):
        # 获取当前时间
        currentTime = datetime.datetime.now()
        # 更新时间标签
        self.ui.timeLabel.setText("現在時間: " + currentTime.strftime("%Y-%m-%d %H:%M:%S"))

        # 获取下一节课的信息
        nextCourse = coursedata.getNextCourse(self.scheduleData, currentTime)

        # 更新当前课程标签
        if nextCourse:
            self.ui.currentClassLabel.setText(
                f"下一節課: 星期{nextCourse['星期']} | {nextCourse['科目名稱'].split('\n')[0]} | {nextCourse['教室']} | {nextCourse['節次']}")
        else:
            self.ui.currentClassLabel.setText("目前沒有課程")

    def showLogin(self):
        # 创建登录对话框实例
        loginDialog = LoginDialog(self)
        if loginDialog.exec_() == QDialog.Accepted: 
            QMessageBox.information(self, "更新完成", "課表已更新。")
            self.scheduleData = self.getScheduleData()
            self.loadSchedule()



    def loadSchedule(self):
        try:
            if not self.scheduleData:
                self.showLogin()
                return

            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('course.html')

            htmlContent = template.render(courseName='課表', periodMapping=coursedata.periodMapping,
                                           scheduleData=coursedata.getScheduleData(self.scheduleData))
            htmlContent = coursedata.mergeSameRowHtml(htmlContent)

            self.ui.scheduleText.setHtml(htmlContent)
        except Exception as e:
            print(e)
            QMessageBox.information(self, "Error", f"Could not load schedule: {e}")

    def openMap(self):
        htmlContent = map.renderMap()
        self.mapWindow = QWebEngineView()
        self.mapWindow.setWindowTitle("學校地圖")
        self.mapWindow.setGeometry(200, 200, 1024, 900)
        self.mapWindow.setHtml(htmlContent)
        self.mapWindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
