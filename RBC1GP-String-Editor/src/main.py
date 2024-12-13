# a quick dirty conversion of my txr3 text editor to handle C1GP
# files that have no offsets

import sys

from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import QDialogButtonBox
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QTabWidget
from PyQt6.QtWidgets import QStyle, QVBoxLayout, QDialog, QFileDialog, QWidget, QHBoxLayout

import bad_tab
import events_tab
import file_reader
import rivals_tab
import teams_tab

var_rivals_tab = None
var_teams_tab = None
var_events_tab = None
var_bad_tab = None


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

        self.hex_le_field = QLineEdit(self)
        self.layout.addWidget(self.hex_le_field)  # hex but in little endian

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)
        self.layout.addWidget(self.button_box)

    def change_hex_field(self):
        text = self.text_field.text()
        encoded_bytes = file_reader.encode_string(text.replace(" ", "$"), self.table)

        hex_str = encoded_bytes.hex().upper()
        hex_str = ' '.join([hex_str[i:i + 4] for i in range(0, len(hex_str), 4)])
        self.hex_field.setText(hex_str + " FFFF")

        hex_str = encoded_bytes[::-1].hex().upper()
        hex_str = ' '.join([hex_str[i:i + 4] for i in range(0, len(hex_str), 4)])
        self.hex_le_field.setText("FFFF " + hex_str)


class StartupDialog(QDialog):
    def __init__(self, icon):
        super().__init__()
        self.mainWidget = QWidget()
        self.setWindowTitle("RB:C1GP Text Editor")
        self.setWindowIcon(icon)
        self.setGeometry(100, 100, 600, 200)

        self.title_label = QLabel("RB:C1GP Text Editor")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;"
                                       "color:  #2e2e2e;background-color: #bababa;")
        self.dat1_label = QLabel("210.bin")
        self.dat2_label = QLabel("211.bin")
        self.dat3_label = QLabel("212.bin")
        self.dat1_field = QLineEdit()
        self.dat2_field = QLineEdit()
        self.dat3_field = QLineEdit()
        self.dat1_button = QPushButton("Browse...")
        self.dat2_button = QPushButton("Browse...")
        self.dat3_button = QPushButton("Browse...")
        self.accept_button = QPushButton("OK")
        self.accept_button.setEnabled(False)

        self.dat1_layout = QHBoxLayout()
        self.dat2_layout = QHBoxLayout()
        self.dat3_layout = QHBoxLayout()
        self.dat1_layout.addWidget(self.dat1_label)
        self.dat1_layout.addWidget(self.dat1_field)
        self.dat1_layout.addWidget(self.dat1_button)
        self.dat2_layout.addWidget(self.dat2_label)
        self.dat2_layout.addWidget(self.dat2_field)
        self.dat2_layout.addWidget(self.dat2_button)
        self.dat3_layout.addWidget(self.dat3_label)
        self.dat3_layout.addWidget(self.dat3_field)
        self.dat3_layout.addWidget(self.dat3_button)

        self.dat1_button.clicked.connect(lambda: self.open_file_dialog(self.dat1_field))
        self.dat2_button.clicked.connect(lambda: self.open_file_dialog(self.dat2_field))
        self.dat3_button.clicked.connect(lambda: self.open_file_dialog(self.dat3_field))
        self.dat1_field.textChanged.connect(self.check_fields)
        self.dat2_field.textChanged.connect(self.check_fields)
        self.dat3_field.textChanged.connect(self.check_fields)
        self.accept_button.clicked.connect(self.accept)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.title_label)
        self.layout().addLayout(self.dat1_layout)
        self.layout().addLayout(self.dat2_layout)
        self.layout().addLayout(self.dat3_layout)
        self.layout().addWidget(self.accept_button)

        made_by = QLabel("warning: very long loading due to processing data with custom encoder")
        made_by.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(made_by)

    def open_file_dialog(self, dat_field):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open .bin file', '', 'BIN Files (*.bin)')
        dat_field.setText(file_name)

    def check_fields(self):
        if self.dat1_field.text():
            self.accept_button.setEnabled(True)
        else:
            self.accept_button.setEnabled(False)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        sys.exit(0)

    def accept(self):
        global var_rivals_tab, var_events_tab, var_bad_tab, var_teams_tab
        rivals_file = file_reader.RivalFile(self.dat1_field.text())
        events_file = file_reader.EventFile(self.dat2_field.text())
        bad_file = file_reader.BADFile(self.dat3_field.text())
        var_rivals_tab = rivals_tab.RivalsTab(rivals_file)
        var_teams_tab = teams_tab.TeamsTab(rivals_file)
        var_events_tab = events_tab.EventsTab(events_file)
        var_bad_tab = bad_tab.BADTab(bad_file)
        super().accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        _, self.mod_decoding_table = file_reader.load_encoding_table('resources//modified.tbl')
        self.menu_bar = self.menuBar()
        self.status_bar = self.statusBar()
        self.setWindowTitle("RB:C1GP Text Editor")
        pixmap = QStyle.StandardPixmap.SP_FileDialogContentsView
        icon = self.style().standardIcon(pixmap)

        self.tab_widget = QTabWidget()

        self.setCentralWidget(self.tab_widget)
        self.setWindowIcon(icon)
        self.setGeometry(100, 100, 800, 600)

        self.startup_dialog = StartupDialog(icon)
        self.startup_dialog.exec()
        if self.startup_dialog.result() == QDialog.DialogCode.Accepted:
            self.tab_widget.addTab(var_rivals_tab, "Rivals")
            self.tab_widget.addTab(var_teams_tab, "Teams")
            self.tab_widget.addTab(var_events_tab, "Events")
            self.tab_widget.addTab(var_bad_tab, "B.A.D.")

        self.menu_bar_setup()

    def menu_bar_setup(self):
        file_menu = self.menu_bar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        encode_menu = self.menu_bar.addMenu("Encode")
        encode_action = encode_menu.addAction("Encode Text")
        encode_action.triggered.connect(ConvertDialog(self.mod_decoding_table, self).exec)


def run_app():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_app()
