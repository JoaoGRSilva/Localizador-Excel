import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit
from PyQt5.QtGui import QFont
import pandas as pd

df = pd.read_excel(r'\SOROCRED – CREDITO, FINANCIAMENTO E INVESTIMENTO S\Qualidade Afinz - Documentos\Melhoria Contínua e Processos\Teste\dados.xlsx', engine='openpyxl')

class PesquisaCPF(QWidget):
    def __init__(self):
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

        self.button_pesquisar.clicked.connect(self.pesquisar)
        self.button_limpar.clicked.connect(self.limpar)
        

    def pesquisar(self):
        cpf = self.input_cpf.text()
        if df.empty:
            self.label_oferta.setText("Arquivo Excel vazio ou não carregado corretamente.")
            
        try:
            cpf = int(cpf)
        except ValueError:
            self.label_oferta.setText("CPF não é válido, por favor tente apenas números.")

        if 'cpf' not in df.columns:
            self.label_oferta.setText("Coluna CPF não encontrada!")

        if 'fx_score' not in df.columns:
            self.label_oferta.setText("Coluna FX_SCORE não encontrada!")

        if cpf in df['cpf'].values:
            linha_cpf = df[df['cpf'] == cpf]

            fx_score = linha_cpf['fx_score'].values[0]

            if fx_score == "00 - CONTA NOVA":
                self.label_oferta.setText("Cliente com conta nova, sem ofertas!")
                self.label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")
            
            elif fx_score == "01 - VERMELHO":
                self.label_oferta.setText("Cliente com uma baixa pontuação, oferta de até 25%!")
                self.label_oferta.setStyleSheet("background-color: #ff6961; border-radius: 10px; ")

            elif fx_score == "02 - AMARELO":
                self.label_oferta.setText("Cliente com pontuação mediana, oferta de até 50%!")
                self.label_oferta.setStyleSheet("background-color: #faf7a9; border-radius: 10px; ")

            elif fx_score == "03 - VERDE":
                self.label_oferta.setText("Cliente com uma boa pontuação, oferta de até 100%!")
                self.label_oferta.setStyleSheet("background-color: #cfe0bc; border-radius: 10px; ")

            else:
                self.label_oferta.setText("Oferta não localizada.")

        else:
            self.label_oferta.setText("Cliente não localizado!")
            self.label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")

    def limpar(self):
        self.input_cpf.setText("")
        self.label_oferta.setText(" ")
        self.label_oferta.setStyleSheet("background-color: #292929; border-radius: 10px; ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PesquisaCPF()
    window.show()
    sys.exit(app.exec())