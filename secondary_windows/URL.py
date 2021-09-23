import os
import sys
import re
root = os.path.abspath(os.getcwd())
sys.path.insert(0, root)

from database.db import DB

from  PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QFontDatabase, QIcon

# Import the URL Window UI
from uipy.add_url import Ui_add_url_window

# Import the message box
from class_snippets.MessageBox import Message


url_stylesheet = """QDialog {
	background-color: #007EA6;
}

QLabel {
	color: white;
	font-size: 16px;
}

QPushButton {
	color: white;
	border: 2px solid white;
	border-radius: 10px;
	padding: 5px;
	font-size: 16px;
}

QPushButton:pressed {
	color: #007EA6;
	background-color: white;
}

QLineEdit {
	font-size: 16px;
	padding: 5px;
	border-radius: 5px;
}"""

class URLWindow(QDialog, Ui_add_url_window):
    url_signal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(URLWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Add Website")
        self.load_settings()

        self.setWindowIcon(QIcon("images/WorkMate.png"))

        # Connections to button click events
        self.btn_discard.clicked.connect(self.discard_clicked)
        self.btn_save.clicked.connect(self.save_clicked)
        
    # Handle the Discard button click
    def discard_clicked(self):
        self.hide()
    
    # Handle the Save Button click
    def save_clicked(self):
        
        
        # Get the info from URL Window
        name = self.lnedit_name.text()
        path = self.lnedit_url.text()

        websiteReg = "^(https?://)|(www\.).+\."
        match = re.search(websiteReg, path)

        if match == None:
            Message("The URL you entered is invalid. Please enter a valid url.", "Invalid URL")
            return

        # If there is a name and url create a payload to store in website variable
        if ( not name and not path):
            # If the user didn't enter all the required information show a message
            Message("Please fill in all the fields", "There are empty fields")
        elif (name and path):
            # Import the websites from the category window to add the websites
            from primary_windows.Add_category import files

            is_copy = False

            for file in files:
                if (name == file[0]):
                    Message("The name is already being used. Please use another name", "Name already exists.")
                    is_copy = True
                elif (path == file[1]):
                    Message("The website is already being used. Cannot add the same website.", "Website already exists.")
                    is_copy = True
            
            if (not is_copy):
                payload = [
                    name,
                    path,
                    1
                ]
        
                files.append(payload)
                self.url_signal.emit("url added")
                self.hide()
            
    
    # Create a new instance of the Category Window when the user closes the URL window
    def closeEvent(self, event):
        if (event):
            event.accept()
    
    def load_settings(self):
        settings = DB().read("settings")
        app_font = QFont(settings[0][2])

        widgets = [
            self.btn_discard,
            self.btn_save,
            self.lbl_name,
            self.lbl_url,
            self.lnedit_name,
            self.lnedit_url,
        ]
        
        for widget in widgets:
            widget.setFont(app_font)

        updated_stylesheet = re.sub("#007EA6", settings[0][1], url_stylesheet)
        self.setStyleSheet(updated_stylesheet)