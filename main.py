import sys
from PyQt5.QtWidgets import QApplication
from gui import PesquisaCPF
from PesquisaCPF import search_logic, clear_logic

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PesquisaCPF(search_logic, clear_logic)
    window.show()
    sys.exit(app.exec())