#backend.py
import pandas as pd
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton, QDialog, QMessageBox, QLabel
from PySide6.QtCore import Qt
 

class DataModel:

    def __init__(self):
        self.df = None
        self.carregar_base()

    def carregar_base(self):
        print("Carregando dados...")
        try:
            self.df = pd.read_parquet('dados.parquet')
            print("Dados carregados com sucesso!")
            print(self.df.head())
            return self.df
        
        except FileNotFoundError:
            print("Arquivo Parquet não encontrado. Criando DataFrame vazio.")
            self.df = pd.DataFrame({
                'cpf': [], 
                'fx_semaforo': [], 
                'desc_farmacia_ult3m': [], 
                'desc_farmacia_total': [],
                'numero_conta': []
            })
            return self.df
        
        except Exception as e:
            print(f"Erro ao carregar dados: {str(e)}")
            self.df = pd.DataFrame({
                'cpf': [], 
                'fx_semaforo': [], 
                'desc_farmacia_ult3m': [], 
                'desc_farmacia_total': [],
                'numero_conta': []
            })
            return self.df

    @staticmethod
    def tratar_cpf(cpf):
        try:
            cpf = int(cpf)
        except ValueError:
            text = "CPF não é válido, por favor tente apenas números."
            style = "background-color: #f8f8ff; border-radius: 10px; "
            return text, style

        cpf = ''.join(filter(str.isdigit, str(cpf)))

        if len(cpf) < 11:
            cpf = cpf.zfill(11)
        
        return cpf
    

    def logica_pesquisa(self ,cpf, label_oferta, label_farm3m=None, label_total_valor=None):

        if self.df is None:
            print("DataFrame não inicializado. Tentando carregar novamente...")
            self.carregar_base()

        if self.df is None:
            label_oferta.setText("Erro ao carregar dados!")
            label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px;")
            return      


        required_columns = ['cpf', 'fx_semaforo', 'desc_farmacia_ult3m', 'desc_farmacia_total', 'numero_conta']    
        
        cpf_tratado = self.tratar_cpf(cpf)

        if isinstance(cpf_tratado, tuple):
            label_oferta.setText(cpf_tratado[0])
            label_oferta.setStyleSheet(cpf_tratado[1])
            return
        
        mask = self.df['cpf'] == cpf_tratado

        if self.df.empty:
            label_oferta.setText("Arquivo de dados vazio ou não carregado corretamente.")
            label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")
            return 

        for column in required_columns:
            if column not in self.df.columns:
                label_oferta.setText(f"Coluna {column.upper()} não foi encontrada!")
                return

        if mask.any():
            linha_cpf = self.df.loc[mask].copy()
            row_count = len(linha_cpf)
            print(linha_cpf)

            if row_count == 1:
                selected_row = linha_cpf.iloc[0]
                selected_message = ""
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
                print(f"Múltiplas contas encontradas. Selecionada a conta com melhor score: {selected_row['numero_conta']}")

            fx_semaforo = selected_row['fx_semaforo']
            desc_farm_3m = selected_row.get('desc_farmacia_ult3m')  
            desc_farm_total = selected_row.get('desc_farmacia_total')

            offer_messages = {
                "4 - MORTO": ("VERMELHO 25%", "#FF2A00"),
                "1 - VERMELHO": ("VERMELHO 25%", "#FF2A00"),
                "2 - AMARELO": ("AMARELO 50% A 75%", "#FFEB3B"),
                "3 - VERDE": ("VERDE 75% A 100%", "#28A745"),
            }

            message, color = offer_messages.get(fx_semaforo, ("Oferta não localizada.", "#f8f8ff"))
            if row_count == 1:
                label_oferta.setText(message)
            else:
                label_oferta.setText(message + selected_message)
            label_oferta.setStyleSheet(f"background-color: {color}; border-radius: 10px; ")

            if label_farm3m is not None:
                if desc_farm_3m is not None and pd.notna(desc_farm_3m): 
                    try:
                        valor_formatado_3m = f"R$ {float(desc_farm_3m):.2f}".replace('.', ',')
                    except (ValueError, TypeError):
                        valor_formatado_3m = "R$ 0,00"
                else:
                    valor_formatado_3m = "R$ 0,00"
                label_farm3m.setText(valor_formatado_3m)
            
            # Tratar valores nulos para o valor total
            if label_total_valor is not None:
                if desc_farm_total is not None and pd.notna(desc_farm_total):  
                    try:
                        valor_formatado_total = f"R$ {float(desc_farm_total):.2f}".replace('.', ',')
                    except (ValueError, TypeError):
                        valor_formatado_total = "R$ 0,00"
                else:
                    valor_formatado_total = "R$ 0,00"
                label_total_valor.setText(valor_formatado_total)

        else:
            label_oferta.setText("Cliente não localizado!")
            label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")
    
            if label_farm3m is not None:
                label_farm3m.setText("R$ 0,00")
            if label_total_valor is not None:
                label_total_valor.setText("R$ 0,00")
    
    @staticmethod
    def clear_fields(input_cpf, label_oferta, label_farm3m=None, label_total_valor=None):
        input_cpf.setText("")
        label_oferta.setText(" ")
        label_oferta.setStyleSheet("background-color: #292929; border-radius: 10px; ")
        label_farm3m.setText("R$ 0,00")
        label_total_valor.setText("R$ 0,00")   