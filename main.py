#main.py
import sys
from PySide6.QtWidgets import QApplication
from gui import PesquisaCPF
from model import DataModel
from PySide6.QtGui import QIcon


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))
    df = DataModel.carregar_base()
    window = PesquisaCPF(DataModel.search_logic, DataModel.clear_logic, df)
    window.show()
    sys.exit(app.exec())