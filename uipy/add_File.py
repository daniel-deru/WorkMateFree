# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_File.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Add_File_Dialog(object):
    def setupUi(self, Add_File_Dialog):
        Add_File_Dialog.setObjectName("Add_File_Dialog")
        Add_File_Dialog.setWindowModality(QtCore.Qt.NonModal)
        Add_File_Dialog.setEnabled(True)
        Add_File_Dialog.resize(425, 131)
        Add_File_Dialog.setMaximumSize(QtCore.QSize(16777215, 200))
        Add_File_Dialog.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Add_File_Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.file_gridlayout = QtWidgets.QGridLayout()
        self.file_gridlayout.setObjectName("file_gridlayout")
        self.lbl_filename = QtWidgets.QLabel(Add_File_Dialog)
        self.lbl_filename.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_filename.setObjectName("lbl_filename")
        self.file_gridlayout.addWidget(self.lbl_filename, 0, 0, 1, 1)
        self.lnedit_filename = QtWidgets.QLineEdit(Add_File_Dialog)
        self.lnedit_filename.setObjectName("lnedit_filename")
        self.file_gridlayout.addWidget(self.lnedit_filename, 0, 1, 1, 1)
        self.btn_add_file = QtWidgets.QPushButton(Add_File_Dialog)
        self.btn_add_file.setObjectName("btn_add_file")
        self.file_gridlayout.addWidget(self.btn_add_file, 1, 0, 1, 1)
        self.lbl_path = QtWidgets.QLabel(Add_File_Dialog)
        self.lbl_path.setMaximumSize(QtCore.QSize(350, 16777215))
        self.lbl_path.setObjectName("lbl_path")
        self.file_gridlayout.addWidget(self.lbl_path, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.file_gridlayout)
        self.hbox_button_container = QtWidgets.QHBoxLayout()
        self.hbox_button_container.setObjectName("hbox_button_container")
        self.btn_discard = QtWidgets.QPushButton(Add_File_Dialog)
        self.btn_discard.setObjectName("btn_discard")
        self.hbox_button_container.addWidget(self.btn_discard)
        self.btn_save = QtWidgets.QPushButton(Add_File_Dialog)
        self.btn_save.setObjectName("btn_save")
        self.hbox_button_container.addWidget(self.btn_save)
        self.verticalLayout.addLayout(self.hbox_button_container)

        self.retranslateUi(Add_File_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Add_File_Dialog)

    def retranslateUi(self, Add_File_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Add_File_Dialog.setWindowTitle(_translate("Add_File_Dialog", "Dialog"))
        self.lbl_filename.setText(_translate("Add_File_Dialog", "Name"))
        self.btn_add_file.setText(_translate("Add_File_Dialog", "Add File"))
        self.lbl_path.setText(_translate("Add_File_Dialog", "Path:"))
        self.btn_discard.setText(_translate("Add_File_Dialog", "Exit"))
        self.btn_save.setText(_translate("Add_File_Dialog", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Add_File_Dialog = QtWidgets.QDialog()
    ui = Ui_Add_File_Dialog()
    ui.setupUi(Add_File_Dialog)
    Add_File_Dialog.show()
    sys.exit(app.exec_())