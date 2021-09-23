import os
import sys
import re
db_path = os.path.abspath(os.getcwd())
sys.path.insert(0, db_path)

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QFontDatabase, QFont, QIcon

from uipy.edit_notes import Ui_edit_notes



from database.db import DB
from datetime import date
from class_snippets.MessageBox import Message

radio_stylesheet1 = """
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
    QRadioButton {
        color: #EC4B4B;
    }
"""
radio_stylesheet2 = """
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
    QRadioButton {
        color: #E8ED09;
    }
"""
radio_stylesheet3 = """
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
    QRadioButton {
        color: #36E432;
    }
"""
notes_stylesheet = """#edit_notes {
	background-color: #007EA6;

}

QLabel {
	color: white;
	font-size: 20px;
}

QRadioButton {
	color: white;
	font-size: 16px;
	font-weight: bold;
}

QPushButton {
	color: white;
	border: 2px solid white;
	border-radius: 10px;
	background-color: transparent;
	padding: 5px;
	font-size: 16px;
}

QPushButton:pressed {
	color: #007EA6;
	background-color: white;
}

#rbtn_high {
	color: #D60025;
}

#rbtn_low {
	color: #90FA00;
}

#rbtn_medium {
	color: #FAE700;
}

QLineEdit {
	font-size: 16px;
	border-radius: 10px;
	padding:5px;
}

QTextEdit {
	font-size: 16px;
	border-radius: 10px;
	padding:5px;
	background-color: palette(base);
}"""


class NotesWindow(QDialog, Ui_edit_notes):
    # signal to show note was handled successfully
    note_signal = pyqtSignal(str)
    def __init__(self, table = None, name = None):
        super(NotesWindow, self).__init__()
        self.table = table
        self.name = name
        self.setupUi(self)
        self.load_settings()
        self.setModal(True)
        self.setWindowIcon(QIcon("images/WorkMate.png"))
        if name:
            self.setWindowTitle(f"Edit {name} Note")
        else:
            self.setWindowTitle("Add Note")

        # check the first radiobutton
        self.hbox_importance.itemAt(0).widget().setChecked(True)

        # handle the slot connections
        self.btn_discard.clicked.connect(self.notes_window_discard_clicked)
        self.btn_save.clicked.connect(self.notes_window_save_clicked)

        if table is not None and name is not None:
            self.load_data(table, name)

    def notes_window_discard_clicked(self):
        self.hide()

    # handle save click
    def notes_window_save_clicked(self):

        # Get the values from the form
        name = self.ldt_note_title.text()
        body = self.txtedt_note_body.toPlainText()
        priority = self.hbox_importance.itemAt(0).widget().text()
        current_date = date.today().strftime("%B %d, %Y")

        importance_container = self.hbox_importance

        # get the priority from the note window
        for i in range(0, 3):
            priority_box = importance_container.itemAt(i).widget()
            if priority_box.isChecked():
                priority = priority_box.text()
        
        # make the note tuple to send to database
        note = (
            name,
            body,
            priority,
            current_date
        )

        # Send a Message if there is missing data
        if not name or not body:
            Message("There are missing fields. Please make sure your note has a title and a body.", "Missing Fields")

        # Check if there is a title and body
        else:
            if self.table == None and self.name == None:
                
                # Check if name is already in database
                db = DB()
                items = db.read("notes")

                # save the notes if there are no notes
                if  len(items) == 0:
                    db = DB()
                    db.save("notes", note)
                    self.note_signal.emit("note saved")
                    self.hide()
                
                # save if there are already notes and check if the note doesn't already exist
                for i in range(0, len(items)):
                    if items[i][0] == name:
                        Message("The title you entered is already being used. Please Choose a different title", "title already used.")
                        break
                    # Make sure it's not an edit
                    elif i + 1 == len(items):
                        db = DB()
                        db.save("notes", note)
                        self.note_signal.emit("note saved")
                        self.hide()           
            # Update the existing note in the database
            else:
                db = DB()
                db.update(self.table, self.name, note)
                self.note_signal.emit("note saved")
                self.hide()
    
    # load the data if the window is opened in edit mode
    def load_data(self, table, name):
        db = DB()
        
        # get the data from database
        item = db.get_item(table, name)
        title = item[0]
        body = item[1]
        priority = item[2]

        # put the data in the window
        self.ldt_note_title.setText(title)
        self.txtedt_note_body.setText(body)
        count = self.hbox_importance.count()

        for i in range(count):
            widget = self.hbox_importance.itemAt(i).widget()
            if priority == widget.text():
                widget.setChecked(True)
    
    def load_settings(self):
        
        self.rbtn_high.setStyleSheet(radio_stylesheet1)
        self.rbtn_medium.setStyleSheet(radio_stylesheet2)
        self.rbtn_low.setStyleSheet(radio_stylesheet3)

        db = DB()
        settings = db.read("settings")

        app_font = QFont(settings[0][2], 18)

        widgets = [
            self.lbl_note_title,
            self.lbl_importance,
            self.lbl_note_body,
            self.txtedt_note_body,
            self.ldt_note_title,
            self.rbtn_high,
            self.rbtn_medium,
            self.rbtn_low,
            self.btn_discard,
            self.btn_save
        ]

        for widget in widgets:
            widget.setFont(app_font)

        updated_stylesheet = re.sub("#007EA6", settings[0][1], notes_stylesheet)
        self.setStyleSheet(updated_stylesheet)


        


