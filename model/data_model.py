import pandas as pd

class DataModel:
    def __init__(self):
        self.df = None
        self.carregar_base()

    # Carrega os dados do arquivo Parquet
    def carregar_base(self):
        print("Carregando dados...\n")
        try:
            self.df = pd.read_parquet('data\\dados.parquet')  # caminho com escape
            print("\nDados carregados com sucesso!\n\nPrintando colunas:")
            print(self.df.columns)
            print("\nPrintando cabeçalho:")
            print(self.df.head())
            return self.df
        except FileNotFoundError:
            print("Arquivo Parquet não encontrado. Criando DataFrame vazio.")
            return None
        except Exception as e:
            print(f"Erro ao carregar dados: {str(e)}")
            return None

    # Trata o CPF: valida e remove caracteres não numéricos
    @staticmethod
    def tratar_cpf(cpf):
        try:
            cpf = int(cpf)
        except ValueError:
            text = "CPF não é válido, por favor tente apenas números."
            style = "background-color: gray; border-radius: 10px; "
            return text, style

        cpf = ''.join(filter(str.isdigit, str(cpf)))

        cpf = cpf.zfill(11)
        
        return cpf

    # Lógica principal de pesquisa por CPF e atualização de labels
    def logica_pesquisa(self, cpf, label_oferta, label_farm3m=None, label_total_valor=None):
        # Verifica se o DataFrame está carregado e possui dados
        if self.df is None:
            label_oferta.setText("Erro ao carregar dados!")
            label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px;")
            return

        if self.df.empty:
            label_oferta.setText("Base de dados vazia!")
            label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px;")
            return

        # Verifica se todas as colunas necessárias existem no DataFrame
        required_columns = ['cpf', 'fx_semaforo', 'desc_farmacia_ult3m', 'desc_farmacia_total', 'numero_conta']
        for column in required_columns:
            if column not in self.df.columns:
                label_oferta.setText(f"Coluna {column.upper()} não foi encontrada!")
                return

        # Trata o CPF antes de aplicar a pesquisa
        cpf_tratado = self.tratar_cpf(cpf)
        if isinstance(cpf_tratado, tuple):
            label_oferta.setText(cpf_tratado[0])
            label_oferta.setStyleSheet(cpf_tratado[1])
            return

        # Filtra o DataFrame por CPF
        mask = self.df['cpf'] == cpf_tratado
        if mask.any():
            linha_cpf = self.df.loc[mask].copy()
            row_count = len(linha_cpf)

            if row_count == 1:
                selected_row = linha_cpf.iloc[0]
                selected_message = ""
            else:
                # Se houver múltiplas contas, escolhe a de melhor score
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

            # Obtém os dados da linha selecionada
            fx_semaforo = selected_row['fx_semaforo']
            desc_farm_3m = selected_row.get('desc_farmacia_ult3m')
            desc_farm_total = selected_row.get('desc_farmacia_total')

            # Define mensagens e cores com base no semáforo
            offer_messages = {
                "4 - MORTO": ("VERMELHO 25%", "#FF2A00"),
                "1 - VERMELHO": ("VERMELHO 25%", "#FF2A00"),
                "2 - AMARELO": ("AMARELO 50% A 75%", "#FFEB3B"),
                "3 - VERDE": ("VERDE 75% A 100%", "#28A745"),
            }
            message, color = offer_messages.get(fx_semaforo, ("Oferta não localizada.", "#f8f8ff"))

            # Atualiza os labels
            label_oferta.setText(message + selected_message if row_count > 1 else message)
            label_oferta.setStyleSheet(f"background-color: {color}; border-radius: 10px; ")

            # Atualiza o label de descontons nos últimos 3 meses
            if label_farm3m is not None:
                valor_formatado_3m = "R$ 0,00"
                if desc_farm_3m is not None and pd.notna(desc_farm_3m):
                    try:
                        valor_formatado_3m = f"R$ {float(desc_farm_3m):.2f}".replace('.', ',')
                    except (ValueError, TypeError):
                        pass
                label_farm3m.setText(valor_formatado_3m)

            # Atualiza o label de descontons no total
            if label_total_valor is not None:
                valor_formatado_total = "R$ 0,00"
                if desc_farm_total is not None and pd.notna(desc_farm_total):
                    try:
                        valor_formatado_total = f"R$ {float(desc_farm_total):.2f}".replace('.', ',')
                    except (ValueError, TypeError):
                        pass
                label_total_valor.setText(valor_formatado_total)

        else:
            # CPF não encontrado
            label_oferta.setText("Cliente não localizado!")
            label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")
            if label_farm3m is not None:
                label_farm3m.setText("R$ 0,00")
            if label_total_valor is not None:
                label_total_valor.setText("R$ 0,00")

    # Reseta todos os campos da tela
    @staticmethod
    def clear_fields(input_cpf, label_oferta, label_farm3m=None, label_total_valor=None):
        input_cpf.setText("")
        label_oferta.setText(" ")
        label_oferta.setStyleSheet("background-color: #292929; border-radius: 10px; ")
        if label_farm3m:
            label_farm3m.setText("R$ 0,00")
        if label_total_valor:
            label_total_valor.setText("R$ 0,00")