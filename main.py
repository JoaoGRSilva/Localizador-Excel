import PySimpleGUI as sg
import pandas as pd
import openpyxl

# Carrega o arquivo Excel
df = pd.read_excel(r'C:\Users\joao_silva\Desktop\HTML TESTE\RFV - CR - Copia.xlsx', engine='openpyxl')

sg.theme('LightGreen2')

layout = [
    [[sg.Text('Digite o CPF:'), sg.InputText(key='-CPF-')], [sg.Button('Pesquisar'), sg.Button('Atualizar Tabela')]],
    [sg.Text('', key='-OFERTA-', size=(50, 3), text_color='#000000', justification="center")]
]

# Cria a janela
window = sg.Window('Pesquisa de CPF', layout)

def atualizar_tabela():
    global df
    df = pd.read_excel('dados.xlsx', engine='openpyxl')

# Loop de eventos para processar eventos e obter valores
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == 'Atualizar Tabela':
        atualizar_tabela()
        window['-OFERTA-'].update('Tabela atualizada com sucesso!')

    elif event == 'Pesquisar':
        if df.empty:
            window['-OFERTA-'].update('Arquivo Excel vazio ou não carregado corretamente.')
            continue

        try:
            cpf = int(values['-CPF-'])
        except ValueError:
            window['-OFERTA-'].update('Digite um CPF válido (apenas números).')
            continue

        # Verifica se a coluna 'CPF' existe no DataFrame
        if 'CPF' not in df.columns:
            window['-OFERTA-'].update('A coluna "CPF" não existe no arquivo Excel.')
            continue

        # Verifica se a coluna 'fx_score' existe no DataFrame
        if 'fx_score' not in df.columns:
            window['-OFERTA-'].update('A coluna "fx_score" não existe no arquivo Excel.')
            continue

        # Verifica se o CPF existe na coluna 'CPF'
        if cpf in df['CPF'].values:
            # Exibe os dados do CPF encontrado
            dados_cpf = df[df['CPF'] == cpf]
            
            # Obtém o valor da coluna 'fx_score' para o CPF encontrado
            fx_score = dados_cpf['fx_score'].values[0]
            
            if fx_score == "00 - CONTA NOVA":
                window['-OFERTA-'].update('Cliente com conta nova, sem ofertas!')
                window['-OFERTA-'].update(text_color='#000000')
                window['-OFERTA-'].update(background_color='#f8f8ff')
            elif fx_score == "02 - AMARELO":
                window['-OFERTA-'].update('Cliente com pontuação mediana, oferte de até 50%!')
                window['-OFERTA-'].update(text_color='#000000')
                window['-OFERTA-'].update(background_color='#faf7a9')
            elif fx_score == "581 - VERMELHO":
                window['-OFERTA-'].update('Cliente com uma baixa pontuação, oferta de até 25%!')
                window['-OFERTA-'].update(text_color='#000000')
                window['-OFERTA-'].update(background_color='#f8f8ff')
            elif fx_score == "03 - VERDE":
                window['-OFERTA-'].update('Cliente com uma boa pontuação, oferta de até 100%!')
                window['-OFERTA-'].update(text_color='#000000')
                window['-OFERTA-'].update(background_color='#cfe0bc')
            else:
                window['-OFERTA-'].update('Cliente não tem oferta disponível.')
                window['-OFERTA-'].update(text_color='#000000')
        else:
            window['-OFERTA-'].update('Cliente não localizado!')
            window['-OFERTA-'].update(text_color='#000000')
            window['-OFERTA-'].update(background_color='#ffffff')
    else:
        window['-OFERTA-'].update('')

# Fecha a janela
window.close()