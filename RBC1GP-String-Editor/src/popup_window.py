import file_parser

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtWidgets import QCheckBox

from PyQt6.QtCore import Qt

class EditDialog(QDialog):
    def __init__(self, table_widget, row, encoding_table, decoding_table, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Edit Text')
        self.setGeometry(100, 100, 400, 100)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table_widget = table_widget
        self.row = row
        self.encoding_table = encoding_table
        self.decoding_table = decoding_table

        self.add_terminator = False

        self.text_label = QLabel('Text:')
        self.layout.addWidget(self.text_label)

        self.text_field = QLineEdit(self)
        self.layout.addWidget(self.text_field)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.edit_text)
        self.button_box.accepted.connect(self.accept)
        self.layout.addWidget(self.button_box)

        self.add_terminator_checkbox = QCheckBox('Add 0xFFFF terminator')
        self.layout.addWidget(self.add_terminator_checkbox)
        self.add_terminator_checkbox.stateChanged.connect(self.toggle_terminator)

    def edit_text(self):
        text = self.text_field.text()
        decoded_hex = file_parser.encode_string(text, self.decoding_table) + 'FFFF' if self.add_terminator else file_parser.encode_string(text, self.decoding_table)
        decoded_hex = decoded_hex.upper()
        self.table_widget.setItem(self.row, 1, QTableWidgetItem(text))
        self.table_widget.setItem(self.row, 2, QTableWidgetItem(decoded_hex))
        new_length = len(decoded_hex)//4
        old_length = int(self.table_widget.item(self.row, 3).text())
        if new_length > old_length:
            for i in range(self.row+1, self.table_widget.rowCount()):
                hex_offset = self.table_widget.item(i, 0).text()
                new_offset = int(hex_offset, 16) + (new_length - old_length) * 2
                self.table_widget.setItem(i, 0, QTableWidgetItem(hex(new_offset)))
        
        self.table_widget.setItem(self.row, 3, QTableWidgetItem(str(new_length)))

    def toggle_terminator(self):
        self.add_terminator = not self.add_terminator

    
class ConvertDialog(QDialog):
    def __init__(self, decoding_table, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Encode Text')
        self.setGeometry(100, 100, 400, 100)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = decoding_table

        self.text_label = QLabel('Text:')
        self.layout.addWidget(self.text_label)

        self.text_field = QLineEdit(self)
        self.layout.addWidget(self.text_field)
        self.text_field.textChanged.connect(self.change_hex_field)

        self.hex_label = QLabel('Hex:')
        self.layout.addWidget(self.hex_label)

        self.hex_field = QLineEdit(self)
        self.layout.addWidget(self.hex_field)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        self.layout.addWidget(self.button_box)

    def change_hex_field(self):
        text = self.text_field.text()
        encoded_bytes = file_parser.encode_string(text, self.table)
        self.hex_field.setText(encoded_bytes.upper())

class FindDialog(QDialog):
    def __init__(self, table_widget, status_bar, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Find')
        self.setGeometry(100, 100, 400, 100)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table_widget = table_widget
        self.status_bar = status_bar

        self.text_label = QLabel('Text:')
        self.layout.addWidget(self.text_label)

        self.text_field = QLineEdit(self)
        self.layout.addWidget(self.text_field)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.find_text)
        self.button_box.accepted.connect(self.accept)
        self.layout.addWidget(self.button_box)

    def find_text(self):
        text = self.text_field.text()
        matching = self.table_widget.findItems(text, Qt.MatchFlag.MatchContains)
        if matching:
            for item in matching:
                item.setSelected(True)
                self.table_widget.scrollToItem(item)
        else:
            self.status_bar.showMessage('Text not found', 2000)