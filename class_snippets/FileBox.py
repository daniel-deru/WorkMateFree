from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QLabel, QFrame
from PyQt5.QtGui import QFont


import os
import sys
import math
db_path = os.path.abspath(os.getcwd())
sys.path.insert(0, db_path)
from database.db import DB


file_stylesheet = """
    QCheckBox::indicator {
        width: 25px;
        height: 25px
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

active_stylesheet = """
 QCheckBox::indicator {
        width: 35px;
        height: 35px
    }
    QCheckBox::indicator:checked {
        image: url(images/toggle-on.png);
        width: 35px;
        height: 35px
    }
    QCheckBox::indicator:unchecked {
        image: url(images/toggle-off.png);
        width: 35px;
        height: 35px;
    }
"""

def make_file_container(data, call):
    db = DB()
    files = db.read("files", "category_name", data[0])

    settings = DB().read("settings")
    color = settings[0][1]
    font = settings[0][2]
    
    file_container = QWidget()
    file_container.setObjectName("file_container")

    app_font = QFont(font, 18)
    

    file_layout = QVBoxLayout()
    file_container.setLayout(file_layout)

    frame = QFrame()
    frame.setFont(app_font)
    frame.setObjectName("frame")
    
    title_hbox = QHBoxLayout()
    title_hbox.setObjectName("hbox_title")

    file_layout.addLayout(title_hbox)
    file_layout.addWidget(frame)

    title = QLabel()
    title.setObjectName("title")
    title.setFont(app_font)
    title.setText(data[0])

    active = QCheckBox()
    active.setFont(app_font)
    active.setObjectName("active")
    active.setText("Active")
    active.setChecked(data[1])
    active.setStyleSheet(active_stylesheet)
    active.stateChanged.connect(lambda: call(data[0], active.isChecked()))
    
    title_hbox.addWidget(title)
    title_hbox.addWidget(active)

    frame_grid = QGridLayout()
    frame.setLayout(frame_grid)
    file_count = len(files)
    for i in range(0, file_count):
        
        checkbox = QCheckBox()
        checkbox.setObjectName("file")
        checkbox.setFont(app_font)
        checkbox.setStyleSheet(file_stylesheet)
        checkbox.setText(files[i][0])
        if files[i][2]:
            checkbox.setChecked(True)
        
        column = i % 2
        row = math.floor(i / 2)

        if column == 0:
            frame_grid.addWidget(checkbox, row, column)

        if column == 1:
            frame_grid.addWidget(checkbox, row, column)


    file_container.setStyleSheet(f"""
        #note_container {{
            min-height: 100px;
        }}
        #frame {{
            border: 2px solid white;
            background-color: white;
            color: {color};
            border-radius: 10px;
        }}

        #title {{
            font-size: 20px;
            color: white;
        }}

        #active {{
            font-size: 20px;
            color: white;
        }}

        #file {{
            color: black;
            background-color: white;
            font-size: 16px;
        }}
    """)

    return file_container

# make_file_container(("test", 1))








