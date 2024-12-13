from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QLineEdit, QLabel, QPushButton
from PyQt6.QtWidgets import QWidget, QTreeWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QTreeWidgetItem

import file_reader


class BADTab(QWidget):
    def __init__(self, bad_file: file_reader.BADFile):
        super().__init__()
        self.bad_idx = 0
        self.bad_file = bad_file
        self.bad_tree_view = QTreeWidget()

        self.encoding, self.decoding = file_reader.load_encoding_table('resources//c1gp.tbl')
        self.mod_encoding, self.mod_decoding = file_reader.load_encoding_table('resources//modified.tbl')

        self.bad_names_0, self.bad_names_1 = bad_file.get_bad()
        self.bad_line_0 = QLineEdit()
        self.bad_line_1 = QLineEdit()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setup_layout()

        # self.reset()

    def setup_layout(self):
        left_vbox = QVBoxLayout()
        tree_scroll_area = QScrollArea()
        self.bad_tree_view.setHeaderHidden(True)
        tree_scroll_area.setWidget(self.bad_tree_view)
        tree_scroll_area.setWidgetResizable(True)
        left_vbox.addWidget(tree_scroll_area)
        tree_scroll_area.setMaximumWidth(225)
        self.layout.addLayout(left_vbox)

        for bad in self.bad_names_0:
            for block in bad['blocks']:
                item = QTreeWidgetItem([file_reader.decode_string(block['name0'], self.encoding).strip('\x00') + '\t' +
                                        file_reader.decode_string(block['name1'], self.encoding).strip('\x00')])
                self.bad_tree_view.addTopLevelItem(item)

        for bad in self.bad_names_1:
            item = QTreeWidgetItem([file_reader.decode_string(bad['name'], self.encoding).strip('\x00')])
            self.bad_tree_view.addTopLevelItem(item)

        self.bad_tree_view.itemClicked.connect(self.bad_selected)

        right_vbox = QVBoxLayout()
        self.layout.addLayout(right_vbox)

        right_vbox.addWidget(QLabel("B.A.D. name 1:"))
        right_vbox.addWidget(self.bad_line_0)
        right_vbox.addWidget(QLabel("B.A.D. name 2:"))
        right_vbox.addWidget(self.bad_line_1)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_bad)
        right_vbox.addWidget(save_button)

        switch_encoding_button = QPushButton("Switch Encoding")
        switch_encoding_button.clicked.connect(self.switch_encoding)
        right_vbox.addWidget(switch_encoding_button)

        right_vbox.addStretch(1)

    def bad_selected(self, item):
        self.bad_idx = self.bad_tree_view.indexOfTopLevelItem(item)
        block_id = self.bad_idx // 5
        if block_id < len(self.bad_names_0):
            self.bad_line_1.setDisabled(False)
            self.bad_line_0.setText(
                file_reader.decode_string(self.bad_names_0[block_id]['blocks'][self.bad_idx % 5]['name0'],
                                          self.encoding).strip('\x00').replace("$", " "))
            self.bad_line_1.setText(
                file_reader.decode_string(self.bad_names_0[block_id]['blocks'][self.bad_idx % 5]['name1'],
                                          self.encoding).strip('\x00').replace("$", " "))
        else:
            self.bad_line_1.setDisabled(True)
            self.bad_line_0.setText(
                file_reader.decode_string(self.bad_names_1[self.bad_idx - (30 * 5)]['name'],
                                          self.encoding).strip('\x00').replace("$", " "))
            self.bad_line_1.setText("")

    def save_bad(self):

        self.bad_line_0.setStyleSheet("background-color: white;")
        self.bad_line_1.setStyleSheet("background-color: white;")
        block_id = self.bad_idx // 5

        if block_id < len(self.bad_names_0):
            self.bad_names_0[block_id]['blocks'][self.bad_idx % 5]['name0'] = file_reader.encode_string(
                self.bad_line_0.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
            self.bad_names_0[block_id]['blocks'][self.bad_idx % 5]['name1'] = file_reader.encode_string(
                self.bad_line_1.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'

            if len(self.bad_names_0[block_id]['blocks'][self.bad_idx % 5]['name0']) > 0x0E:
                self.bad_line_0.setStyleSheet("background-color: red;")
                self.bad_names_0[block_id]['blocks'][self.bad_idx % 5]['name0']\
                    = self.bad_names_0[block_id]['blocks'][self.bad_idx % 5]['name0'][:0x0C] + b'\xFF\xFF'

            if len(self.bad_names_0[block_id]['blocks'][self.bad_idx % 5]['name1']) > 0x0E:
                self.bad_line_1.setStyleSheet("background-color: red;")
                self.bad_names_0[block_id]['blocks'][self.bad_idx % 5]['name1']\
                    = self.bad_names_0[block_id]['blocks'][self.bad_idx % 5]['name1'][:0x0C] + b'\xFF\xFF'
        else:
            self.bad_names_1[self.bad_idx - (30 * 5)]['name'] = file_reader.encode_string(
                self.bad_line_0.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'

            if len(self.bad_names_1[self.bad_idx - (30 * 5)]['name']) > 0x1A:
                self.bad_line_0.setStyleSheet("background-color: red;")
                self.bad_names_1[self.bad_idx - (30 * 5)]['name']\
                    = self.bad_names_1[self.bad_idx - (30 * 5)]['name'][:0x18] + b'\xFF\xFF'

        self.bad_file.write_bad(self.bad_names_0, self.bad_names_1)
        self.bad_tree_view.topLevelItem(self.bad_idx).setText(0, self.bad_line_0.text() + '\t' + self.bad_line_1.text())
        self.bad_tree_view.itemFromIndex(self.bad_tree_view.selectedIndexes()[0])\
            .setBackground(0, QBrush(QColor(0, 255, 0)))

    def switch_encoding(self):
        temp = self.encoding
        self.encoding = self.mod_encoding
        self.mod_encoding = temp
        self.bad_selected(self.bad_tree_view.topLevelItem(self.bad_idx))
            
