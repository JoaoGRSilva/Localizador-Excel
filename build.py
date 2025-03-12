import PyInstaller.__main__
import sys

PyInstaller.__main__.run([
    'main.py',  # seu arquivo principal
    '--onefile',  # criar um único executável
    '--noconsole',  # não mostrar console ao executar
    '--icon=icon.ico',  # se você tiver um ícone
    '--name=Retenção 5D',  # nome do executável
    '--windowed',  # aplicação com interface gráfica
])