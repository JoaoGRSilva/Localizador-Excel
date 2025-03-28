import pandas as pd
import time
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton, QDialog, QMessageBox, QLabel
from PySide6.QtCore import Qt

print("Carregando dados...")
start_time = time.time()
try:
    df = pd.read_parquet('dados.parquet')
    load_time = time.time() - start_time
    print(df)
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
    
    required_columns = ['cpf', 'fx_semaforo', 'desc_farmacia_ult3m', 'desc_farmacia_total', 'numero_conta']
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
    
    cpf = ''.join(filter(str.isdigit, str(cpf)))
    if len(cpf) < 11:
        cpf = cpf.zfill(11)

    print(cpf, type(cpf))

    mask = df['cpf'] == cpf

    print(mask)

    if mask.any():
        linha_cpf = df.loc[mask].copy()
        row_count = len(linha_cpf)
        print(linha_cpf)

        if row_count == 1:
            selected_row = linha_cpf.iloc[0]
        else:
            score_mapping = {
                "3 - VERDE": 1,
                "2 - AMARELO": 2,
                "1 - VERMELHO": 3,
                "4 - MORTO": 4,
            }
            
            linha_cpf['score_value'] = linha_cpf['fx_semaforo'].map(score_mapping)
            linha_cpf = linha_cpf.sort_values('score_value')
            selected_row = linha_cpf.iloc[0] 
            selected_message = f"\nA melhor conta encontrada é: {selected_row['numero_conta']}"
            print(f"Múltiplas contas encontradas. Selecionada automaticamente a conta com melhor score: {selected_row['numero_conta']}")

        # Extrair os valores da linha selecionada
        fx_score = selected_row['fx_semaforo']
        desc_farm_3m = selected_row['desc_farmacia_ult3m']
        desc_farm_total = selected_row['desc_farmacia_total']
        numero_conta = selected_row['numero_conta']

        offer_messages = {
            "4 - MORTO": ("VERMELHO 25%", "#FF2A00"),
            "1 - VERMELHO": ("VERMELHO 25%", "#FF2A00"),
            "2 - AMARELO": ("AMARELO 50% A 75%", "#FFEB3B"),
            "3 - VERDE": ("VERDE 75% A 100%", "#28A745"),
        }

        message, color = offer_messages.get(fx_score, ("Oferta não localizada.", "#f8f8ff"))
        if row_count == 1:
            label_oferta.setText(message)
        else:
            label_oferta.setText(message + selected_message)
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
        
        required_columns = ['cpf', 'fx_score', 'desc_farmacia_ult3m', 'desc_farmacia_total', 'numero_conta']
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