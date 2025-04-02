import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from gui import PesquisaCPF
from model import DataModel

if __name__ == '__main__':

    print(f"Diretório atual: {os.getcwd()}")
    print(f"Lista de arquivos no diretório: {os.listdir()}")
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))
    

    model = DataModel()

    window = PesquisaCPF(model)
    window.show()
    
    sys.exit(app.exec())