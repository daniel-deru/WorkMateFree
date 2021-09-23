from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont, QIcon, QFontDatabase

class Message:
    def __init__(self, text, title):
        QFontDatabase.addApplicationFont("fonts/Nunito-SemiBoldItalic.ttf")
        
        message = QMessageBox()
        message.setIcon(QMessageBox.Warning)
        message.setText(text)
        message.setWindowTitle(title)
        message.setWindowIcon(QIcon("images/WorkMate"))
        message.setFont(QFont("Nunito SemiBold", 18))
        message.exec_()
        
        