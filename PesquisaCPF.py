import pandas as pd

df = pd.read_excel('dados.xlsx', engine='openpyxl')

def search_logic(cpf, label_oferta):
    if df.empty:
        label_oferta.setText("Arquivo Excel vazio ou não carregado corretamente.")
        
    try:
        cpf = int(cpf)
    except ValueError:
        label_oferta.setText("CPF não é válido, por favor tente apenas números.")

    if 'cpf' not in df.columns:
        label_oferta.setText("Coluna CPF não encontrada!")

    if 'fx_score' not in df.columns:
        label_oferta.setText("Coluna FX_SCORE não encontrada!")

    if cpf in df['cpf'].values:
        linha_cpf = df[df['cpf'] == cpf]

        fx_score = linha_cpf['fx_score'].values[0]

        if fx_score == "00 - CONTA NOVA":
            label_oferta.setText("Cliente com conta nova, sem ofertas!")
            label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")
        
        elif fx_score == "01 - VERMELHO":
            label_oferta.setText("Cliente com uma baixa pontuação, oferta de até 25%!")
            label_oferta.setStyleSheet("background-color: #ff6961; border-radius: 10px; ")

        elif fx_score == "02 - AMARELO":
            label_oferta.setText("Cliente com pontuação mediana, oferta de até 50%!")
            label_oferta.setStyleSheet("background-color: #faf7a9; border-radius: 10px; ")

        elif fx_score == "03 - VERDE":
            label_oferta.setText("Cliente com uma boa pontuação, oferta de até 100%!")
            label_oferta.setStyleSheet("background-color: #cfe0bc; border-radius: 10px; ")

        else:
            label_oferta.setText("Oferta não localizada.")

    else:
        label_oferta.setText("Cliente não localizado!")
        label_oferta.setStyleSheet("background-color: #f8f8ff; border-radius: 10px; ")

def clear_logic(input_cpf, label_oferta):
    input_cpf.setText("")
    label_oferta.setText(" ")
    label_oferta.setStyleSheet("background-color: #292929; border-radius: 10px; ")