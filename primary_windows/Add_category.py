import os
import sys
import re
db_path = os.path.abspath(os.getcwd())
sys.path.insert(0, db_path)
from database.db import DB

from PyQt5.QtWidgets import  QCheckBox, QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFontDatabase, QFont, QIcon

# Import Add Category UI
from uipy.add_categoryUI import Ui_add_category

# Import the Windows
from secondary_windows.URL import URLWindow
from secondary_windows.File import FileWindow


# Import message box
from class_snippets.MessageBox import Message

# container to keep all the websites data in memory before the app category is
# created and saved in the database
files = []

checkbox_styles = """
    QCheckBox {
        color: white;
        font-size: 14px;
    }
     QCheckBox::indicator {
        width: 25px;
        height: 25px;
    }
    QCheckBox::indicator:checked {
        image: url(images/toggle-on.png);
        width: 25px;
        height: 25px;
    }
    QCheckBox::indicator:unchecked {
        image: url(images/toggle-off.png);
        width: 25px;
        height: 25px;
    }
"""

main_stylesheet = """QDialog {
	background-color: #007EA6;
}

QCheckBox {
	font-size: 16px;
}

QPushButton {
	color: white;
	border: 2px solid white;
	background-color: transparent;
	padding: 5px;
	border-radius: 5px;
	font-size: 16px;
}

QPushButton:pressed {
	color: #007EA6;
	background-color: white;
}

QLineEdit {
	font-size: 16px;
	border-radius: 10px;
	padding: 10px;
}

QLabel {
		color: white;
		font-size: 16px;
}"""

