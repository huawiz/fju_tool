import sys
import json
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5.QtCore import QTimer
from ui.pyqtUI import Ui_ClassHelper  # 导入自动生成的 UI 类
from ui.login import LoginDialog  # 导入自定义的登录对话框类
from src import scraper, coursedata, map
from PyQt5.QtWebEngineWidgets import QWebEngineView
from jinja2 import Environment, FileSystemLoader
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 使用pyqt生成的UI
        self.ui = Ui_ClassHelper()
        self.ui.setupUi(self)

        # 連接點擊事件
        self.ui.updateButton.clicked.connect(self.show_login)
        #self.ui.loadButton.clicked.connect(self.load_schedule)
        self.ui.mapButton.clicked.connect(self.open_map)


        schedule_data = self.get_scheduleData()
        self.load_schedule()
        # 初始化時間
        self.init_time_widget()

    def get_scheduleData(self):
        file_path = os.path.join(os.getcwd(), "data/courseData.json")
        # 檢查文件是否存在
        if not os.path.exists(file_path):
            # 如果文件不存在，创建一个空的JSON文件
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf8") as f:
                json.dump([], f)

        # 打開文件並加载数据
        with open(file_path, "r", encoding="utf8") as f:
            try:
                schedule_data = json.load(f)
            except json.JSONDecodeError:
                schedule_data = None

        if not schedule_data:
            self.show_login()
        
        return schedule_data
    
    def init_time_widget(self):
        schedule_data = self.get_scheduleData()

        # 建立定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_time(schedule_data))
        self.timer.start(1000)  # 每秒刷新一次

        # 更新时间显示
        self.update_time(schedule_data)

    def update_time(self, schedule_data):
        # 获取当前时间
        current_time = datetime.datetime.now()
        # 更新时间标签
        self.ui.timeLabel.setText("現在時間: " + current_time.strftime("%Y-%m-%d %H:%M:%S")
)

        # 获取下一节课的信息
        nextCourse = coursedata.getNextCourse(schedule_data, current_time)

        # 更新当前课程标签
        if nextCourse:
            self.ui.currentClassLabel.setText(
                f"下一節課: 星期{nextCourse['星期']} | {nextCourse['科目名稱'].split('\n')[0]} | {nextCourse['教室']} | {nextCourse['節次']}")
        else:
            self.ui.currentClassLabel.setText("目前沒有課程")

    def show_login(self):
        # 创建登录对话框实例
        login_dialog = LoginDialog(self)
        if login_dialog.exec_() == QDialog.Accepted:
            # 從對話框中獲取帳號和密碼
            username = login_dialog.username_input.text()
            password = login_dialog.password_input.text()
            # 使用帳號和密碼進行後續操作
            self.update_schedule(username, password)
        else:
            pass

    def update_schedule(self, username, password):
        scraper.updateCourse(username, password)
        QMessageBox.information(self, "更新完成", "課表已更新。")
        self.load_schedule()

    def load_schedule(self):
        try:
            schedule_data = self.get_scheduleData()

            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('course.html')

            html_content = template.render(courseName='課表', periodMapping=coursedata.periodMapping,
                                           scheduleData=coursedata.getScheduleData(schedule_data))
            html_content = coursedata.mergeSameRowHtml(html_content)

            self.ui.scheduleText.setHtml(html_content)
        except Exception as e:
            print(e)
            QMessageBox.information(self, "Error", f"Could not load schedule: {e}")

    def open_map(self):
        html_content = map.renderMap()
        self.map_window = QWebEngineView()
        self.map_window.setWindowTitle("學校地圖")
        self.map_window.setGeometry(200, 200, 1024, 1024)
        self.map_window.setHtml(html_content)
        self.map_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
