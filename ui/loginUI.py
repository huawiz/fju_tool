from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from src import scraper

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setFixedSize(300, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def initUI(self):
        self.setWindowTitle("取得課表資料")
        layout = QVBoxLayout()
        self.usernameLabel = QLabel("FJU學生帳號:")
        self.usernameInput = QLineEdit(self)
        self.passwordLabel = QLabel("FJU學生密碼:")
        self.passwordInput = QLineEdit(self)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.loginButton = QPushButton("登入", self)
        self.loginButton.clicked.connect(self.getCourseData)

        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameInput)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordInput)
        layout.addWidget(self.loginButton)
        self.setLayout(layout)

    def getCourseData(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        login = scraper.CourseData(username, password)
        data = login.getCourseData()
        
        try:
            if username and password and data:
                login.saveData(data)
                self.accept()
            else:
                raise ValueError("無效的用戶名或密碼，或無法獲取課程數據。")
        except Exception as e:
            QMessageBox.warning(self, "登入失敗", str(e))
