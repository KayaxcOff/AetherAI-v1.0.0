from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel,
    QLineEdit, QPushButton, QWidget,
    QVBoxLayout, QProgressBar, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QIcon, QFontDatabase, QFont
from PyQt5.QtCore import QTimer, Qt
import psutil
import sys
import json
import os
import joblib
import numpy as np

class AetherAI():
    def __init__(self):
        self.cpu = psutil.cpu_percent(interval=None)
        self.memory = psutil.virtual_memory().percent
        try:
            self.aet_model = joblib.load("../AetherModel/Model/aether_ai.pkl")
        except FileNotFoundError:
            print("Warning: Model file not found. Creating dummy model.")
            self.aet_model = None

    def predict(self, cpu_data, cpu_load, memory_data, memory_load):
        if self.aet_model is not None:
            self.data = np.array([[cpu_data, cpu_load, memory_data, memory_load]])
            self.prediction = self.aet_model.predict(self.data)
        else:
            self.prediction = [[cpu_data + 1, memory_data + 1]]

    def systemUsage(self):
        self.cpu_pre = self.prediction[0][0] - 2
        self.ram_pre = self.prediction[0][1] + 2
        return self.cpu_pre, self.ram_pre


class WatchCPUUsage(QWidget):
    def __init__(self):
        super(WatchCPUUsage, self).__init__()
        self.setWindowTitle("CPU Usage")
        self.setGeometry(100, 100, 300, 200)
        try:
            self.setWindowIcon(QIcon("AetPictures/logo.png"))
        except:
            pass
        self.aether_ai = AetherAI()
        self.initUI()
        self.cpu_warning_shown = False #

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
        cpu_usage = psutil.cpu_percent(interval=None)
        # ram_usage = psutil.virtual_memory().percent
        self.cpu_progress.setValue(int(cpu_usage))
        self.cpu_label.setText(f"CPU Usage: {cpu_usage}%")

        if 0 <= cpu_usage <= 30:
            cpu_load = 0
        elif 31 <= cpu_usage <= 70:
            cpu_load = 1
        elif 71 <= cpu_usage <= 100:
            cpu_load = 2
        else:
            QMessageBox.warning(self, "Warning", "Model can't work")

        self.aether_ai.predict(cpu_usage, cpu_load, 0, 0)
        self.cpu_warning = self.aether_ai.systemUsage()[0]
        if self.cpu_warning > 4 and not self.cpu_warning_shown:
            QMessageBox.warning(self, "Warning", "CPU usage is high! Consider closing some applications.")
            self.cpu_warning_shown = True

class WatchRAMUsage(QWidget):
    def __init__(self):
        super(WatchRAMUsage, self).__init__()
        self.setWindowTitle("RAM Usage")
        self.setGeometry(100, 100, 300, 200)
        try:
            self.setWindowIcon(QIcon("AetPictures/logo.png"))
        except:
            pass
        self.aether_ai = AetherAI()
        self.initUI()
        self.memory_warning_shown = False #

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
        #cpu_usage = psutil.cpu_percent(interval=None)
        self.ram_progress.setValue(int(ram_usage))
        self.ram_label.setText(f"RAM Usage: {ram_usage}%")

        total_memory = psutil.virtual_memory().total / (1024 ** 3)
        available_memory = psutil.virtual_memory().available / (1024 ** 3)
        used_memory = psutil.virtual_memory().used / (1024 ** 3)

        self.total_memory.setText(f"Total RAM Usage: {total_memory:.2f} GB")
        self.available_memory.setText(f"Available RAM Usage: {available_memory:.2f} GB")
        self.used_memory.setText(f"Used RAM Usage: {used_memory:.2f} GB")

        if 0 <= ram_usage <= 50:
            ram_load = 3
        elif 51 <= ram_usage <= 80:
            ram_load = 4
        elif 81 <= ram_usage <= 100:
            ram_load = 5
        else:
            QMessageBox.warning(self, "Warning", "Model can't work")

        self.aether_ai.predict(0, 0, ram_usage, ram_load)
        self.memory_warning = self.aether_ai.systemUsage()[1]
        if self.memory_warning > 11 and not self.memory_warning_shown:
            QMessageBox.warning(self, "Warning", "RAM usage is high! Consider closing some applications.")
            self.memory_warning_shown = True #

class AetAIApp(QWidget):
    def __init__(self):
        super(AetAIApp, self).__init__()
        self.setWindowTitle("AetherAI Application")
        self.setGeometry(100, 100, 800, 600)
        try:
            self.setWindowIcon(QIcon("AetPictures/logo.png"))
        except:
            pass
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

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.cpu_window = None
        self.ram_window = None

    def show_cpu_usage(self):
        if self.cpu_window is not None:
            self.cpu_window.close()
        self.cpu_window = WatchCPUUsage()
        self.cpu_window.show()

    def show_ram_usage(self):
        if self.ram_window is not None:
            self.ram_window.close()
        self.ram_window = WatchRAMUsage()
        self.ram_window.show()

    def close_app(self):
        QApplication.quit()


