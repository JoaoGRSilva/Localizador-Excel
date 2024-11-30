# Retenção 5D - Aplicativo de Pesquisa de CPF

**Retenção 5D** é um aplicativo desenvolvido para realizar pesquisas de CPF e fornecer ofertas personalizadas com base no `fx_score` do cliente. Além disso, o app agora inclui funcionalidades aprimoradas para **atualizar a base de dados** diretamente dentro da aplicação e **carregar os dados de maneira otimizada**, proporcionando uma experiência mais rápida e eficiente.

## 🆕 **Novidades na versão 2.0**
### **Funcionalidades adicionadas:**
1. **Atualização de Banco de Dados dentro do App**:
   - Agora você pode **atualizar o banco de dados** diretamente no aplicativo, sem necessidade de conversão manual do arquivo.
   - Basta clicar no botão **"Atualizar Base"**, fornecer um arquivo Excel atualizado, e o banco de dados será automaticamente convertido para o formato Parquet.
   - Para garantir maior segurança, o botão de atualização fica oculto até que um código secreto seja inserido.

2. **Otimização na Abertura do Aplicativo**:
   - O tempo de carregamento foi otimizado, tornando a abertura do aplicativo muito mais rápida.
   - A busca de CPF e o carregamento dos dados agora são mais eficientes, proporcionando uma experiência melhor para o usuário.

3. **Melhoria na Lógica de Busca de CPF**:
   - A busca foi otimizada para garantir **respostas mais rápidas** e **confiáveis**.
   - Caso o CPF não seja encontrado ou se o banco de dados não estiver carregado corretamente, a interface agora fornece mensagens claras de erro.

4. **Aparência Melhorada**:
   - A interface foi aprimorada com cores mais modernas e agradáveis.
   - O botão de atualização é agora ativado por um código secreto, aumentando a segurança e controle no uso.

---

## 📥 **Instalação**

### **Requisitos**
- Python 3.6+
- Dependências:
  - PyQt5
  - Pandas
  - Openpyxl

### **Instalação das dependências**
1. Clone o repositório:
   ```bash
   git clone https://github.com/JoaoGRSilva/Localizador-Excel.git
Navegue até a pasta do projeto:

bash
Copiar código
cd repositorio
Instale as dependências:

bash
Copiar código
pip install -r requirements.txt
Se preferir, crie um ambiente virtual:

bash
Copiar código
python -m venv venv
source venv/bin/activate  # no Linux/macOS
venv\Scripts\activate     # no Windows
🖥 Como usar
Executando o Aplicativo:

Para executar o aplicativo, basta rodar o arquivo main.py:
bash
Copiar código
python main.py
Pesquisa de CPF:

Digite um CPF válido na caixa de texto e clique em "Pesquisar" para encontrar as ofertas associadas a esse CPF.
Atualização de Banco de Dados:

O botão "Atualizar Base" estará oculto até que o código secreto seja digitado.
Após desbloquear o botão, selecione o arquivo Excel com os dados atualizados e o banco de dados será automaticamente convertido para o formato Parquet.

---

⚙️ Como funciona o banco de dados?
-O banco de dados é carregado no formato Parquet, o que permite uma leitura mais rápida e eficiente. Caso o arquivo dados.parquet não esteja disponível ou precise ser atualizado, o aplicativo permite importar dados de um arquivo Excel para gerar o banco de dados novamente.

---

🚀 Tecnologias Utilizadas
PyQt5: Para a interface gráfica do usuário (GUI).
Pandas: Para manipulação de dados e leitura/escrita do arquivo Parquet.
Excel (XLSX): Formato de arquivo usado para importar dados atualizados.

---

🐞 Problemas conhecidos
-A primeira vez que você abrir o aplicativo e não tiver um arquivo dados.parquet, ele tentará carregar um banco de dados vazio. Certifique-se de rodar a atualização da base de dados se necessário.

---

🤝 Contribuindo
-Contribuições são bem-vindas! Se você tiver melhorias, correções de bugs ou novas funcionalidades, sinta-se à vontade para abrir uma issue ou enviar um pull request.

Faça um fork deste repositório.
Crie uma nova branch (git checkout -b feature-nome-da-sua-feature).
Faça as alterações necessárias e commit com uma mensagem clara (git commit -am 'Adicionando nova funcionalidade').
Push para sua branch (git push origin feature-nome-da-sua-feature).
Abra um pull request explicando as mudanças realizadas.

---

📃 Licença
-Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.

---

👨‍💻 Autoria
-Desenvolvido por João Gabriel.
