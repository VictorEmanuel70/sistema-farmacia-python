import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="farmaciapaguepouco",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.Cursor
)

def menu():
    while True:
        print("0. para Sair")
        print("1. para Procurar Produtos")
        print("2. Para Cadastrar Produtos")
        print("3. Para cadastrar Farmacêuticos")
        print("4. Para cadastrar Clientes")
        print("5. para consultar o estoque")
        print("6. para Registrar uma venda")
        print("7. Para gerar um relatório")
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite um número válido.")
            continue

        match opcao:
            case 1:
                ProcurarProdutos()
            case 2:
                CadastrarProduto()
            case 3:
                CadastrarFarmaceutico()
            case 4:
                CadastrarCliente()
            case 5:
                ControleEstoque()
            case 6:
                Venda()
            case 7:
                Relatorios()
            case 0:
                print("Fim.")
                break
            case _:
                print("Opção inválida.")

def ProcurarProdutos():
    cursor = connection.cursor()
    try:
        produto = int(input("Entre com 1 para procurar pelo nome ou 2 para procurar usando o composto do produto: "))
    except ValueError:
        print("Opção inválida.")
        cursor.close()
        return

    if produto == 1:
        procurar = input("Entre com o nome do produto: ")
        cursor.execute("SELECT * FROM Produtos WHERE Nome LIKE %s", ("%" + procurar + "%",))
    elif produto == 2:
        procurar = input("Entre com o composto do produto: ")
        cursor.execute("SELECT * FROM Produtos WHERE Composto LIKE %s", ("%" + procurar + "%",))
    else:
        print("Opção inválida.")
        cursor.close()
        return

    resultado = cursor.fetchall()
    if not resultado:
        print("Nenhum produto encontrado.")
    else:
        for x in resultado:
            print(x)
    cursor.close()

def CadastrarProduto():
    cursor = connection.cursor()
    nome = input("Nome do produto: ")
    composto = input("Composto do produto: ")
    dataValidade = input("Validade do produto('AAAA-MM-DD'): ")
    try:
        quantidadeEstoque = int(input("Quantidade em estoque: "))
        valorCompra = float(input("Valor da compra: "))
        valorVenda = float(input("Valor de Venda: "))
    except ValueError:
        print("Quantidade/valor inválido.")
        cursor.close()
        return

    cursor.execute(
        "INSERT INTO Produtos (Nome, Composto, DataValidade, QuantidadeEstoque, ValorCompra, ValorVenda) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (nome, composto, dataValidade, quantidadeEstoque, valorCompra, valorVenda)
    )
    connection.commit()
    print("Produto cadastrado.")
    cursor.close()

def CadastrarFarmaceutico():
    cursor = connection.cursor()
    nome = input("Nome do Farmacêutico: ")
    cpf = input("CPF: ")
    datanasc = input("Data de Nascimento (AAAA-MM-DD): ")
    telefone = input("Telefone: ")
    cursor.execute(
        "INSERT INTO Farmaceutico (Nome, CPF, DataNasc, Telefone) VALUES (%s, %s, %s, %s)",
        (nome, cpf, datanasc, telefone)
    )
    connection.commit()
    print("Farmacêutico cadastrado.")
    cursor.close()

def CadastrarCliente():
    cursor = connection.cursor()
    nome = input("Nome do Cliente: ")
    cpf = input("CPF: ")
    datanasc = input("Data de Nascimento (AAAA-MM-DD): ")
    telefone = input("Telefone: ")
    endereco = input("Endereço: ")
    cursor.execute(
        "INSERT INTO Cliente (Nome, CPF, DataNasc, Telefone, Endereco) VALUES (%s, %s, %s, %s, %s)",
        (nome, cpf, datanasc, telefone, endereco)
    )
    connection.commit()
    print("Cliente cadastrado.")
    cursor.close()

def ControleEstoque():
    cursor = connection.cursor()
    try:
        idproduto = int(input("Id do Produto: "))
        novaquantidade = int(input("Nova quantidade em estoque: "))
    except ValueError:
        print("Id ou quantidade inválida.")
        cursor.close()
        return

    cursor.execute('UPDATE Produtos SET QuantidadeEstoque = %s WHERE idProdutos = %s', (novaquantidade, idproduto))
    connection.commit()
    print("Quantidade de estoque atualizada com sucesso.")
    cursor.close()