class SignUpWindow(QWidget):
    def __init__(self, parent=None):
        super(SignUpWindow, self).__init__()
        self.parent = parent

        self.setWindowTitle("Sign Up")
        self.setGeometry(100, 100, 400, 300)
        try:
            self.setWindowIcon(QIcon("AetPictures/logo.png"))
        except:
            pass
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

        self.signup_button = QPushButton("Sign up", self)
        self.signup_button.setMaximumSize(150, 50)
        self.signup_button.clicked.connect(self.handle_signup)
        layout.addWidget(self.signup_button)

        self.setLayout(layout)

    def handle_signup(self):
        name = self.name_input.text().strip()
        lastname = self.lastname_input.text().strip()
        email = self.email_input.text().strip()

        if not all([name, lastname, email]):
            QMessageBox.warning(self, "Warning", "Please fill in all fields")
            return

        if "@" not in email or "." not in email:
            QMessageBox.warning(self, "Warning", "Please enter a valid email address")
            return

        filename = 'users.json'
        user_information = {
            "name": name,
            "lastname": lastname,
            "email": email
        }

        try:
            if not os.path.exists(filename):
                with open(filename, 'w') as userFile:
                    json.dump([user_information], userFile, indent=4)
                QMessageBox.information(self, "Success", "Sign up successful!")
                self.close()
                return

            with open(filename, 'r') as userFile:
                try:
                    users = json.load(userFile)
                    if not isinstance(users, list):
                        users = []
                except json.JSONDecodeError:
                    users = []

            for user in users:
                if isinstance(user, dict) and user.get("email") == email:
                    QMessageBox.warning(self, "Error", "This email is already registered!")
                    return

            users.append(user_information)

            with open(filename, 'w') as userFile:
                json.dump(users, userFile, indent=4)

            QMessageBox.information(self, "Success", "Sign up successful!")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


class SignInWindow(QWidget):
    def __init__(self, parent=None):
        super(SignInWindow, self).__init__()
        self.parent = parent

        self.setWindowTitle("Sign In")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint) #
        try:
            self.setWindowIcon(QIcon("AetPictures/logo.png"))
        except:
            pass
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

        self.signin_button = QPushButton("Sign In", self)
        self.signin_button.setMaximumSize(150, 50)
        self.signin_button.clicked.connect(self.handle_signin)
        layout.addWidget(self.signin_button)

        self.setLayout(layout)

    def handle_signin(self):
        name = self.name_input.text().strip()
        lastname = self.lastname_input.text().strip()
        email = self.email_input.text().strip()

        if not all([name, lastname, email]):
            QMessageBox.warning(self, "Warning", "Please fill in all fields")
            return

        if "@" not in email or "." not in email:
            QMessageBox.warning(self, "Warning", "Please enter a valid email")
            return

        filename = 'users.json'
        found = False

        try:
            if os.path.exists(filename):
                with open(filename, 'r') as userFile:
                    try:
                        users = json.load(userFile)
                        if not isinstance(users, list):
                            users = []
                    except json.JSONDecodeError:
                        users = []

                    for user in users:
                        if isinstance(user, dict):
                            user_email = user.get("email", "")
                            user_name = user.get("name", "")
                            user_lastname = user.get("lastname", "")

                            if (user_email == email and
                                    user_name == name and
                                    user_lastname == lastname):
                                found = True
                                break

            if found:
                QMessageBox.information(self, "Success", "Sign in successful!")
                self.main_app = AetAIApp()
                self.main_app.show()
                self.close()
                if self.parent:
                    self.parent.hide()
            else:
                QMessageBox.warning(self, "Error",
                                    "Invalid credentials. Please check your information or sign up first.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


class AetherAIApp(QMainWindow):
    def __init__(self):
        super(AetherAIApp, self).__init__()
        self.setWindowTitle("AetherAI Application")
        self.setGeometry(100, 100, 800, 600)
        self.setToolTip("AetherAI Application")
        try:
            self.setWindowIcon(QIcon("AetPictures/logo.png"))
        except:
            pass
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
        try:
            self.signin_button.setIcon(QIcon("AetPictures/signin.png"))
        except:
            pass  # Icon file not found, continue without icon
        self.signin_button.clicked.connect(self.signIn)
        button_layout.addWidget(self.signin_button)

        self.signup_button = QPushButton("Sign Up", self.central_widget)
        self.signup_button.setMinimumSize(150, 50)
        try:
            self.signup_button.setIcon(QIcon("AetPictures/signup.png"))
        except:
            pass  # Icon file not found, continue without icon
        self.signup_button.clicked.connect(self.signUp)
        button_layout.addWidget(self.signup_button)

        layout.addLayout(button_layout)
        self.central_widget.setLayout(layout)

    def signIn(self):
        self.signInWindow = SignInWindow(parent=self)
        self.signInWindow.show()

    def signUp(self):
        self.signUpWindow = SignUpWindow(parent=self)
        self.signUpWindow.show()


def start_app():
    app = QApplication(sys.argv)

    with open('AetAIApp.qss', 'r') as file:
        app.setStyleSheet(file.read())

    app.setApplicationName("AetherAI")

    try:
        font_id = QFontDatabase.addApplicationFont("FontFile/WDXLLubrifontSC-Regular.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            app.setFont(QFont(font_family, 12))
        else:
            print("Font not found, using default font")
    except:
        print("Font file not found, using default font")

    main_window = AetherAIApp()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_app()