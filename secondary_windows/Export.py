from PyQt5.QtWidgets import QDialog, QCheckBox
from uipy.exportUI import Ui_exportWindow
from database.db import DB

class ExportWindow(QDialog, Ui_exportWindow):
    def __init__(self):
        super(ExportWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Export")
        self.show_data()

        self.chk_box_apps_all.stateChanged.connect(lambda: self.selectAll(self.chk_box_apps_all, self.vbox_apps_container))
        self.chk_box_notes_all.stateChanged.connect(lambda: self.selectAll(self.chk_box_notes_all, self.vbox_notes_container))
        self.btn_export.clicked.connect(self.export)

    def show_data(self):
        
        notes = DB().read("notes")
        apps = DB().read("categories")

        for note in notes:
            checkbox= QCheckBox(note[0])
            self.vbox_notes_container.addWidget(checkbox)
        
        for app in apps:
            checkbox= QCheckBox(app[0])
            self.vbox_apps_container.addWidget(checkbox)

    def selectAll(self, checkbox, container):
        item_count = container.count()
        for i in range(item_count):
            container.itemAt(i).widget().setChecked(checkbox.isChecked())
    
    # only websites can be exported
    def export(self):
        app_fields = ["name", "category_active", "file_name", "path", "file_active", "category_name", "file_id"]
        website_fields = []
        notes_fields = ["title", "body", "priority", "date"]
        csv_headers = []
        
        for i in range(self.vbox_apps_container.count()):
            if self.vbox_apps_container.itemAt(i).widget().isChecked():
                csv_headers += (app_fields + website_fields)
                break

        for i in range(self.vbox_notes_container.count()):
            if self.vbox_notes_container.itemAt(i).widget().isChecked():
                csv_headers += notes_fields
                break

        
        categories = DB().read("categories")
        files = DB().read("files")
        notes = DB().read("notes")
        


