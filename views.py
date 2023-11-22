import os.path
import sys
import sqlite3

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLineEdit, QWidget, QMessageBox, \
    QStackedWidget, QComboBox, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QBrush, QPixmap, QPalette, QIcon


class DataBase(QMainWindow):
    def __init__(self):
        super().__init__()

        if not os.path.isfile('developers.db'):
            self.create_table()

        background = QPixmap('fon2.jpg')
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
        self.setPalette(palette)

        icon = QIcon('yarlyk.png')
        self.setWindowIcon(icon)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.setWindowTitle("Table Database")
        self.setFixedSize(QSize(700, 700))
        self.stacked_widget = QStackedWidget()

        self.add_user_widget = self.create_add_user_widget()
        self.get_user_widget = self.create_get_user_widget()

        self.stacked_widget.addWidget(self.add_user_widget)
        self.stacked_widget.addWidget(self.get_user_widget)

        layout.addWidget(self.stacked_widget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        menubar = self.menuBar()
        main_menu = menubar.addMenu("Main menu")

        add_user_action = QAction("Add new developer", self)
        add_user_action.triggered.connect(self.show_add_user)
        main_menu.addAction(add_user_action)

        get_user_action = QAction("Get data about developer", self)
        get_user_action.triggered.connect(self.show_get_user)
        main_menu.addAction(get_user_action)

    def create_table(self):
        connect = sqlite3.connect('developers.db')
        cursor = connect.cursor()
        cursor.execute(
            """CREATE TABLE Developers(
            id INTEGER PRIMARY KEY,
            name TEXT,
            surname TEXT,
            second_name TEXT,
            phone TEXT,
            mail TEXT,
            level TEXT,
            direction TEXT,
            education TEXT,
            general_characteristics TEXT  
            )"""
        )
        connect.commit()
        connect.close()

    def fill_db(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        second_name = self.second_name_input.text()
        phone = self.phone.text()
        mail = self.mail_input.text()
        level = self.level_input.currentText()
        direction = self.direction_input.currentText()
        education = self.education_input.currentText()
        general_characteristics = self.general_characteristics_input.text()

        data = (name, surname, second_name, phone, mail, level, direction, education, general_characteristics)
        for info in data:
            if not info:
                self.messege_add_box("Fill all lines")
                return
        connect = sqlite3.connect('developers.db')
        cursor = connect.cursor()

        try:
            cursor.execute("""INSERT INTO Developers(name, surname, second_name, phone, mail, level, direction, education,
             general_characteristics)  VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)
            connect.commit()
            connect.close()
            self.messege_add_box("Developer was added")
            objects = [self.name_input, self.surname_input,
             self.second_name_input, self.mail_input,
             self.phone, self.general_characteristics_input]
            for obj in objects:
                obj.clear()
        except Exception as e:
            print(e)
            connect.close()

    def get_user(self):
        connect = sqlite3.connect('developers.db')
        cursor = connect.cursor()
        name = self.get_name_input.text()
        surname = self.get_surname_input.text()

        if not name or not surname:
            self.messege_add_box("Fill all lines")
            return
        try:
            cursor.execute("""SELECT * FROM Developers WHERE name = ? AND surname = ?""", (name, surname))
            result = cursor.fetchone()
            if not result:
                self.messege_add_box("Developer not found")
                connect.close()
                return
            connect.close()
            txt = (f'Name: {result[1]}\n'
                   f'Surname: {result[2]}\n'
                   f'Second_name: {result[3]}\n'
                   f'Phone {result[4]}\n'
                   f'eMail: {result[5]}\n'
                   f'Level {result[6]}\n'
                   f'Direction: {result[7]}\n'
                   f'Education: {result[8]}\n'
                   f'General characteristic: {result[9]}')
            self.messege_add_box(txt)
            self.get_name_input.clear()
            self.get_surname_input.clear()
        except Exception as e:
            print(e)

    def messege_add_box(self, text):
        mesbox = QMessageBox()
        mesbox.setText(text)
        mesbox.exec()

    def create_add_user_widget(self):
        directions =['Software Development', 'System Administration', 'Information Security',
                     'Data Analysis and Machine Learning',
                     'Internet of Things', 'Cloud Technologies', 'Big Data', 'DevOps', 'Virtualization',
                     'Project Management', 'Software Testing',
                     'Version Control Systems',
                     'Computer Graphics and Design', 'Technical Support', 'Blockchain and Cryptocurrencies']

        levels = ['Student', 'Junior', 'Middle', 'Senior', 'Lead']

        widget = QWidget()
        layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Input developer name")
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Input developer surname")
        self.second_name_input = QLineEdit()
        self.second_name_input.setPlaceholderText("Input developer second name")
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone")
        self.mail_input = QLineEdit()
        self.mail_input.setPlaceholderText("Email")
        self.level_input = QComboBox()
        self.level_input.addItems(levels)
        self.direction_input = QComboBox()
        self.direction_input.addItems(directions)
        self.education_input = QComboBox()
        self.education_input.addItems(['Yes', 'No'])
        self.general_characteristics_input = QLineEdit()
        self.general_characteristics_input.setPlaceholderText("General characteristics")
        add_button = QPushButton("ADD DEVELOPER")
        add_button.clicked.connect(self.fill_db)

        layout.addWidget(QLabel('Name'))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel('Surname'))
        layout.addWidget(self.surname_input)
        layout.addWidget(QLabel('Second name'))
        layout.addWidget(self.second_name_input)
        layout.addWidget(QLabel('Phone'))
        layout.addWidget(self.phone)
        layout.addWidget(QLabel('Email'))
        layout.addWidget(self.mail_input)
        layout.addWidget(QLabel('Skill level'))
        layout.addWidget(self.level_input)
        layout.addWidget(QLabel('Direction'))
        layout.addWidget(self.direction_input)
        layout.addWidget(QLabel('Education'))
        layout.addWidget(self.education_input)
        layout.addWidget(QLabel('General characteristics'))
        layout.addWidget(self.general_characteristics_input)
        layout.addWidget(add_button)
        layout.addWidget(add_button)
        widget.setLayout(layout)
        return widget

    def create_get_user_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.get_name_input = QLineEdit()
        self.get_surname_input = QLineEdit()

        get_button = QPushButton("Get data")
        get_button.clicked.connect(self.get_user)
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.get_name_input)
        layout.addWidget(QLabel("Surname:"))
        layout.addWidget(self.get_surname_input)
        layout.addWidget(get_button)
        layout.setAlignment(get_button, Qt.AlignmentFlag.AlignTop)
        widget.setLayout(layout)
        return widget

    def show_add_user(self):
        self.stacked_widget.setCurrentWidget(self.add_user_widget)

    def show_get_user(self):
        self.stacked_widget.setCurrentWidget(self.get_user_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataBase()
    window.show()
    sys.exit(app.exec())
