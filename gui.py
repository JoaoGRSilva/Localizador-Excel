from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QTextEdit, QFileDialog, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class PesquisaCPF(QWidget):
    def __init__(self, search_logic, clear_logic, update_logic):
        super().__init__()

        self.secret_code = "att5d"  # Código secreto para ativar o botão
        self.current_input = ""  # Armazena as teclas digitadas
        
        self.setWindowTitle('Retenção 5D')
        self.setGeometry(100, 100, 400, 200)
        
        # Widgets existentes
        self.label_cpf = QLabel('Digite o CPF:')
        self.input_cpf = QLineEdit()
        self.button_pesquisar = QPushButton('Pesquisar')
        self.button_limpar = QPushButton('Limpar')
        self.label_oferta = QTextEdit()
        self.label_oferta.setReadOnly(True)
        
        # Botão de atualização (inicialmente oculto)
        self.button_update = QPushButton('Atualizar Base')
        self.button_update.setStyleSheet("background-color: #4CAF50; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 5px 10px;")
        self.button_update.hide()  # Inicialmente oculto

        # Estilos existentes
        self.setStyleSheet("background-color: #292929;")
        self.label_cpf.setStyleSheet("color: #ded953; font-size: 16px; font-weight: bold;")
        self.input_cpf.setStyleSheet("background-color: #ffffff; color: #333333; font-size: 14px; border-radius: 5px;")
        self.button_pesquisar.setStyleSheet("background-color: #00C6CC; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 5px 10px;")
        self.button_limpar.setStyleSheet("background-color: #D3FF00; color: #333333; font-size: 14px; border-radius: 5px; padding: 5px 10px;")
        self.label_oferta.setStyleSheet("background-color: #292929; color: #333333; font-size: 14px; border-radius: 10px;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_cpf)
        layout.addWidget(self.input_cpf)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_pesquisar)
        h_layout.addWidget(self.button_limpar)
        h_layout.addWidget(self.button_update)
        layout.addLayout(h_layout)

        layout.addWidget(self.label_oferta)

        self.setLayout(layout)

        # Conectando os sinais
        self.button_pesquisar.clicked.connect(lambda: search_logic(self.input_cpf.text(), self.label_oferta))
        self.button_limpar.clicked.connect(lambda: clear_logic(self.input_cpf, self.label_oferta))
        self.button_update.clicked.connect(lambda: self.update_database(update_logic))

        # Instalando event filter para capturar teclas
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress:
            # Captura a tecla pressionada
            key = event.text().lower()
            
            # Adiciona a tecla à sequência atual
            self.current_input += key
            
            # Mantém apenas os últimos caracteres (tamanho do código secreto)
            self.current_input = self.current_input[-len(self.secret_code):]
            
            # Verifica se o código secreto foi digitado
            if self.current_input == self.secret_code:
                self.button_update.show()
                self.current_input = ""  # Limpa a sequência
            
        return super().eventFilter(obj, event)

    def update_database(self, update_logic):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo Excel", "", "Excel Files (*.xlsx *.xls)")
            if file_name:
                success = update_logic(file_name)
                if success:
                    QMessageBox.information(self, "Sucesso", "Base de dados atualizada com sucesso!")
                    self.button_update.hide()  # Esconde o botão após atualização
                else:
                    QMessageBox.warning(self, "Erro", "Erro ao atualizar a base de dados.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar: {str(e)}")
            print((self, "Erro", f"Erro ao atualizar: {str(e)}"))