import sys
from PyQt5.QtWidgets import QApplication
from gui import PesquisaCPF
from PesquisaCPF import search_logic, clear_logic, df


def update_logic(file_name):
    try:
        import pandas as pd
        import time
        
        print("Iniciando conversão Excel para Parquet...")
        start_time = time.time()
        
        print("Lendo arquivo Excel...")
        new_data = pd.read_excel(file_name)
        
        global df  
        df = new_data
        df.to_parquet('dados.parquet', index=False)
        end_time = time.time()
        print(f"Conversão concluída em {end_time - start_time:.2f} segundos!")
        print(f"Número de linhas convertidas: {len(df)}")
        
        # Recarregar o dataframe atualizado na memória
        df = pd.read_parquet('dados.parquet')
        
        return True
    except Exception as e:
        print(f"Erro ao atualizar base: {e}")
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PesquisaCPF(search_logic, clear_logic, update_logic)
    window.show()
    sys.exit(app.exec())
