# a quick dirty conversion of my txr3 text editor to handle C1GP
# files that have no offsets

import sys

import rivals_tab
import teams_tab
import events_tab

import file_reader

from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QTabWidget, QMessageBox
from PyQt6.QtWidgets import QStyle, QVBoxLayout, QDialog, QFileDialog, QWidget, QHBoxLayout

var_rivals_tab = None
var_teams_tab = None
var_events_tab = None
var_bad_tab = None


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

        made_by = QLabel("warning: slow as hell due to custom encoding/decoding")
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
        # bad_file = file_reader.BADFile(self.dat3_field.text())
        var_rivals_tab = rivals_tab.RivalsTab(rivals_file)
        var_teams_tab = teams_tab.TeamsTab(rivals_file)
        var_events_tab = events_tab.EventsTab(events_file)
        super().accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

        self.menu_bar_setup()

    def menu_bar_setup(self):
        file_menu = self.menu_bar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)


def run_app():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_app()
