import pandas as pd
import time
from PySide6 import QtWidgets


print("Carregando dados...")
start_time = time.time()
try:
    df = pd.read_parquet('dados.parquet')
    load_time = time.time() - start_time
    print(f"Dados carregados em {load_time:.2f} segundos!")
except FileNotFoundError:
    print("Arquivo Parquet não encontrado. Use converter_excel.py primeiro para converter o Excel.")
    df = pd.DataFrame()

def search_logic(cpf, label_oferta, label_farm3m=None, label_total_valor=None):
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
        linha_cpf = df.loc[mask].iloc[0]
        fx_score = linha_cpf['fx_score']
        desc_farm_3m = linha_cpf['desc_farmacia_ult3m']
        desc_farm_total = linha_cpf['desc_farmacia_total']

        offer_messages = {
            "4 - MORTO": ("VERMELHO 25%", "#ff6961"),
            "1 - VERMELHO": ("VERMELHO 25%", "#ff6961"),
            "2 - AMARELO": ("AMARELO 50% A 75%", "#faf7a9"),
            "3 - VERDE": ("VERDE 75% A 100%", "#cfe0bc"),
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


def clear_logic(input_cpf, label_oferta):
    input_cpf.setText("")
    label_oferta.setText(" ")
    label_oferta.setStyleSheet("background-color: #292929; border-radius: 10px; ")


def update_logic(file_path):
    global df
    try:
        # Lê o arquivo Excel
        new_df = pd.read_excel(file_path)
        
        # Verifica se possui as colunas necessárias
        required_columns = ['cpf', 'fx_score', 'desc_farmacia_ult3m', 'desc_farmacia_total']
        for column in required_columns:
            if column not in new_df.columns:
                print(f"Coluna {column} não encontrada no arquivo!")
                return False
        
        # Salva como parquet
        new_df.to_parquet('dados.parquet')
        
        # Recarrega o dataframe
        df = new_df
        
        return True
    except Exception as e:
        print(f"Erro ao atualizar a base: {str(e)}")
        return False