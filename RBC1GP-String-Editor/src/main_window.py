import os
import file_parser
import popup_window

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt6.QtWidgets import QStyle
from PyQt6.QtWidgets import QFileDialog

from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow):

    def menu_bar_setup(self):
        # Menu bar
        self.menu_bar = self.menuBar()

        # File menu
        self.file_menu = self.menu_bar.addMenu("File")

        # Open action
        self.open_action = self.file_menu.addAction("Open without offsets")
        self.open_action.triggered.connect(self.open_file)

        # Open with offsets action
        self.open_action = self.file_menu.addAction("Open with offsets")
        self.open_action.triggered.connect(self.open_offset_file)

        # Save action
        self.save_action = self.file_menu.addAction("Save")
        self.save_action.triggered.connect(self.save_file)
        self.save_action.setEnabled(False)

        # Save as action
        self.save_as_action = self.file_menu.addAction("Save As")
        self.save_as_action.triggered.connect(self.save_as_file)
        self.save_as_action.setEnabled(False)

        # Separator
        self.file_menu.addSeparator()

        # Exit action
        self.exit_action = self.file_menu.addAction("Exit")
        self.exit_action.triggered.connect(self.close)
        

        # Tools menu
        self.tools_menu = self.menu_bar.addMenu("Tools")

        # Encode text action
        self.text_hex_action = self.tools_menu.addAction("Encode text")
        self.text_hex_action.triggered.connect(popup_window.ConvertDialog(self.decoding_table, self).exec)

        # Find action
        self.find_action = self.tools_menu.addAction("Find")
        self.find_action.triggered.connect(popup_window.FindDialog(self.table_widget, self.status_bar, self).exec)



    def __init__(self):
        super().__init__()
        self.setWindowTitle("RBC1GP String Editor")

        pixmapi = QStyle.StandardPixmap.SP_FileDialogContentsView
        icon = self.style().standardIcon(pixmapi)

        self.setWindowIcon(icon)
        self.setGeometry(100, 100, 800, 600)

        # Encoding table
        tbl_path = os.path.join(os.path.dirname(__file__), "resources", "c1gp.tbl")
        self.encoding_table, self.decoding_table = file_parser.load_encoding_table(tbl_path)

        self.offsets_available = False
        self.current_file_data = None

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Table widget
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Status bar 
        self.status_bar = self.statusBar()

        # Menu bar setup
        self.menu_bar_setup()

    def open_file(self):
        if self.current_file_data != None:
            self.reset_file()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file with no defined offsets', '', 'All Files (*)')
        self.status_bar.showMessage(f"Processing {file_name}...")
        if file_name:
            data = file_parser.read_file(file_name)
            self.current_file_data = data
            string_locations = file_parser.find_strings_with_terminator(data)
            strings = file_parser.read_strings(data, string_locations, self.encoding_table, True)
            self.table_widget.setRowCount(len(strings))
            self.table_widget.setColumnCount(4)
            self.table_widget.setHorizontalHeaderLabels(['Hex Offset', 'String', 'Decoded Hex', 'Length'])
            for row, string in enumerate(strings):
                self.table_widget.setItem(row, 0, QTableWidgetItem(hex(string_locations[row][0])))
                self.table_widget.setItem(row, 1, QTableWidgetItem(string))
                decoded_hex = data[string_locations[row][0]:string_locations[row][1]].hex().upper()
                self.table_widget.setItem(row, 2, QTableWidgetItem(decoded_hex))
                self.table_widget.setItem(row, 3, QTableWidgetItem(str(len(decoded_hex)//4)))
            self.save_action.setEnabled(True)
            self.save_as_action.setEnabled(True)
            self.status_bar.showMessage(f"File {file_name} opened successfully.")

            self.table_widget.cellDoubleClicked.connect(self.edit_string)

    def open_offset_file(self):
        if self.current_file_data != None:
            self.reset_file()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file with defined offsets', '', 'All Files (*)')
        self.status_bar.showMessage(f"Processing {file_name}...")
        if file_name:
            data = file_parser.read_file(file_name)
            self.current_file_data = data
            string_locations = file_parser.read_string_locations(data)
            strings = file_parser.read_strings(data, string_locations, self.encoding_table, False)
            self.table_widget.setRowCount(len(strings))
            self.table_widget.setColumnCount(4)
            self.table_widget.setHorizontalHeaderLabels(['Hex Offset', 'String', 'Decoded Hex', 'Length'])
            for row, string in enumerate(strings):
                self.table_widget.setItem(row, 0, QTableWidgetItem(hex(string_locations[row][0])))
                self.table_widget.setItem(row, 1, QTableWidgetItem(string))
                decoded_hex = data[string_locations[row][0]:string_locations[row][1]].hex().upper()
                self.table_widget.setItem(row, 2, QTableWidgetItem(decoded_hex))
                self.table_widget.setItem(row, 3, QTableWidgetItem(str(len(decoded_hex)//4)))
            self.save_action.setEnabled(True)
            self.save_as_action.setEnabled(True)
            self.status_bar.showMessage(f"File {file_name} opened successfully.")
            self.offsets_available = True
            
            self.table_widget.cellDoubleClicked.connect(self.edit_string)

    def save_file(self):
        pass

    def save_as_file(self):
        new_file_name, _ = QFileDialog.getSaveFileName(self, 'Save file', '', 'All Files (*)')
        string_locations = []
        strings = []
        if new_file_name:
            for row in range(self.table_widget.rowCount()):
                hex_offset = int(self.table_widget.item(row, 0).text(), 16)
                string = self.table_widget.item(row, 1).text()
                decoded_hex = self.table_widget.item(row, 2).text()
                string_locations.append((hex_offset, hex_offset + len(decoded_hex)//2))
                strings.append(string)

            if self.offsets_available:
                new_data = file_parser.write_offsets_strings(self.current_file_data, string_locations, strings)
            else:
                new_data = file_parser.write_strings(self.current_file_data, string_locations, strings)
            with open(new_file_name, 'wb') as f:
                f.write(new_data)
            self.status_bar.showMessage(f"File saved as {new_file_name}.")
            self.current_file_data = new_data
        
    def reset_file(self):
        self.table_widget.clear()
        self.table_widget.cellDoubleClicked.disconnect()
        self.save_action.setEnabled(False)
        self.save_as_action.setEnabled(False)
        self.offsets_available = False
        self.current_file_data = None
        self.status_bar.showMessage("File closed.")
        

    def closeEvent(self, event):
        event.accept()

    def edit_string(self, row, column):
        if column == 1:
            popup_window.EditDialog(self.table_widget, row, self.encoding_table, self.decoding_table, self).exec()