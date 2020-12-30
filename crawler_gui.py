import json
import sys
import time
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QComboBox,
    QPushButton,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QMessageBox,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QListWidget,
    QListWidgetItem,
    QGridLayout,
)

from helpers import get_domain_data, add_domain, is_online, check_endpoint


class WindowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crawler UI")
        self.setFixedSize(300, 300)
        self.route_combo = QComboBox()
        self.button = QPushButton()
        self.title_label = QLabel()
        self.domain_input_field = QLineEdit()
        self.response_textbox = QTextEdit()
        self.response_window = QWidget()
        self.version_label = QLabel()
        self.warning_label = QLabel()
        self.message_box = QMessageBox()
        #block
        self.title_label2 = QLabel()
        self.language_label = QLabel()
        self.country_label = QLabel()
        self.email_label = QLabel()
        self.phone_label = QLabel()
        self.emails = QListWidget()
        self.phone_numbers = QListWidget()
        self.last_updated_label = QLabel()
        self.setup_ui()
        self.create_layout()
        self.check_requirements()

    def setup_ui(self):
        self.route_combo.addItem("Add route for crawling")
        self.route_combo.addItem("Get data from crawler")
        self.button.setText("Click Me")
        self.button.clicked.connect(self.route_choice)
        self.title_label.setText("CrawlerUI")
        self.title_label.setFont(QFont("Times New Roman", 15))
        self.title_label.setStyleSheet("color:black")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.domain_input_field.setText("Example.com")
        self.version_label.setText("v1.0.0")
        self.version_label.setFont(QFont("Times New Roman", 12))
        self.version_label.setStyleSheet("color:black")
        self.version_label.setAlignment(Qt.AlignRight)
        self.warning_label.setFont(QFont("Times New Roman", 12))
        self.warning_label.setStyleSheet("color:black")
        self.warning_label.setAlignment(Qt.AlignCenter)
        self.response_window.setFixedSize(600,600)

    def route_choice(self):
        if self.route_combo.currentText() == "Add route for crawling":
            self.create_messagebox()
        else:
            self.create_table()

    def create_messagebox(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("Info")
        message = add_domain(self.domain_input_field.text())
        message_box.setStandardButtons(QMessageBox.Ok)
        if type(message) is str:
            message_box.setText(message)
            message_box.setIcon(QMessageBox.Icon.Critical)
        else:
            message_box.setIcon(QMessageBox.Icon.Information)
            if message["message"] == "added":
                message_box.setText(f'Started crawling {self.domain_input_field.text()}')
            elif message["message"] == "started anew":
                message_box.setText(f'Recrawling {self.domain_input_field.text()}')
            else:
                message_box.setText(f'Already crawling {self.domain_input_field.text()}')
        message_box.exec_()

    def create_table(self):
        try:
            data = json.loads(get_domain_data(self.domain_input_field.text()))
            grid = QGridLayout()
            #title_label = QLabel()
            # title_label.repaint()
            # title_label.setText(f'Showing results for {data["domain"]}')
            # title_label.setFont(QFont("Times New Roman", 15))
            self.title_label2.repaint()
            self.title_label2.setText(f'Showing results for {data["domain"]}')
            self.title_label2.setFont(QFont("Times New Roman", 15))

            #language_label = QLabel()
            #language_label.setText(f'Language: {data["language"]}')
            self.language_label.repaint()
            self.language_label.setText(f'Language: {data["language"]}')
            email_label = QLabel()
            self.email_label.repaint()
            self.email_label.setText("Emails:")
            phone_label = QLabel()
            self.email_label.repaint()
            self.phone_label.setText("Phone numbers:")
            country_label = QLabel()
            self.country_label.repaint()
            self.country_label.setText(f'Country: {data["country"]}')
            phone_numbers = QListWidget()
            emails = QListWidget()
            self.phone_numbers.clear()
            self.emails.clear()
            self.phone_numbers.repaint()
            self.emails.repaint()
            if data["phone_numbers"]:
                self.phone_numbers.addItems(data["phone_numbers"])
            else:
                self.phone_numbers.addItems(["No phone numbers found"])
            if data["emails"]:
                self.emails.addItems(data["emails"])
            else:
                self.emails.addItems(["No emails found"])
            last_updated_label = QLabel()
            self.last_updated_label.repaint()
            self.last_updated_label.setText(f'Last updated at: {data["updated_at"]}')
            grid.addWidget(self.title_label2, 0, 0, 1, 2, alignment=Qt.AlignCenter)
            grid.addWidget(self.language_label, 1, 0)
            grid.addWidget(self.country_label, 2, 0)
            grid.addWidget(self.email_label, 3, 0)
            grid.addWidget(self.phone_label, 3, 1)
            grid.addWidget(self.emails, 4, 0)
            grid.addWidget(self.phone_numbers, 4, 1)
            grid.addWidget(self.last_updated_label, 5, 0, 1, 2, alignment=Qt.AlignRight)
            self.response_window.setLayout(grid)
            self.response_window.show()
            return
        except json.decoder.JSONDecodeError:
            data = get_domain_data(self.domain_input_field.text())
            message_box = QMessageBox()
            message_box.setText(data)
            message_box.setIcon(QMessageBox.Icon.Question)
            message_box.exec_()

    def create_layout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.title_label)
        vbox.addWidget(self.route_combo)
        vbox.addWidget(self.domain_input_field)
        vbox.addWidget(self.button)
        vbox.addWidget(self.version_label)
        vbox.addWidget(self.warning_label)
        self.setLayout(vbox)

    def check_requirements(self):
        # display only most severe issue
        if not check_endpoint():
            self.warning_label.setText("Endpoint offline")
            self.button.setDisabled(True)
        elif not is_online():
            self.warning_label.setText("Check your internet connection!")
            self.button.setDisabled(True)
        else:
            self.warning_label.setText("Ready for crawling")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WindowWidget()
    window.show()
    sys.exit(app.exec_())
