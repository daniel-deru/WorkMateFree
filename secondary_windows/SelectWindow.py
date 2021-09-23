import os
import sys
import re
db_path = os.path.abspath(os.getcwd())
sys.path.insert(0, db_path)

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import  QDialog, QRadioButton
from PyQt5.QtGui import QFont, QFontDatabase, QIcon

from uipy.selectNotesUI import Ui_SelectWindow
from database.db import DB

from primary_windows.Notes import NotesWindow
from primary_windows.Add_category import CategoryWindow

radio_stylesheet = """
    QRadioButton::indicator:unchecked {
        image: url(images/radio-off.png);
        width: 25px;
        height: 25px;
    }

    QRadioButton::indicator:checked {
        image: url(images/radio-on.png);
        width: 25px;
        height: 25px;
    }
"""

select_stylesheet = """QDialog {
	background-color: #007EA6;
    }

    QPushButton {
                    font-size: 16px;
                    color: white;
                    border: 2px solid white;
                    border-radius: 10px;
                    padding: 5px;
                    background-color: transparent;
                }

    QPushButton:pressed {
            color: #007EA6;
            background-color: white;
    }

    QRadioButton {
	color: white;
	font-size: 16px;
    }

    QWidget {
	background-color: #007EA6;
    }"""

class SelectWindow(QDialog, Ui_SelectWindow):
    # signal for show edit was successfully handled
    edit_signal = pyqtSignal(str)
    def __init__(self, table):
        super(SelectWindow, self).__init__()
        self.table = table
        self.setupUi(self)
        self.load_settings()
        self.setModal(True)
        self.show(table)
        
        self.setWindowIcon(QIcon("images/WorkMate.png"))
        self.setWindowTitle(f"Edit {table.capitalize()}")

        # button click connections
        self.btn_discard.clicked.connect(self.discard_clicked)
        self.btn_edit.clicked.connect(self.edit_clicked)
    
    # get the data from database
    def show(self, table):
        db = DB()
        items = db.read(table)
        self.make_buttons(items)

    # make the buttons
    def make_buttons(self, items):
        for item in items:
            name = item[0]
            self.radio = QRadioButton(name)
            self.radio.setFont(self.app_font)
            self.radio.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    color: white;
                    border: 2px solid white;
                    border-radius: 10px;
                    padding: 5px;
                    background-color: transparent;
                }

                QPushButton:pressed {
                    color: #007ea6;
                    background-color: white;
                }
            """)
            self.radio.setStyleSheet(radio_stylesheet)
            self.verticalLayout.addWidget(self.radio)

    # note or category when one is selected
    def edit_clicked(self):
        items = self.verticalLayout.count()

        name = ""
        for i in range(items):
            item = self.verticalLayout.itemAt(i)
            if item.widget():
                if item.widget().isChecked():
                    name = item.widget().text()
                    # open notes if it is a note
                    if self.table == "notes":
                        note = NotesWindow(self.table, name)
                        note.note_signal.connect(lambda: self.edit_signal.emit("note saved"))
                        note.exec_()
                        # open categories if it is a category
                    elif self.table == "categories":
                        app = CategoryWindow(name)
                        app.category_signal.connect(lambda: self.edit_signal.emit("category saved"))
                        app.exec_()

                    self.hide()

    def discard_clicked(self):
        self.hide()
    
    def load_settings(self):
        settings = DB().read("settings")
        self.app_font = QFont(settings[0][2])

        self.btn_discard.setFont(self.app_font)
        self.btn_edit.setFont(self.app_font)

        updated_stylesheet = re.sub("#007EA6", settings[0][1], select_stylesheet)   
        self.setStyleSheet(updated_stylesheet)
        