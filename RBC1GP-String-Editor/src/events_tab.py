from PyQt6.QtWidgets import QLineEdit, QLabel, QPushButton
from PyQt6.QtWidgets import QWidget, QTreeWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QTreeWidgetItem

import file_parser
import file_reader


class EventsTab(QWidget):
    def __init__(self, event_file: file_reader.EventFile):
        super().__init__()
        self.event_idx = 0
        self.event_file = event_file
        self.event_tree_view = QTreeWidget()

        self.encoding, self.decoding = file_parser.load_encoding_table('resources//c1gp.tbl')
        self.mod_encoding, self.mod_decoding = file_parser.load_encoding_table('resources//modified.tbl')

        self.events = event_file.get_events()
        self.event_name = QLineEdit()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setup_layout()

        # self.reset()

    def setup_layout(self):
        left_vbox = QVBoxLayout()
        tree_scroll_area = QScrollArea()
        self.event_tree_view.setHeaderHidden(True)
        tree_scroll_area.setWidget(self.event_tree_view)
        tree_scroll_area.setWidgetResizable(True)
        left_vbox.addWidget(tree_scroll_area)
        tree_scroll_area.setMaximumWidth(175)
        self.layout.addLayout(left_vbox)

        for event in self.events:
            # print(file_parser.decode_string(rival['nickname'], encoding).strip('\x00'))
            item = QTreeWidgetItem([file_parser.decode_string(event['event_name'], self.encoding).strip('\x00')])
            self.event_tree_view.addTopLevelItem(item)

        self.event_tree_view.itemClicked.connect(self.rival_selected)

        right_vbox = QVBoxLayout()
        self.layout.addLayout(right_vbox)

        right_vbox.addWidget(QLabel("Event name:"))
        right_vbox.addWidget(self.event_name)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_event)
        right_vbox.addWidget(save_button)

        switch_encoding_button = QPushButton("Switch Encoding")
        switch_encoding_button.clicked.connect(self.switch_encoding)
        right_vbox.addWidget(switch_encoding_button)

        right_vbox.addStretch(1)

    def rival_selected(self, item):
        self.event_idx = self.event_tree_view.indexOfTopLevelItem(item)
        self.event_name.setText(
            file_parser.decode_string(self.events[self.event_idx]['event_name'], self.encoding).strip('\x00'))

    def save_event(self):

        self.event_name.setStyleSheet("background-color: white;")

        self.events[self.event_idx]['event_name'] = file_parser.encode_string(
            self.event_name.text(), self.mod_decoding) + b'\xFF' + b'\xFF'

        if len(self.events[self.event_idx]['event_name']) > 0x1C:
            self.events[self.event_idx]['event_name'] = self.events[self.event_idx]['event_name'][:0x1A] \
                                                       + b'\xFF' + b'\xFF'
            self.event_name.setStyleSheet("background-color: red;")

        self.event_file.write_events(self.events)

    def switch_encoding(self):
        temp = self.encoding
        self.encoding = self.mod_encoding
        self.mod_encoding = temp
        self.refresh()

    def refresh(self):
        self.event_name.setText(
            file_parser.decode_string(self.events[self.event_idx]['event_name'], self.encoding).strip('\x00'))
