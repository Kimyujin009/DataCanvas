import sys

from PySide6.QtWidgets import QApplication

from .app import DataCanvasWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("DataCanvas")
    window = DataCanvasWindow()
    window.show()
    sys.exit(app.exec())
