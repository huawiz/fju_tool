import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from jinja2 import Environment, FileSystemLoader
import ui
import fju



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 使用 PyQt 生成 UI
        self.ui = ui.mainUI()
        self.ui.setupUi(self)

        # 連結按鈕事件
        self.ui.updateButton.clicked.connect(self.showLogin)
        self.ui.mapButton.clicked.connect(self.openMap)
        self.scheduleData = self.getScheduleData()
        self.loadSchedule()
        # 初始化時間
        self.initTimeWidget()

    def getScheduleData(self):
        self.scheduleData = fju.getjsonCourseData()
        if self.scheduleData is None or self.scheduleData == {}:
            self.showLogin()
        return self.scheduleData

    # 建立定時器
    def initTimeWidget(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateLabel)
        self.timer.start(1000)   # 每秒刷新一次
        self.updateLabel()

    # 更新介面文字標籤
    def updateLabel(self):
        # 獲取台灣時間
        currentTime = fju.getCurrentTime()
        # 更新時間標籤
        self.ui.timeLabel.setText("現在時間: " + currentTime.strftime("%Y-%m-%d %H:%M:%S"))

        # 獲得下節課訊息
        nextCourse = fju.getNextCourse(self.scheduleData)
        
        # 更新下節課標籤
        if nextCourse is not None:
            self.ui.currentClassLabel.setText(f"下一節課: 星期{nextCourse['星期']} | {nextCourse['科目名稱'].split('\n')[0]} | {nextCourse['教室']} | {nextCourse['節次']}")
        else:
            self.ui.currentClassLabel.setText("目前沒有課程")

    # 登入框
    def showLogin(self):
        loginDialog = ui.LoginDialog(self)
        if loginDialog.exec_() == QDialog.Accepted: 
            self.scheduleData = self.getScheduleData()
            self.loadSchedule()
            QMessageBox.information(self, "更新完成", "課表已更新。")
            


    # 載入課表
    def loadSchedule(self):
        # 渲染課表到畫面的WebView
        try:
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('course.html')
            htmlContent = template.render(courseName='課表', periodMapping=fju.periodMapping,
                                           scheduleData=fju.getScheduleData())
            htmlContent = fju.mergeSameRowHtml(htmlContent)
            self.ui.scheduleText.setHtml(htmlContent)
        except Exception as e:
            print(e)
            QMessageBox.information(self, "Error", f"無法載入課表: {e}")

    # 學校地圖
    def openMap(self):
        htmlContent = fju.renderMap()
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
