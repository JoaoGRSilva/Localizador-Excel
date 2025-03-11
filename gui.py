from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QTextEdit, QFileDialog, QMessageBox, QFrame)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt, QEvent

class PesquisaCPF(QWidget):
    def __init__(self, search_logic, clear_logic, update_logic):
        super().__init__()

        self.secret_code = "att5d"  # Código secreto para ativar o botão
        self.current_input = ""  # Armazena as teclas digitadas
        
        self.setWindowIcon(QIcon("icon.ico"))
        
        self.setWindowTitle('Retenção 5D')
        self.setGeometry(100, 100, 400, 320)
        self.setFixedSize(400, 320)  # Torna a janela não redimensionável
        
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
        
        # Adicionar labels para mostrar os valores (em vez de QTextEdit)
        self.label_farm3m = QLabel('')
        self.label_farm3m.setStyleSheet("background-color: #ffffff; color: #333333; font-size: 14px; border-radius: 5px; min-width: 170px; min-height: 20px; padding: 2px;")
        self.label_farm3m.setAlignment(Qt.AlignCenter)
        
        self.label_total_valor = QLabel('')
        self.label_total_valor.setStyleSheet("background-color: #ffffff; color: #333333; font-size: 14px; border-radius: 5px; min-width: 170px; min-height: 20px; padding: 2px;")
        self.label_total_valor.setAlignment(Qt.AlignCenter)
        
        # Botão de atualização (inicialmente oculto)
        self.button_update = QPushButton('Atualizar Base')
        self.button_update.setStyleSheet("background-color: #4CAF50; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 5px 10px;")
        self.button_update.hide()  # Inicialmente oculto

        # Estilos existentes
        self.setStyleSheet("background-color: #292929;")
        self.label_cpf.setStyleSheet("color: #ded953; font-size: 16px; font-weight: bold;")
        self.input_cpf.setStyleSheet("background-color: #ffffff; color: #333333; font-size: 14px; border-radius: 5px; width: 360px; height:20px;")
        self.button_pesquisar.setStyleSheet("background-color: #00C6CC; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 5px 10px; width: 170px; height:20px;")
        self.button_limpar.setStyleSheet("background-color: #D3FF00; color: #333333; font-size: 14px; border-radius: 5px; padding: 5px 10px;")
        self.label_oferta.setStyleSheet("background-color: #292929; color: #333333; font-size: 14px; border-radius: 10px; width: 360px; height: 40px;")
        
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
        h_layout.addWidget(self.button_update)
        layout.addLayout(h_layout)

        layout.addWidget(self.label_oferta)
        layout.addWidget(self.linha_divisoria)  # Adicionar a linha divisória
        
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

        # Conectando os sinais (sintaxe diferente no PySide6)
        self.button_pesquisar.clicked.connect(lambda: search_logic(self.input_cpf.text(), self.label_oferta, self.label_farm3m, self.label_total_valor))
        self.button_limpar.clicked.connect(lambda: self.clear_all_fields(clear_logic))
        self.button_update.clicked.connect(lambda: self.update_database(update_logic))

        # Instalando event filter para capturar teclas
        self.installEventFilter(self)

    def clear_all_fields(self, clear_logic):
        # Limpa todos os campos
        clear_logic(self.input_cpf, self.label_oferta)
        self.label_farm3m.setText("")
        self.label_total_valor.setText("")

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
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