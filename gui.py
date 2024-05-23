from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QFont

class PesquisaCPF(QWidget):
    def __init__(self, search_logic, clear_logic):
        super().__init__()

        self.setWindowTitle('Retenção 5D')
        self.setGeometry(100, 100, 400, 200)
        self.label_cpf = QLabel('Digite o CPF:')
        self.input_cpf = QLineEdit()
        self.button_pesquisar = QPushButton('Pesquisar')
        self.button_limpar = QPushButton('Limpar')
        self.label_oferta = QTextEdit()
        self.label_oferta.setReadOnly(True)

        self.setStyleSheet("background-color: #292929;")  # Definindo o fundo branco
        self.label_cpf.setStyleSheet("color: #ded953; font-size: 16px; font-weight: bold;")  # Definindo a cor do texto do label cpf
        self.input_cpf.setStyleSheet("background-color: #ffffff; color: #333333; font-size: 14px; border-radius: 5px;")  # Estilo para o campo de entrada CPF
        self.button_pesquisar.setStyleSheet("background-color: #00C6CC; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 5px 10px;")  # Estilo para o botão Pesquisar
        self.button_limpar.setStyleSheet("background-color: #D3FF00; color: #333333; font-size: 14px; border-radius: 5px; padding: 5px 10px;")  # Estilo para o botão Limpar
        self.label_oferta.setStyleSheet("background-color: #292929; color: #333333; font-size: 14px; border-radius: 10px;")  # Estilo para a caixa de texto de oferta


        layout = QVBoxLayout()
        layout.addWidget(self.label_cpf)
        layout.addWidget(self.input_cpf)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_pesquisar)
        h_layout.addWidget(self.button_limpar)
        layout.addLayout(h_layout)

        layout.addWidget(self.label_oferta)

        self.setLayout(layout)

        self.button_pesquisar.clicked.connect(lambda: search_logic(self.input_cpf.text(), self.label_oferta))
        self.button_limpar.clicked.connect(lambda: clear_logic(self.input_cpf, self.label_oferta))