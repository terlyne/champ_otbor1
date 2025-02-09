from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QErrorMessage,
)
from PyQt6.QtCore import pyqtSignal

from database.db import read_user

class LoginDialog(QDialog):

    authorized = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setMinimumSize(200, 100)

        self.setWindowTitle("Авторизация")

        self.username_label = QLabel("Имя пользователя:")
        self.password_label = QLabel("Пароль:")

        self.username_lineedit = QLineEdit()
        self.password_lineedit = QLineEdit()


        self.user = None


        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)

        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(self.username_label)
        self.main_layout.addWidget(self.username_lineedit)
        self.main_layout.addWidget(self.password_label)
        self.main_layout.addWidget(self.password_lineedit)
        self.main_layout.addWidget(self.login_button)

        self.setLayout(self.main_layout)

    def login(self):
        self.user = read_user(self.username_lineedit.text(), self.password_lineedit.text())
        if self.user:
            self.authorized.emit()
            self.accept()
        else:
            error = QErrorMessage(self)
            error.showMessage("Произошла ошибка! Попробуйте еще раз")