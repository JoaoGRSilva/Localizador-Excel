import sys
from PySide6.QtWidgets import QApplication
from gui import PesquisaCPF
from backend import search_logic, clear_logic, df, update_logic
from PySide6.QtGui import QIcon


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))
    window = PesquisaCPF(search_logic, clear_logic, update_logic)
    window.show()
    sys.exit(app.exec())