class CategoryWindow(QDialog, Ui_add_category):
    category_signal = pyqtSignal(str)
    def __init__(self, name=None):
        super(CategoryWindow, self).__init__()
        self.name = name
        
        self.setupUi(self)
        self.load_settings()
        self.setModal(True)
        self.setWindowIcon(QIcon("images/WorkMate.png"))
        if name:
            self.setWindowTitle(f"Edit {name} Category")
        else:
            self.setWindowTitle(f"Add Category")
        # QFontDatabase.addApplicationFont("fonts/Nunito-SemiBoldItalic.ttf")
       

        self.show_files()
        

        if name != None:
            self.load_data(name)
        
        # Connections to button click events
        # Important Note the lbl is actually a button
        self.lbl_save.clicked.connect(self.add_category_save_clicked)
        self.lbl_discard.clicked.connect(self.add_category_discard_clicked)
        self.lbl_add_url.clicked.connect(self.add_url_clicked)
        self.lbl_add_file.clicked.connect(self.add_file)
        self.btn_delete.clicked.connect(self.delete_clicked)
    
    # Handle the Save button click
    def add_category_save_clicked(self):
        
        category_name = self.add_category_name_input.text()

        if (category_name):
            
            # Check if the category is in the database
            db = DB()
            categories = db.read("categories")
            
            # if db is empty then just add the data
            if len(categories) == 0:
                self.save_db(category_name)                
            # if the database isn't empty than do the following
            else:
                category_count = len(categories)
                for i in range(0, category_count):
                    # send a message that the category already exists and break out of the loop
                    if self.name == None:
                        if categories[i][0] == category_name:
                            Message("The category name you entered already exists. Please enter a unique category name", "Invalid Name")
                            break
                        # check to make sure the loop went through the whole database and add the data if the data doesn't exist 
                        elif i + 1 == category_count: 
                            self.save_db(category_name)
                    else:
                        self.save_db(category_name)
                        break

        else:
            Message( "Please enter the name of your category", "Please enter a name")
   

    # Handle the Discard button click
    def add_category_discard_clicked(self):
        # remove items from memory
        for item in range(0, len(files)):
            files.pop()
        self.hide()

    # Open the URL Window 
    def add_url_clicked(self):
        url = URLWindow()
        url.url_signal.connect(self.updated)
        url.exec_()

    # Remove the websites from memory if the user closes the window
    def closeEvent(self, event):
        if (event):
            for item in range(0, len(files)):
                files.pop()

    # Open the file window 
    def add_file(self):
        file_window = FileWindow()
        file_window.file_signal.connect(self.updated)
        file_window.exec_()

    # delete the selected items
    def delete_clicked(self):

        for i in range(len(files)):
            # check if the file is selected, remove the file and recursively call the delete function
            # until there are no more selected checkboxes
            if files[i][2] == 1:
                files.pop(i)
                return self.delete_clicked()
            
        self.show_files()
    
    # handle saving data to database
    def save_db(self, category_name):
        # make empty list to edit append information
        db_files = []
        for i in range(0, len(files)):
            # custom function to make file id
            file_id = self.make_id(category_name, files[i][0], files[i][1])

            # Add category name and file id in this specific order DON'T SWAP THE ORDER
            files[i].append(category_name)
            files[i].append(file_id)
            db_file = tuple(files[i])
            db_files.append(db_file)
            self.hide()
        
        
        # save data if it is not an edit
        if self.name == None:
            db = DB()
            db.save("categories", (category_name, 1))

            db2 = DB()
            db2.save("files", db_files)
        # update information if it is an edit
        else:
            db = DB()
            db.update("categories", self.name, (category_name, 1))

            db2 = DB()
            db2.update("files", self.name, db_files)

        # Clear memory
        for item in range(0, len(files)):
            files.pop()

        # send signal save was successfull
        self.category_signal.emit("category saved")

    # update the add category window when a new url or file is added
    def updated(self, event):
        if event == "url added" or event == "file added":
            self.show_files()
    
    # make id for files
    def make_id(self, category_name, file_name, file_path):
        category = 0
        name = 0
        path = 0

        for char in category_name:
            category += ord(char)

        for char in file_name:
            name += ord(char)

        for char in file_path:
            path += ord(char)
        
        file_id = str(category) + str(name) + str(path)
        return int(file_id) 
        
    # show the files from the files list 
    def show_files(self):
        container = self.vbox_container
        count = container.count()
        for i in range(count):
            if container.itemAt(i).widget():
                container.itemAt(i).widget().deleteLater()
        font = DB().read("settings")
        checkbox_font = QFont(font[0][2], 18)
        # Create checkbox and add it to the window
        if len(files) > 0:
            for file in files:
                checkbox = QCheckBox()
                checkbox.setText(file[0])
                checkbox.setFont(checkbox_font)
                checkbox.setStyleSheet(checkbox_styles)
                checkbox.setChecked(file[2])
                checkbox.stateChanged.connect(self.checkbox_event_handler)
                container.addWidget(checkbox)
            
    
    # load the data from database if it is an edit window
    def load_data(self, name):
        db = DB()
        db_files = db.read("files", "category_name", name)

        self.add_category_name_input.setText(name)

        for file in db_files:
            file = file[0:3]
            files.append(list(file))

        # show the files after the files list is updated
        self.show_files()
    
    # update the files list when checkbox is checked
    def checkbox_event_handler(self):
        container = self.vbox_container
        count = container.count()
        for i in range(count):
            # get the checkbox
            checkbox = container.itemAt(i).widget()
            # create the state for db
            state = 1 if checkbox.isChecked() else 0
            # update the files list
            files[i][2] = state
        
    
    def load_settings(self):
        db = DB()
        settings = db.read("settings")
        updated_stylesheet = re.sub("#007EA6", settings[0][1], main_stylesheet)
        self.setStyleSheet(updated_stylesheet)

        app_font = QFont(settings[0][2], 18)

        widgets = [
        self.lbl_name,
        self.lbl_add_file,
        self.lbl_add_url,
        self.lbl_discard,
        self.lbl_save, 
        self.btn_delete,
        self.add_category_name_input
        ]

        for widget in widgets:
            widget.setFont(app_font)
        
