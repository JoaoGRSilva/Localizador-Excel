#gui.py
from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QTextEdit, QFileDialog, QMessageBox, QFrame)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QEvent

class PesquisaCPF(QWidget):
    def __init__(self, data_model):
        super().__init__()

        self.data_model = data_model
       
        self.setWindowIcon(QIcon("icon.ico"))
        
        self.setWindowTitle('Retenção 5D')
        self.setGeometry(100, 100, 400, 320)
        self.setFixedSize(400, 250)
        
        # Widgets existentes
        self.label_cpf = QLabel('Digite o CPF:')
        self.input_cpf = QLineEdit()
        self.button_pesquisar = QPushButton('Pesquisar')
        self.button_limpar = QPushButton('Limpar')
        self.label_oferta = QTextEdit()
        self.label_oferta.setReadOnly(True)
        
        # Linha divisória
        self.linha_divisoria = QFrame()
        self.linha_divisoria.setFrameShape(QFrame.HLine)
        self.linha_divisoria.setFrameShadow(QFrame.Sunken)
        self.linha_divisoria.setStyleSheet("background-color: gray;")
        
        # Widgets para desconto de farmácia
        self.label_farm = QLabel('Desconto farmácia:')
        self.label_ultimos3 = QLabel('Últimos 3 meses')
        self.label_total = QLabel('Total')
        
        self.label_farm3m = QLabel('')
        self.label_farm3m.setStyleSheet("background-color: #ffffff; color: #333333; font-size: 14px; border-radius: 5px; min-width: 170px; min-height: 20px; padding: 2px;")
        self.label_farm3m.setAlignment(Qt.AlignCenter)
        
        self.label_total_valor = QLabel('')
        self.label_total_valor.setStyleSheet("background-color: #ffffff; color: #333333; font-size: 14px; border-radius: 5px; min-width: 170px; min-height: 20px; padding: 2px;")
        self.label_total_valor.setAlignment(Qt.AlignCenter)

        # Estilos existentes
        self.setStyleSheet("background-color: #292929;")
        self.label_cpf.setStyleSheet("color: #ded953; font-size: 16px; font-weight: bold;")
        self.input_cpf.setStyleSheet("background-color: #ffffff; color: #333333; font-size: 14px; border-radius: 5px; width: 360px; height:20px;")
        self.button_pesquisar.setStyleSheet("background-color: #00C6CC; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 5px 10px; width: 170px; height:20px;")
        self.button_limpar.setStyleSheet("background-color: #D3FF00; color: #333333; font-size: 14px; border-radius: 5px; padding: 5px 10px;")
        self.label_oferta.setStyleSheet("background-color: #292929; color: #333333; font-size: 14px; border-radius: 10px; width: 360px; height: 20px;")
        
        # Estilos para os elementos de desconto farmácia
        self.label_farm.setStyleSheet("color: #ded953; font-size: 16px; font-weight: bold")
        self.label_ultimos3.setStyleSheet("color: #ffffff; font-size: 14px;")
        self.label_total.setStyleSheet("color: #ffffff; font-size: 14px;")
        
        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.label_cpf)
        layout.addWidget(self.input_cpf)

        # Layout para os botões
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_pesquisar)
        h_layout.addWidget(self.button_limpar)
        layout.addLayout(h_layout)

        layout.addWidget(self.label_oferta)
        layout.addWidget(self.linha_divisoria) 
        
        # Layout para a seção de desconto farmácia
        layout.addWidget(self.label_farm)
        
        # Layout para os rótulos "Últimos 3 meses" e "Total"
        rotulos_layout = QHBoxLayout()
        rotulos_layout.addWidget(self.label_ultimos3)
        rotulos_layout.addWidget(self.label_total)
        layout.addLayout(rotulos_layout)
        
        # Layout para os campos de texto dos valores
        valores_layout = QHBoxLayout()
        valores_layout.addWidget(self.label_farm3m)
        valores_layout.addWidget(self.label_total_valor)
        layout.addLayout(valores_layout)

        self.setLayout(layout)

        self.button_pesquisar.clicked.connect(self.pesquisar)
        self.button_limpar.clicked.connect(self.limpar)

    def pesquisar(self):
        cpf = self.input_cpf.text()
        self.data_model.logica_pesquisa(
            cpf, 
            self.label_oferta, 
            self.label_farm3m, 
            self.label_total_valor
        )

    def limpar(self):
        self.data_model.clear_fields(
            self.input_cpf, 
            self.label_oferta, 
            self.label_farm3m, 
            self.label_total_valor
        )