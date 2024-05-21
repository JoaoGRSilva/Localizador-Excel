import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit
import pandas as pd
import openpyxl

df = pd.read_excel(r'\\fileserver-matriz\Files\Quartil - QIL\Quartil CR - QCR\Qualidade SSAP\Teste\dados.xlsx', engine='openpyxl')



class PesquisaCPF(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Retenção 5D')
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: #D3FF00")

        self.label_cpf = QLabel('Digite o CPF:')
        self.input_cpf = QLineEdit()
        self.button_pesquisar = QPushButton('Pesquisar')
        self.button_limpar = QPushButton('Limpar')
        self.label_oferta = QTextEdit()
        self.label_oferta.setReadOnly(True)
        self.input_cpf.setStyleSheet("background-color: #00C6CC; border-radius: 10px; ")
        self.button_pesquisar.setStyleSheet("background-color: #00C6CC; border-radius: 10px; ")
        self.button_limpar.setStyleSheet("background-color: #00C6CC; border-radius: 10px; ")
        self.label_oferta.setStyleSheet("background-color: #00C6CC; border-radius: 10px; ")

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

        self.df = pd.DataFrame()

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
            self.label_oferta.setStyleSheet("background-color: #ffffff; border-radius: 10px; ")

    def limpar(self):
        self.input_cpf.setText("")
        self.label_oferta.setText(" ")
        self.label_oferta.setStyleSheet("background-color: #00C6CC; border-radius: 10px; ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PesquisaCPF()
    window.show()
    sys.exit(app.exec())