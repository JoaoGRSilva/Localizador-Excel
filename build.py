import PyInstaller.__main__
import sys

PyInstaller.__main__.run([
    'main.py',  # seu arquivo principal
    '--onefile',  # criar um único executável
    '--noconsole',  # não mostrar console ao executar
    '--add-data', 'dados.parquet;.',  # incluir arquivo de dados
    '--icon=icon.ico',  # se você tiver um ícone
    '--name=Retençaõ 5D',  # nome do executável
    '--windowed',  # aplicação com interface gráfica
])