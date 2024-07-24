import sys
import main_window

from PyQt6.QtWidgets import QApplication

def run_app():
    app = QApplication(sys.argv)
    window = main_window.MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    run_app()