import os
import sys
import re
db_path = os.path.abspath(os.getcwd())
sys.path.insert(0, db_path)

from uipy.deleteNotes import Ui_DeleteWindow

from PyQt5.QtWidgets import QCheckBox, QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QFontDatabase, QIcon

from database.db import DB

checkbox_styles = """
     QCheckBox::indicator {
        width: 15px;
        height: 15px
    }
    QCheckBox::indicator:checked {
        image: url(images/tick.png);
        width: 15px;
        height: 15px
    }
    QCheckBox::indicator:unchecked {
        image: url(images/cross.png);
        width: 15px;
        height: 15px;
    }
"""

delete_stylesheet = """QPushButton {
	color: white;
	font-size: 16px;
	border: 2px solid white;
	border-radius: 10px;
	background-color: transparent;
	padding: 5px;
}

QPushButton:pressed {
	color: #007ea6;
	background-color: white;
}

QDialog {
	background-color: #007EA6;
}

QCheckBox {
	color: white;
	font-size: 16px;
}

QWidget {
	background-color: #007EA6;
}"""

class DeleteWindow(QDialog, Ui_DeleteWindow):
    # signal to be sent when delete was successfull
    delete_signal = pyqtSignal(str)
    def __init__(self, window):
        super(DeleteWindow, self).__init__()
        # get the window name to determine what to delete
        self.window_name = window
        self.setupUi(self)
        self.setModal(True)
        self.load_settings()

        self.setWindowIcon(QIcon("images/WorkMate.png"))
        self.setWindowTitle(f"Delete {window.capitalize()}")

        # connect signals to slots
        self.btn_discard.clicked.connect(self.discard_clicked)
        self.btn_delete.clicked.connect(self.delete_clicked)

    def discard_clicked(self):
        self.hide()

    # delete the selected items
    def delete_clicked(self):
        items = self.verticalLayout_2.count()

        
        for index in range(0, items):
            checkbox = self.verticalLayout_2.itemAt(index).widget()
            if checkbox.isChecked():
                item = checkbox.text()
                db = DB()
                db.delete(self.window_name, item)
          
        self.delete_signal.emit("delete completed")
        self.close()
    
    def load_settings(self):
        settings = DB().read("settings")
        app_font = QFont(settings[0][2])

        self.btn_discard.setFont(app_font)
        self.btn_delete.setFont(app_font)

        updated_stylesheet = re.sub("#007EA6", settings[0][1], delete_stylesheet)
        self.setStyleSheet(updated_stylesheet)

        # show the items in the window
        db = DB()
        items = db.read(self.window_name)
        for item in items:
            checkbox = QCheckBox(item[0])
            checkbox.setFont(app_font)
            checkbox.setStyleSheet(checkbox_styles)
            self.verticalLayout_2.addWidget(checkbox)


