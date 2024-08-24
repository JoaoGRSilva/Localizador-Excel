import pandas as pd

df = pd.read_excel('dados.xlsx', engine='openpyxl')

def search_logic(cpf, label_oferta):
    if df.empty:
        label_oferta.setText("Arquivo Excel vazio ou não carregado corretamente.")
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
        return
    
    if cpf in df['cpf'].values:
        linha_cpf = df[df['cpf'] == cpf]
        fx_score = linha_cpf['fx_score'].values[0]

        # Dicionário para mensagens e estilos
        offer_messages = {
            "00 - CONTA NOVA": ("Cliente com conta nova, sem ofertas!", "#f8f8ff"),
            "01 - VERMELHO": ("Cliente com uma baixa pontuação, oferta de até 25%!", "#ff6961"),
            "02 - AMARELO": ("Cliente com pontuação mediana, oferta de até 50%!", "#faf7a9"),
            "03 - VERDE": ("Cliente com uma boa pontuação, oferta de até 100%!", "#cfe0bc"),
        }

        # Definir mensagem e estilo com base no fx_score
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