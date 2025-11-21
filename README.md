# 💊 Sistema de Farmácia - Pague Pouco

Este projeto foi desenvolvido por Victor Emanuel no curso de Desenvolvimento de Sistemas.

O objetivo é criar um sistema de gerenciamento para uma farmácia, utilizando Python para o desenvolvimento do sistema e MySQL como banco de dados.

---

## 📌 Funcionalidades

- Cadastro de **Produtos**, **Clientes** e **Farmacêuticos**
- Controle de **Estoque**
- Registro de **Vendas**
- Geração de **Relatórios**:
  - Produtos em estoque
  - Vendas por data
  - Detalhes de uma venda

---

## 🛠 Tecnologias usadas

- Python 3
- pymysql
- MySQL Workbench

---

## 🗂 Como usar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/SEU-USUARIO/farmacia-pague-pouco.git
   ```

2. **Configure o banco de dados**:
   - Abra o arquivo `banco_farmacia.sql` no MySQL Workbench e execute os comandos para criar as tabelas e inserir os dados.

3. **Ajuste a conexão** no arquivo `sistema_farmacia.py` caso seu MySQL tenha usuário/senha diferente:
   ```python
   connection = pymysql.connect(
       host="localhost",
       user="root",
       password="root",
       database="farmaciapaguepouco",
   )
   ```

4. **Execute o sistema**:
   ```bash
   python sistema_farmacia.py
   ```

---

## 👨‍💻 Autor

- Victor Emanuel Neres do Valle
