import os
import sys
import re
root = os.path.abspath(os.getcwd())
sys.path.insert(0, root)

from database.db import DB

# Python Imports
from  PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QIcon

# Import the URL Window UI
from uipy.add_File import Ui_Add_File_Dialog

# Import the message box
from class_snippets.MessageBox import Message

file_stylesheet = """QDialog {
	background-color: #007EA6;
}

#lbl_name{
	text-align: center;
}


QLineEdit {
	padding: 5px;
	border-radius:10px;
}

QPushButton, QLabel, QLineEdit {
	font-size: 16px;
}


QPushButton {
	color: white;
	background-color: transparent;
	border: 2px solid white;
	border-radius: 10px;
	padding: 5px;
}

QPushButton:pressed {
	color: #007EA6;
	background-color: white;
}

 QLabel {
	color: white;
}"""


class FileWindow(QDialog, Ui_Add_File_Dialog):
    file_signal = pyqtSignal(str)
    def __init__(self):
        super(FileWindow, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        
        self.load_settings()
        self.setWindowTitle("Add File")
        self.setWindowIcon(QIcon("images/WorkMate.png"))

        # Connect button click to function
        self.btn_discard.clicked.connect(self.discard_clicked)
        self.btn_save.clicked.connect(self.save_clicked)
        self.btn_add_file.clicked.connect(self.add_file_clicked)
        

    def discard_clicked(self):
        self.hide()

    def save_clicked(self):

        name = self.lnedit_filename.text()

        # make sure there is a name and path
        if (not name and not self.path):
            Message("Please enter a name and add a file", "Empty fields")     
        elif (name and self.path):
            # import files here to avoid a circular import error
            from primary_windows.Add_category import files
            # set is copy to false when the button is clicked
            is_copy = False

            for file in files:
                if (name == file[0]):
                    Message("The name is already being used. Please use another name", "Name already exists.")
                    is_copy = True
                elif (self.path == file[1]):
                    Message("The file is already selected. Cannot add the same file.", "File already exists.")
                    is_copy = True
            
            # check that the file isn't alread in the category
            if (not is_copy):
                payload = [
                    name,
                    self.path,
                    1
                ]

                files.append(payload)
                self.file_signal.emit("file added")
                self.hide()

    # Select file from computer
    def add_file_clicked(self):
        self.path = QFileDialog.getOpenFileName(self, "Open a file", "", "All Files (*.*)")[0]
        short_path  = self.path[0:30]
        display_path = f"Path: {short_path}..."

        self.lbl_path.setText(display_path)
        

    # Create a new instance of the Category Window when the user closes the URL window
    def closeEvent(self, event):
        if (event):
            event.accept()
    
    def load_settings(self):
        settings = DB().read("settings")
        app_font = QFont(settings[0][2])

        widgets = [
            self.btn_save,
            self.btn_discard,
            self.btn_add_file,
            self.lbl_filename,
            self.lbl_path,
            self.lnedit_filename
        ]
        
        for widget in widgets:
            widget.setFont(app_font)

        updated_stylesheet = re.sub("#007EA6", settings[0][1], file_stylesheet)
        self.setStyleSheet(updated_stylesheet)

       