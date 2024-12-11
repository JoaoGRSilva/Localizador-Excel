import pandas as pd
import time
from PyQt5 import QtWidgets


# Carrega os dados do Parquet
print("Carregando dados...")
start_time = time.time()
try:
    df = pd.read_parquet('dados.parquet')
    load_time = time.time() - start_time
    print(f"Dados carregados em {load_time:.2f} segundos!")
except FileNotFoundError:
    print("Arquivo Parquet não encontrado. Use converter_excel.py primeiro para converter o Excel.")
    df = pd.DataFrame()

def search_logic(cpf, label_oferta):
    global df
    
    if df.empty:
        label_oferta.setText("Arquivo de dados vazio ou não carregado corretamente.")
        return
    
    required_columns = ['cpf', 'fx_score']
    for column in required_columns:
        if column not in df.columns:
            label_oferta.setText(f"Coluna {column.upper()} não foi encontrada!")
            return

    try:
        cpf = int(cpf)
    except ValueError:
        label_oferta.setText("CPF não é válido, por favor tente apenas números.")
        label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")
        return
    
    mask = df['cpf'] == cpf
    if mask.any():
        linha_cpf = df.loc[mask].iloc[0]
        fx_score = linha_cpf['fx_score']

        offer_messages = {
            "4 - MORTO": ("VERMELHO 25%", "#ff6961"),
            "1 - VERMELHO": ("VERMELHO 25%", "#ff6961"),
            "2 - AMARELO": ("AMARELO 50% A 75%", "#faf7a9"),
            "3 - VERDE": ("VERDE 75% A 100%", "#cfe0bc"),
        }

        message, color = offer_messages.get(fx_score, ("Oferta não localizada.", "#f8f8ff"))
        label_oferta.setText(message)
        label_oferta.setStyleSheet(f"background-color: {color}; border-radius: 10px; ")
    else:
        label_oferta.setText("Cliente não localizado!")
        label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")


def clear_logic(input_cpf, label_oferta):
    input_cpf.setText("")
    label_oferta.setText(" ")
    label_oferta.setStyleSheet("background-color: #292929; border-radius: 10px; ")


def filtroEvento(self, obj, event):
    if event.type() == event.KeyPress:
        key = event.text().lower()

        self.current_input += key

        self.current_input = self.current_input[-len(self.secret_code):]

        if self.current_input == self.secret_code:
            self.button_update.show()
            self.current.input = ""

    return super().eventFilter(obj, event)

def update_dataBase(self, update_logic):
    try:
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Selecionar arquivo Excel", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            sucess = update_logic(file_name)
            if sucess:
                QtWidgets.QMessageBox.information(self, "Sucesso", "Base de dados atualizada com sucesso!")
                self.button_update.hide()

            else:
                QtWidgets.QMessageBox.warning(self, "Erro", "Não foi possivel atualizar a base dados!")

    except Exception as e:
        QtWidgets.QMessageBox.critical(self, "Erro", f"Erro ao atualizar: {str(e)}")