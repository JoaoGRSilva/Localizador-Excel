import pandas as pd
import time


def converter_excel_para_parquet():
    print("Iniciando conversão do Excel para Parquet...")
    start_time = time.time()
    
    # Lê o arquivo Excel
    print("Lendo arquivo Excel...")
    df = pd.read_excel('dados.xlsx', engine='openpyxl')
    
    # Otimiza o tipo de dados do CPF
    print("Otimizando tipos de dados...")
    df['cpf'] = pd.to_numeric(df['cpf'], downcast='integer')
    
    # Salva como Parquet
    print("Salvando arquivo Parquet...")
    df.to_parquet('dados.parquet', index=False)
    
    end_time = time.time()
    print(f"Conversão concluída em {end_time - start_time:.2f} segundos!")
    print(f"Número de linhas convertidas: {len(df)}")

if __name__ == "__main__":
    converter_excel_para_parquet()