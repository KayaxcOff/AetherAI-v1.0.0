from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel,
    QLineEdit, QPushButton, QWidget,
    QVBoxLayout, QProgressBar, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import psutil
import sys
import json
import os

class WatchCPUUsage(QWidget):
    def __init__(self):
        super(WatchCPUUsage, self).__init__()
        self.setWindowTitle("CPU Usage")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowIcon(QIcon("AetPictures/logo.png"))
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.cpu_label = QLabel("CPU Usage (%)", self)
        layout.addWidget(self.cpu_label)

        self.cpu_progress = QProgressBar(self)
        self.cpu_progress.setRange(0, 100)
        layout.addWidget(self.cpu_progress)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_cpu_usage)
        self.timer.start(1000)

    def update_cpu_usage(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        self.cpu_progress.setValue(cpu_usage)
        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")

class WatchRAMUsage(QWidget):
    def __init__(self):
        super(WatchRAMUsage, self).__init__()
        self.setWindowTitle("RAM Usage")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowIcon(QIcon("AetPictures/logo.png"))
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.ram_label = QLabel("RAM Usage (%)", self)
        layout.addWidget(self.ram_label)

        self.ram_progress = QProgressBar(self)
        self.ram_progress.setRange(0, 100)
        layout.addWidget(self.ram_progress)

        self.setLayout(layout)

        self.total_memory = QLabel("Total RAM Usage", self)
        layout.addWidget(self.total_memory)

        self.available_memory = QLabel("Available RAM Usage", self)
        layout.addWidget(self.available_memory)

        self.used_memory = QLabel("Used RAM Usage", self)
        layout.addWidget(self.used_memory)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ram_usage)
        self.timer.start(1000)

    def update_ram_usage(self):
        ram_usage = psutil.virtual_memory().percent
        self.ram_progress.setValue(ram_usage)
        self.ram_label.setText(f"RAM Usage: {ram_usage}%")

        total_memory = psutil.virtual_memory().total / (1024 ** 3)
        available_memory = psutil.virtual_memory().available / (1024 ** 3)
        used_memory = psutil.virtual_memory().used / (1024 ** 3)

        self.total_memory.setText(f"Total RAM Usage: {total_memory}%")
        self.available_memory.setText(f"Available RAM Usage: {available_memory}%")
        self.used_memory.setText(f"Used RAM Usage: {used_memory}%")

class AetAIApp(QWidget):
    def __init__(self):
        super(AetAIApp, self).__init__()
        self.setWindowTitle("AetherAI Application")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("AetPictures/logo.png"))
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.welcome_label = QLabel("Welcome to AetherAI", self)
        layout.addWidget(self.welcome_label)

        button_layout = QHBoxLayout()

        self.cpu_button = QPushButton("See CPU Usage", self)
        self.cpu_button.setMaximumSize(150, 50)
        self.cpu_button.clicked.connect(self.show_cpu_usage)
        button_layout.addWidget(self.cpu_button)

        self.ram_button = QPushButton("See RAM Usage", self)
        self.ram_button.setMaximumSize(150, 50)
        self.ram_button.clicked.connect(self.show_ram_usage)
        button_layout.addWidget(self.ram_button)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setMaximumSize(150, 50)
        self.exit_button.clicked.connect(self.close_app)
        button_layout.addWidget(self.exit_button)

        self.setLayout(layout)

        self.cpu_window = None
        self.ram_window = None

    def show_cpu_usage(self):
        self.cpu_window = WatchCPUUsage()
        self.cpu_window.show()

    def show_ram_usage(self):
        self.ram_window = WatchRAMUsage()
        self.ram_window.show()

    def close_app(self):
        pass

class SignInWindow(QWidget):
    def __init__(self, parent=None):
        super(SignInWindow, self).__init__()
        self.parent = parent

        self.setWindowTitle("Sign Up")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon("AetPictures/logo.png"))
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("Sign Up", self)
        layout.addWidget(title_label)

        name_layout = QHBoxLayout()
        name_label = QLabel("Name:", self)
        name_label.setMinimumWidth(100)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        lastname_layout = QHBoxLayout()
        lastname_label = QLabel("Last Name:", self)
        lastname_label.setMinimumWidth(100)
        self.lastname_input = QLineEdit(self)
        self.lastname_input.setPlaceholderText("Enter your last name")
        lastname_layout.addWidget(lastname_label)
        lastname_layout.addWidget(self.lastname_input)
        layout.addLayout(lastname_layout)

        email_layout = QHBoxLayout()
        email_label = QLabel("E-mail:", self)
        email_label.setMinimumWidth(100)
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter your email")
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)

        self.signin_button = QPushButton("Sign in", self)
        self.signin_button.setMaximumSize(150, 50)
        self.signin_button.clicked.connect(self.handle_signin)
        layout.addWidget(self.signin_button)

        self.setLayout(layout)

    def handle_signin(self):
        email = self.email_input.text()
        if not email:
            QMessageBox.warning(self, "Warning", "Please enter your email")
            return

        found = False
        if os.path.exists('users.json'):
            with open('users.json', 'r') as userFile:
                users = json.load(userFile)
                for user in users:
                    if user.get("email") == email:
                        found = True
                        break
        if found:
            QMessageBox.information(self, "Success", "Sign in successful!")
            if self.parent:
                self.parent.appMain()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Email isn't exist. Please sign up first.")

