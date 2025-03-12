import pandas as pd
import time
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton, QDialog, QMessageBox
from PySide6.QtCore import Qt

print("Carregando dados...")
start_time = time.time()
try:
    df = pd.read_parquet('dados.parquet')
    load_time = time.time() - start_time
    print(f"Dados carregados em {load_time:.2f} segundos!")
except FileNotFoundError:
    print("Arquivo Parquet não encontrado.")
    df = pd.DataFrame()

def search_logic(cpf, label_oferta, label_farm3m=None, label_total_valor=None, parent=None):
    global df
    
    if df.empty:
        label_oferta.setText("Arquivo de dados vazio ou não carregado corretamente.")
        label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")
        return
    
    required_columns = ['cpf', 'fx_score', 'desc_farmacia_ult3m', 'desc_farmacia_total']
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
        linha_cpf = df.loc[mask]
        row_count = len(linha_cpf)

        if row_count == 1:
            linha_cpf = df.loc[mask].iloc[0]
        else:
            account = linha_cpf['numero_conta']
            account_list = account.tolist()
            
            selected_account = show_account_selection_dialog(account_list, parent)
            if selected_account is None:
                label_oferta.setText("Nenhuma conta selecionada.")
                return
            try:

                if linha_cpf['numero_conta'].dtype.kind in 'iu': 
                    selected_account = int(selected_account)
            except (ValueError, TypeError):
                pass 
                

            filtered = linha_cpf[linha_cpf['numero_conta'] == selected_account]
            

            if filtered.empty:
                label_oferta.setText("Conta selecionada não encontrada.")
                label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")
                return
                
            linha_cpf = filtered.iloc[0]

        fx_score = linha_cpf['fx_score']
        desc_farm_3m = linha_cpf['desc_farmacia_ult3m']
        desc_farm_total = linha_cpf['desc_farmacia_total']        

        offer_messages = {
            "4 - MORTO": ("VERMELHO 25%", "#FF2A00"),
            "1 - VERMELHO": ("VERMELHO 25%", "#FF2A00"),
            "2 - AMARELO": ("AMARELO 50% A 75%", "#FFEB3B"),
            "3 - VERDE": ("VERDE 75% A 100%", "#28A745"),
        }

        message, color = offer_messages.get(fx_score, ("Oferta não localizada.", "#f8f8ff"))
        label_oferta.setText(message)
        label_oferta.setStyleSheet(f"background-color: {color}; border-radius: 10px; ")

        if label_farm3m is not None:
            valor_formatado_3m = f"R$ {desc_farm_3m:.2f}".replace('.', ',')
            label_farm3m.setText(valor_formatado_3m)
            
        if label_total_valor is not None:
            valor_formatado_total = f"R$ {desc_farm_total:.2f}".replace('.', ',')
            label_total_valor.setText(valor_formatado_total)
    else:
        label_oferta.setText("Cliente não localizado!")
        label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")

        if label_farm3m is not None:
            label_farm3m.setText("R$ 0,00")
        if label_total_valor is not None:
            label_total_valor.setText("R$ 0,00")


def show_account_selection_dialog(account_list, parent=None):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Selecione a Conta")
    dialog.setWindowModality(Qt.WindowModal) 
    
    dialog.setStyleSheet("QDialog { background-color: #292929; }"
                         "QLabel { color: white; }"
                         "QRadioButton { color: white; }")
    
    layout = QVBoxLayout()

    radio_buttons = []
    selected_account = None


    if account_list:
        for i, n in enumerate(account_list):
            radio_button = QRadioButton(str(n))
            if i == 0:
                radio_button.setChecked(True)
            radio_buttons.append(radio_button)
            layout.addWidget(radio_button)

    confirm_button = QPushButton("Confirmar")
    confirm_button.setStyleSheet("QPushButton { color: white; background-color: #3a3a3a; border: 1px solid #555; border-radius: 3px; padding: 5px; }"
                                "QPushButton:hover { background-color: #4a4a4a; }"
                                "QPushButton:pressed { background-color: #555; }")
    
    def on_confirm():
        nonlocal selected_account
        for radio_button in radio_buttons:
            if radio_button.isChecked():
                selected_account = radio_button.text()
                dialog.accept()
                break
        if selected_account is None and radio_buttons:
            selected_account = radio_buttons[0].text()
            dialog.accept()

    confirm_button.clicked.connect(on_confirm)
    layout.addWidget(confirm_button)

    dialog.setLayout(layout)
    

    if parent:
        dialog.move(parent.frameGeometry().center() - dialog.rect().center())


    dialog.exec()

    return selected_account


def clear_logic(input_cpf, label_oferta, label_farm3m=None, label_total_valor=None):
    input_cpf.setText("")
    label_oferta.setText(" ")
    label_oferta.setStyleSheet("background-color: #292929; border-radius: 10px; ")
    
    if label_farm3m is not None:
        label_farm3m.setText("R$ 0,00")
    if label_total_valor is not None:
        label_total_valor.setText("R$ 0,00")


def update_logic(file_path):
    global df
    try:
        new_df = pd.read_excel(file_path)
        

        required_columns = ['cpf', 'fx_score', 'desc_farmacia_ult3m', 'desc_farmacia_total']
        for column in required_columns:
            if column not in new_df.columns:
                print(f"Coluna {column} não encontrada no arquivo!")
                return False
        
        new_df.to_parquet('dados.parquet')
        df = new_df
        
        return True
    except Exception as e:
        print(f"Erro ao atualizar a base: {str(e)}")
        return False