def Venda():
    cursor = connection.cursor()

    try:
        idcliente = int(input("ID Cliente: "))
        idfarmaceutico = int(input("ID Farmacêutico: "))
        idproduto = int(input("ID Produto: "))
        quantidade = int(input("Quantidade: "))
    except ValueError:
        print("IDs/quantidade inválidos.")
        cursor.close()
        return

    datavenda = input("Data da Venda (AAAA-MM-DD): ")

    # busca dados do produto (use tupla com vírgula)
    cursor.execute("SELECT Nome, ValorVenda, QuantidadeEstoque FROM Produtos WHERE idProdutos = %s", (idproduto,))
    produto = cursor.fetchone()
    if not produto:
        print("Produto não encontrado.")
        cursor.close()
        return

    nomeproduto = produto[0]
    try:
        valorvenda = float(produto[1])
    except (TypeError, ValueError):
        print("Preço do produto inválido.")
        cursor.close()
        return

    try:
        quantidadeestoque = int(produto[2])
    except (TypeError, ValueError):
        quantidadeestoque = 0

    if quantidade > quantidadeestoque:
        print(f"Estoque insuficiente para o produto {nomeproduto}. Disponível: {quantidadeestoque}")
        cursor.close()
        return

    valortotal = valorvenda * quantidade
    novoestoque = quantidadeestoque - quantidade

    cursor.execute("UPDATE Produtos SET QuantidadeEstoque = %s WHERE idProdutos = %s", (novoestoque, idproduto))
    cursor.execute(
        "INSERT INTO Vendas (Preco, DataVenda, Farmaceutico_idFarmaceutico, Cliente_idCliente) VALUES (%s, %s, %s, %s)",
        (valortotal, datavenda, idfarmaceutico, idcliente)
    )

    idvenda = cursor.lastrowid  
    cursor.execute(
        "INSERT INTO Vendas_has_Produtos (Vendas_idVendas, Vendas_Farmaceutico_idFarmaceutico, Vendas_Cliente_idCliente, Produtos_idProdutos, QuantidadeProduto) VALUES (%s, %s, %s, %s, %s)",
        (idvenda, idfarmaceutico, idcliente, idproduto, quantidade)
    )

    connection.commit()

    print(" Cupom Fiscal ")
    print(f"Nome do Produto: {nomeproduto}")
    print(f"Quantidade: {quantidade}")
    print(f"Valor Total: R${valortotal:.2f}")
    print("Venda registrada!")

    cursor.close()

def Relatorios():
    cursor = connection.cursor()
    print("Escolha o relatório que você quer gerar:")
    print("1. Nome dos produtos e a quantidade disponível no estoque")
    print("2. Vendas realizadas em uma data específica")
    print("3. Detalhes de uma venda específica")
    try:
        opcao = int(input("Digite o número da opção: "))
    except ValueError:
        print("Opção inválida.")
        cursor.close()
        return

    match opcao:
        case 1:
            cursor.execute("SELECT Nome, QuantidadeEstoque FROM Produtos")
            produtos = cursor.fetchall()
            print("Produtos em Estoque:")
            for produto in produtos:
                print(f"Nome: {produto[0]}, Quantidade: {produto[1]}")
        case 2:
            datavenda = input("Digite a data da venda (AAAA-MM-DD): ")
            cursor.execute(
                """SELECT Vendas.DataVenda, Cliente.Nome, Farmaceutico.Nome
                   FROM Vendas
                   JOIN Cliente ON Vendas.Cliente_idCliente = Cliente.idCliente
                   JOIN Farmaceutico ON Vendas.Farmaceutico_idFarmaceutico = Farmaceutico.idFarmaceutico
                   WHERE Vendas.DataVenda = %s""",
                (datavenda,)
            )
            vendas = cursor.fetchall()
            print(f"Vendas realizadas em {datavenda}:")
            for venda in vendas:
                print(f"Data: {venda[0]}, Cliente: {venda[1]}, Farmacêutico: {venda[2]}")
        case 3:
            try:
                idvenda = int(input("Digite o ID da venda: "))
            except ValueError:
                print("ID inválido.")
                cursor.close()
                return
            cursor.execute(
                """SELECT Produtos.Nome, Produtos.ValorVenda, Vendas_has_Produtos.QuantidadeProduto
                   FROM Vendas_has_Produtos
                   JOIN Produtos ON Vendas_has_Produtos.Produtos_idProdutos = Produtos.idProdutos
                   WHERE Vendas_has_Produtos.Vendas_idVendas = %s""",
                (idvenda,)
            )
            produtosvendidos = cursor.fetchall()
            print(f"Detalhes da Venda {idvenda}:")
            for produto in produtosvendidos:
                print(f"Produto: {produto[0]}, Preço unitário: R${produto[1]}, Quantidade: {produto[2]}")
        case _:
            print("Opção inválida.")
    cursor.close()

if __name__ == "__main__":
    try:
        menu()
    finally:
        connection.close()

