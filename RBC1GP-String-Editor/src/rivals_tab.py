from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QLineEdit, QLabel, QPushButton
from PyQt6.QtWidgets import QWidget, QTreeWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QTreeWidgetItem

import file_reader


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)


class RivalsTab(QWidget):
    def __init__(self, rival_file: file_reader.RivalFile):
        super().__init__()
        self.rival_idx = 0
        self.region_idx = 0
        self.rival_file = rival_file
        self.rivals_tree_view = QTreeWidget()

        self.encoding, self.decoding = file_reader.load_encoding_table('resources//c1gp.tbl')
        self.mod_encoding, self.mod_decoding = file_reader.load_encoding_table('resources//modified.tbl')

        self.rival_lines = rival_file.get_rivals()
        self.rival_nickname = QLineEdit()
        self.rival_nickname_hex = QLineEdit()
        self.rival_name = QLineEdit()
        self.rival_occupation = QLineEdit()
        self.rival_motto = QLineEdit()
        self.rival_profile_bio_1 = QLineEdit()
        self.rival_profile_bio_2 = QLineEdit()
        self.rival_profile_bio_3 = QLineEdit()
        self.rival_profile_bio_4 = QLineEdit()
        self.rival_profile_bio_5 = QLineEdit()
        self.rival_dialog_1 = QLineEdit()
        self.rival_dialog_2 = QLineEdit()
        self.rival_dialog_3 = QLineEdit()
        self.rival_dialog_4 = QLineEdit()
        self.rival_dialog_5 = QLineEdit()
        self.rival_dialog_6 = QLineEdit()
        self.rival_dialog_short_1 = QLineEdit()
        self.rival_dialog_short_2 = QLineEdit()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setup_layout()

        # self.reset()
        # write_rivals_to_json(self, self.rival_lines, 'rivals.json')

    def setup_layout(self):
        left_vbox = QVBoxLayout()
        tree_scroll_area = QScrollArea()
        self.rivals_tree_view.setHeaderHidden(True)
        tree_scroll_area.setWidget(self.rivals_tree_view)
        tree_scroll_area.setWidgetResizable(True)
        left_vbox.addWidget(tree_scroll_area)
        tree_scroll_area.setMaximumWidth(175)
        self.layout.addLayout(left_vbox)

        for rival in self.rival_lines:
            # print(file_reader.decode_string(rival['nickname'], encoding).strip('\x00'))
            item = QTreeWidgetItem([file_reader.decode_string(rival['nickname'], self.encoding).strip('\x00')])
            self.rivals_tree_view.addTopLevelItem(item)

        self.rivals_tree_view.itemClicked.connect(self.rival_selected)

        right_vbox = QVBoxLayout()
        self.layout.addLayout(right_vbox)

        right_vbox.addWidget(QLabel("Rival Nickname:"))
        right_vbox.addWidget(self.rival_nickname)
        right_vbox.addWidget(QLabel("Rival Name:"))
        right_vbox.addWidget(self.rival_name)
        right_vbox.addWidget(QLabel("Rival Occupation:"))
        right_vbox.addWidget(self.rival_occupation)
        right_vbox.addWidget(QLabel("Rival Motto:"))
        right_vbox.addWidget(self.rival_motto)
        right_vbox.addWidget(QHLine())
        right_vbox.addWidget(QLabel("Rival Profile Bio 1:"))
        right_vbox.addWidget(self.rival_profile_bio_1)
        right_vbox.addWidget(QLabel("Rival Profile Bio 2:"))
        right_vbox.addWidget(self.rival_profile_bio_2)
        right_vbox.addWidget(QLabel("Rival Profile Bio 3:"))
        right_vbox.addWidget(self.rival_profile_bio_3)
        right_vbox.addWidget(QLabel("Rival Profile Bio 4:"))
        right_vbox.addWidget(self.rival_profile_bio_4)
        right_vbox.addWidget(QLabel("Rival Profile Bio 5:"))
        right_vbox.addWidget(self.rival_profile_bio_5)
        right_vbox.addWidget(QHLine())
        right_vbox.addWidget(QLabel("Rival Dialog Short 1:"))
        right_vbox.addWidget(self.rival_dialog_short_1)
        right_vbox.addWidget(QLabel("Rival Dialog 1:"))
        right_vbox.addWidget(self.rival_dialog_1)
        right_vbox.addWidget(QLabel("Rival Dialog 2:"))
        right_vbox.addWidget(self.rival_dialog_2)
        right_vbox.addWidget(QLabel("Rival Dialog 3:"))
        right_vbox.addWidget(self.rival_dialog_3)
        right_vbox.addWidget(QHLine())
        right_vbox.addWidget(QLabel("Rival Dialog Short 2:"))
        right_vbox.addWidget(self.rival_dialog_short_2)
        right_vbox.addWidget(QLabel("Rival Dialog 4:"))
        right_vbox.addWidget(self.rival_dialog_4)
        right_vbox.addWidget(QLabel("Rival Dialog 5:"))
        right_vbox.addWidget(self.rival_dialog_5)
        right_vbox.addWidget(QLabel("Rival Dialog 6:"))
        right_vbox.addWidget(self.rival_dialog_6)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_rival)
        right_vbox.addWidget(save_button)

        switch_encoding_button = QPushButton("Switch Encoding")
        switch_encoding_button.clicked.connect(self.switch_encoding)
        right_vbox.addWidget(switch_encoding_button)

        right_vbox.addStretch(1)

    def rival_selected(self, item):
        self.rival_idx = self.rivals_tree_view.indexOfTopLevelItem(item)
        self.refresh()

    def save_rival(self):
        # this has to be the ugliest code ive ever written in my life

        self.rival_nickname.setStyleSheet("background-color: white;")
        self.rival_name.setStyleSheet("background-color: white;")
        self.rival_occupation.setStyleSheet("background-color: white;")
        self.rival_motto.setStyleSheet("background-color: white;")
        self.rival_profile_bio_1.setStyleSheet("background-color: white;")
        self.rival_profile_bio_2.setStyleSheet("background-color: white;")
        self.rival_profile_bio_3.setStyleSheet("background-color: white;")
        self.rival_profile_bio_4.setStyleSheet("background-color: white;")
        self.rival_profile_bio_5.setStyleSheet("background-color: white;")
        self.rival_dialog_1.setStyleSheet("background-color: white;")
        self.rival_dialog_2.setStyleSheet("background-color: white;")
        self.rival_dialog_3.setStyleSheet("background-color: white;")
        self.rival_dialog_4.setStyleSheet("background-color: white;")
        self.rival_dialog_5.setStyleSheet("background-color: white;")
        self.rival_dialog_6.setStyleSheet("background-color: white;")
        self.rival_dialog_short_1.setStyleSheet("background-color: white;")
        self.rival_dialog_short_2.setStyleSheet("background-color: white;")

        self.rival_lines[self.rival_idx]['nickname'] = file_reader.encode_string(
            self.rival_nickname.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['name'] = file_reader.encode_string(
            self.rival_name.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['occupation'] = file_reader.encode_string(
            self.rival_occupation.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['motto'] = file_reader.encode_string(
            self.rival_motto.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['profile_bio_1'] = file_reader.encode_string(
            self.rival_profile_bio_1.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['profile_bio_2'] = file_reader.encode_string(
            self.rival_profile_bio_2.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['profile_bio_3'] = file_reader.encode_string(
            self.rival_profile_bio_3.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['profile_bio_4'] = file_reader.encode_string(
            self.rival_profile_bio_4.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['profile_bio_5'] = file_reader.encode_string(
            self.rival_profile_bio_5.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['dialog_1'] = file_reader.encode_string(
            self.rival_dialog_1.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['dialog_2'] = file_reader.encode_string(
            self.rival_dialog_2.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['dialog_3'] = file_reader.encode_string(
            self.rival_dialog_3.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['dialog_4'] = file_reader.encode_string(
            self.rival_dialog_4.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['dialog_5'] = file_reader.encode_string(
            self.rival_dialog_5.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['dialog_6'] = file_reader.encode_string(
            self.rival_dialog_6.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['dialog_short_1'] = file_reader.encode_string(
            self.rival_dialog_short_1.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'
        self.rival_lines[self.rival_idx]['dialog_short_2'] = file_reader.encode_string(
            self.rival_dialog_short_2.text().replace(" ", "$"), self.mod_decoding) + b'\xFF' + b'\xFF'

        if len(self.rival_lines[self.rival_idx]['nickname']) > 0x1A:
            self.rival_lines[self.rival_idx]['nickname'] = self.rival_lines[self.rival_idx]['nickname'][:0x18] \
                                                           + b'\xFF' + b'\xFF'
            self.rival_nickname.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['name']) > 0x1A:
            self.rival_lines[self.rival_idx]['name'] = self.rival_lines[self.rival_idx]['name'][:0x18] \
                                                       + b'\xFF' + b'\xFF'
            self.rival_name.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['occupation']) > 0x22:
            self.rival_lines[self.rival_idx]['occupation'] = self.rival_lines[self.rival_idx]['occupation'][:0x20] \
                                                             + b'\xFF' + b'\xFF'
            self.rival_occupation.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['motto']) > 0x22:
            self.rival_lines[self.rival_idx]['motto'] = self.rival_lines[self.rival_idx]['motto'][:0x20] \
                                                        + b'\xFF' + b'\xFF'
            self.rival_motto.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['profile_bio_1']) > 0x42:
            self.rival_lines[self.rival_idx]['profile_bio_1'] \
                = self.rival_lines[self.rival_idx]['profile_bio_1'][:0x40] + b'\xFF' + b'\xFF'
            self.rival_profile_bio_1.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['profile_bio_2']) > 0x42:
            self.rival_lines[self.rival_idx]['profile_bio_2'] \
                = self.rival_lines[self.rival_idx]['profile_bio_2'][:0x40] + b'\xFF' + b'\xFF'
            self.rival_profile_bio_2.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['profile_bio_3']) > 0x42:
            self.rival_lines[self.rival_idx]['profile_bio_3'] \
                = self.rival_lines[self.rival_idx]['profile_bio_3'][:0x40] + b'\xFF' + b'\xFF'
            self.rival_profile_bio_3.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['profile_bio_4']) > 0x42:
            self.rival_lines[self.rival_idx]['profile_bio_4'] \
                = self.rival_lines[self.rival_idx]['profile_bio_4'][:0x40] + b'\xFF' + b'\xFF'
            self.rival_profile_bio_4.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['profile_bio_5']) > 0x42:
            self.rival_lines[self.rival_idx]['profile_bio_5'] \
                = self.rival_lines[self.rival_idx]['profile_bio_5'][:0x40] + b'\xFF' + b'\xFF'
            self.rival_profile_bio_5.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['dialog_1']) > 0x30:
            self.rival_lines[self.rival_idx]['dialog_1'] = self.rival_lines[self.rival_idx]['dialog_1'][:0x2E] \
                                                           + b'\xFF' + b'\xFF'
            self.rival_dialog_1.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['dialog_2']) > 0x30:
            self.rival_lines[self.rival_idx]['dialog_2'] = self.rival_lines[self.rival_idx]['dialog_2'][:0x2E] \
                                                           + b'\xFF' + b'\xFF'
            self.rival_dialog_2.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['dialog_3']) > 0x30:
            self.rival_lines[self.rival_idx]['dialog_3'] = self.rival_lines[self.rival_idx]['dialog_3'][:0x2E] \
                                                           + b'\xFF' + b'\xFF'
            self.rival_dialog_3.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['dialog_4']) > 0x30:
            self.rival_lines[self.rival_idx]['dialog_4'] = self.rival_lines[self.rival_idx]['dialog_4'][:0x2E] \
                                                           + b'\xFF' + b'\xFF'
            self.rival_dialog_4.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['dialog_5']) > 0x30:
            self.rival_lines[self.rival_idx]['dialog_5'] = self.rival_lines[self.rival_idx]['dialog_5'][:0x2E] \
                                                           + b'\xFF' + b'\xFF'
            self.rival_dialog_5.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['dialog_6']) > 0x30:
            self.rival_lines[self.rival_idx]['dialog_6'] = self.rival_lines[self.rival_idx]['dialog_6'][:0x2E] \
                                                           + b'\xFF' + b'\xFF'
            self.rival_dialog_6.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['dialog_short_1']) > 0x18:
            self.rival_lines[self.rival_idx]['dialog_short_1'] = \
                self.rival_lines[self.rival_idx]['dialog_short_1'][:0x16] + b'\xFF' + b'\xFF'
            self.rival_dialog_short_1.setStyleSheet("background-color: red;")
        if len(self.rival_lines[self.rival_idx]['dialog_short_2']) > 0x18:
            self.rival_lines[self.rival_idx]['dialog_short_2'] = \
                self.rival_lines[self.rival_idx]['dialog_short_2'][:0x16] + b'\xFF' + b'\xFF'
            self.rival_dialog_short_2.setStyleSheet("background-color: red;")
        self.rival_file.write_rivals(self.rival_lines)
        self.rivals_tree_view.topLevelItem(self.rival_idx).setText(0, self.rival_nickname.text())
        self.rivals_tree_view.itemFromIndex(self.rivals_tree_view.selectedIndexes()[0]) \
            .setBackground(0, QBrush(QColor(0, 255, 0)))

    def switch_encoding(self):
        temp = self.encoding
        self.encoding = self.mod_encoding
        self.mod_encoding = temp
        self.refresh()

    def refresh(self):
        self.rival_nickname.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['nickname'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_name.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['name'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_occupation.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['occupation'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_motto.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['motto'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_profile_bio_1.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['profile_bio_1'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_profile_bio_2.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['profile_bio_2'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_profile_bio_3.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['profile_bio_3'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_profile_bio_4.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['profile_bio_4'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_profile_bio_5.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['profile_bio_5'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_dialog_1.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['dialog_1'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_dialog_2.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['dialog_2'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_dialog_3.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['dialog_3'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_dialog_4.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['dialog_4'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_dialog_5.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['dialog_5'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_dialog_6.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['dialog_6'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_dialog_short_1.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['dialog_short_1'], self.encoding).strip('\x00')
            .replace("$", " "))
        self.rival_dialog_short_2.setText(
            file_reader.decode_string(self.rival_lines[self.rival_idx]['dialog_short_2'], self.encoding).strip('\x00')
            .replace("$", " "))


def write_rivals_to_json(self, rivals, json_out):
    with open(json_out, 'w', encoding='utf-8') as f:
        f.write('[\n')
        for rival in rivals:
            f.write('    {\n')
            f.write('        "nickname": "{}",\n'.format(
                file_reader.decode_string(rival['nickname'], self.encoding).strip('\x00')))
            f.write(
                '        "name": "{}",\n'.format(file_reader.decode_string(rival['name'], self.encoding).strip('\x00')))
            f.write('        "occupation": "{}",\n'.format(
                file_reader.decode_string(rival['occupation'], self.encoding).strip('\x00')))
            f.write('        "motto": "{}",\n'.format(
                file_reader.decode_string(rival['motto'], self.encoding).strip('\x00')))
            f.write('        "profile_bio_1": "{}",\n'.format(
                file_reader.decode_string(rival['profile_bio_1'], self.encoding).strip('\x00')))
            f.write('        "profile_bio_2": "{}",\n'.format(
                file_reader.decode_string(rival['profile_bio_2'], self.encoding).strip('\x00')))
            f.write('        "profile_bio_3": "{}",\n'.format(
                file_reader.decode_string(rival['profile_bio_3'], self.encoding).strip('\x00')))
            f.write('        "profile_bio_4": "{}",\n'.format(
                file_reader.decode_string(rival['profile_bio_4'], self.encoding).strip('\x00')))
            f.write('        "profile_bio_5": "{}",\n'.format(
                file_reader.decode_string(rival['profile_bio_5'], self.encoding).strip('\x00')))
            f.write('        "dialog_1": "{}",\n'.format(
                file_reader.decode_string(rival['dialog_1'], self.encoding).strip('\x00')))
            f.write('        "dialog_2": "{}",\n'.format(
                file_reader.decode_string(rival['dialog_2'], self.encoding).strip('\x00')))
            f.write('        "dialog_3": "{}",\n'.format(
                file_reader.decode_string(rival['dialog_3'], self.encoding).strip('\x00')))
            f.write('        "dialog_4": "{}",\n'.format(
                file_reader.decode_string(rival['dialog_4'], self.encoding).strip('\x00')))
            f.write('        "dialog_5": "{}",\n'.format(
                file_reader.decode_string(rival['dialog_5'], self.encoding).strip('\x00')))
            f.write('        "dialog_6": "{}",\n'.format(
                file_reader.decode_string(rival['dialog_6'], self.encoding).strip('\x00')))
            f.write('        "dialog_short_1": "{}",\n'.format(
                file_reader.decode_string(rival['dialog_short_1'], self.encoding).strip('\x00')))
            f.write('        "dialog_short_2": "{}"\n'.format(
                file_reader.decode_string(rival['dialog_short_2'], self.encoding).strip('\x00')))
            f.write('    },\n')
        f.write(']\n')
    print('Rivals written to {}'.format(json_out))
