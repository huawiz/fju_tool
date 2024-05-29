from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,QMessageBox
from PyQt5.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setFixedSize(300, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def initUI(self):
        self.setWindowTitle("取得課表資料")
        layout = QVBoxLayout()

        self.username_label = QLabel("FJU學生帳號:")
        self.username_input = QLineEdit(self)

        self.password_label = QLabel("FJU學生密碼:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("登入", self)
        self.login_button.clicked.connect(self.getCourseData)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def getCourseData(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # 这里可以添加登录验证逻辑
        if username != "" and password != "":
            self.accept()

