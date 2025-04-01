import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py', 
    '--onefile', 
    '--noconsole',  
    '--name=Retenção 5D',  
    '--windowed',  
    '--icon=icon.ico',  
    '--hidden-import=PySide6.QtCore',
    '--hidden-import=PySide6.QtGui',
    '--hidden-import=PySide6.QtWidgets',
])
