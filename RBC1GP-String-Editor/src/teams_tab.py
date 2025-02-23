from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QLineEdit, QLabel, QPushButton
from PyQt6.QtWidgets import QWidget, QTreeWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QTreeWidgetItem

import file_reader


class TeamsTab(QWidget):
    def __init__(self, rival_file: file_reader.RivalFile):
        super().__init__()
        self.team_idx = 0
        self.rival_file = rival_file
        self.teams_tree_view = QTreeWidget()

        self.encoding, self.decoding = file_reader.load_encoding_table('resources//c1gp.tbl')
        self.mod_encoding, self.mod_decoding = file_reader.load_encoding_table('resources//modified.tbl')

        self.teams = rival_file.get_teams()
        self.team_name = QLineEdit()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setup_layout()

        # self.reset()

    def setup_layout(self):
        left_vbox = QVBoxLayout()
        tree_scroll_area = QScrollArea()
        self.teams_tree_view.setHeaderHidden(True)
        tree_scroll_area.setWidget(self.teams_tree_view)
        tree_scroll_area.setWidgetResizable(True)
        left_vbox.addWidget(tree_scroll_area)
        tree_scroll_area.setMaximumWidth(175)
        self.layout.addLayout(left_vbox)

        for team in self.teams:
            # print(file_reader.decode_string(rival['nickname'], encoding).strip('\x00'))
            item = QTreeWidgetItem([file_reader.decode_string(team['team_name'], self.mod_encoding).strip('\x00')])
            self.teams_tree_view.addTopLevelItem(item)

        self.teams_tree_view.itemClicked.connect(self.team_selected)

        right_vbox = QVBoxLayout()
        self.layout.addLayout(right_vbox)

        right_vbox.addWidget(QLabel("Team name:"))
        right_vbox.addWidget(self.team_name)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_team)
        right_vbox.addWidget(save_button)

        switch_encoding_button = QPushButton("Switch Encoding")
        switch_encoding_button.clicked.connect(self.switch_encoding)
        right_vbox.addWidget(switch_encoding_button)

        right_vbox.addStretch(1)

    def team_selected(self, item):
        self.team_idx = self.teams_tree_view.indexOfTopLevelItem(item)
        self.refresh()

    def save_team(self):

        self.team_name.setStyleSheet("background-color: white;")

        self.teams[self.team_idx]['team_name'] = file_reader.encode_string(
            self.team_name.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'

        if len(self.teams[self.team_idx]['team_name']) > 0x22:
            self.teams[self.team_idx]['team_name'] = self.teams[self.team_idx]['team_name'][:0x20] \
                                                     + b'\xFF' + b'\xFF'
            self.team_name.setStyleSheet("background-color: red;")

        self.rival_file.write_teams(self.teams)
        self.teams_tree_view.topLevelItem(self.team_idx).setText(0, self.team_name.text())
        self.teams_tree_view.itemFromIndex(self.teams_tree_view.selectedIndexes()[0]) \
            .setBackground(0, QBrush(QColor(0, 255, 0)))

    def switch_encoding(self):
        temp = self.encoding
        self.encoding = self.mod_encoding
        self.mod_encoding = temp
        self.refresh()

    def refresh(self):
        self.team_name.setText(
            file_reader.decode_string(self.teams[self.team_idx]['team_name'], self.encoding).strip('\x00')
            .replace("$", " "))