class SignUpWindow(QWidget):
    def __init__(self, parent=None):
        super(SignUpWindow, self).__init__()
        self.parent = parent

        self.setWindowTitle("Sign In")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon("AetPictures/logo.png"))
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("Sign In", self)
        layout.addWidget(title_label)

        name_layout = QHBoxLayout()
        name_label = QLabel("Name:", self)
        name_label.setMinimumWidth(100)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        lastname_layout = QHBoxLayout()
        lastname_label = QLabel("Last Name:", self)
        lastname_label.setMinimumWidth(100)
        self.lastname_input = QLineEdit(self)
        self.lastname_input.setPlaceholderText("Enter your last name")
        lastname_layout.addWidget(lastname_label)
        lastname_layout.addWidget(self.lastname_input)
        layout.addLayout(lastname_layout)

        email_layout = QHBoxLayout()
        email_label = QLabel("E-mail:", self)
        email_label.setMinimumWidth(100)
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter your email")
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.setMaximumSize(150, 50)
        self.signup_button.clicked.connect(self.handle_signup)
        layout.addWidget(self.signup_button)

        self.setLayout(layout)

    def handle_signup(self):
        name = self.name_input.text()
        lastname = self.lastname_input.text()
        email = self.email_input.text()

        if not all([name, lastname, email]):
            QMessageBox.warning(self, "Warning", "Please fill in all fields")
            return

        if "@" not in email or "." not in email:
            QMessageBox.warning(self, "Warning", "Please enter a valid email")
            return

        bulundu = False
        if os.path.exists('users.json'):
            with open('users.json', 'r') as userFile:
                users = json.load(userFile)
                for user in users:
                    if user.get("email") == email:
                        bulundu = True
                        break
        if bulundu:
            QMessageBox.warning(self, "Error", "Email already exists. Please sign in.")
            return

        if not os.path.exists('users.json'):
            with open('users.json', 'w') as usersFile:
                usersFile.write(f"{name}, {lastname}, {email}")
                QMessageBox.information(None, "Success", "Sign in successful!")
                self.close()

class AetherAIApp(QMainWindow):
    def __init__(self):
        super(AetAIApp, self).__init__()
        self.setWindowTitle("AetherAI Application")
        self.setGeometry(100, 100, 800, 600)
        self.setToolTip("AetherAI Application")
        self.setWindowIcon(QIcon("AetPictures/logo.png"))
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        title_label = QLabel("I'd like to welcome you to my AetherAI App", self.central_widget)
        layout.addWidget(title_label)

        desc_label = QLabel("This is a simple application to monitor CPU and RAM usage.", self.central_widget)
        layout.addWidget(desc_label)

        button_layout = QHBoxLayout()

        self.signin_button = QPushButton("Sign in", self.central_widget)
        self.signin_button.setMinimumSize(150, 50)
        self.signin_button.setIcon(QIcon("AetPictures/signin.png"))
        self.signin_button.clicked.connect(self.signIn)
        button_layout.addWidget(self.signin_button)

        self.signup_button = QPushButton("Sign Up", self.central_widget)
        self.signup_button.setMinimumSize(150, 50)
        self.signup_button.setIcon(QIcon("AetPictures/signup.png"))
        self.signup_button.clicked.connect(self.signUp)
        button_layout.addWidget(self.signup_button)

    def signIn(self):
        self.signInWindow = SignUpWindow()
        self.signInWindow.show()

    def signUp(self):
        self.signUpWindow = SignInWindow()
        self.signUpWindow.show()

    def appMain(self):
        self.main_app = AetAIApp()
        self.main_app.show()
        self.hide()

def addUser():
    name = "Muhammet"
    lastname = "Kaya"
    email = "muham123cak@gmail.com"

    user_infermation = {
        "name": name,
        "lastname": lastname,
        "email": email
    }

    if not os.path.exists('users.json'):
        with open('users.json', 'w') as userFile:
            json.dump(user_infermation, userFile, indent=4)
        return

    with open('users.json', 'r+') as userFile:
        users = json.load(userFile)
        users.append(user_infermation)
        userFile.seek(0)
        json.dump(users, userFile, indent=4)

def start_app():
    app = QApplication(sys.argv)
    app.setApplicationName("AetherAI")
    addUser()
    main_window = AetherAIApp()
    main_window.show()
    sys.exit(app.exec_())

start_app()
