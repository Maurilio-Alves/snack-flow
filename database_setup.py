import sqlite3

def carregar_dados_iniciais():
    # Conecta ao banco (se não existir, ele cria o arquivo)
    conn = sqlite3.connect('snackflow.db')
    cursor = conn.cursor()

    print("🛠️ Iniciando configuração do Banco de Dados...")

    # 1. TABELA DE PEDIDOS (Gestão da Produção)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            cliente TEXT, 
            lanche TEXT, 
            status TEXT, 
            hora_entrada DATETIME,
            total REAL DEFAULT 0
        )
    ''')
    
    # 2. TABELA DE PRODUTOS (Cardápio do Bilu Burger)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT, 
            categoria TEXT, 
            preco REAL
        )
    ''')

    # 3. TABELA DE CLIENTES (A que estava faltando!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT UNIQUE, 
            telefone TEXT, 
            endereco TEXT
        )
    ''')

    # 4. IMPORTAÇÃO DO CARDÁPIO (Apenas se a tabela estiver vazia)
    cursor.execute("SELECT count(*) FROM produtos")
    if cursor.fetchone()[0] == 0:
        print("🚚 Importando itens do cardápio...")
        cardapio = [
            ('Bilu Burguer', 'Artesanal', 37.50), ('Vegetariano', 'Artesanal', 30.00),
            ('X-Burguer Art', 'Artesanal', 27.50), ('X-Salada Art', 'Artesanal', 30.50),
            ('X-Bacon Art', 'Artesanal', 35.50), ('X-Milho Art', 'Artesanal', 30.50),
            ('X-Egg Art', 'Artesanal', 30.50), ('Cala Burguer Art', 'Artesanal', 35.00),
            ('Fran Burguer Art', 'Artesanal', 35.00), ('Americano Art', 'Artesanal', 35.00),
            ('X-Burguer Trad', 'Tradicional', 22.00), ('X-Salada Trad', 'Tradicional', 24.00),
            ('X-Bacon Trad', 'Tradicional', 31.50), ('X-Milho Trad', 'Tradicional', 24.00),
            ('X-Egg Trad', 'Tradicional', 24.00), ('Cala Burguer Trad', 'Tradicional', 29.00),
            ('Fran Burguer Trad', 'Tradicional', 29.00), ('Americano Trad', 'Tradicional', 30.00),
            ('Carnão', 'Variados', 33.00), ('Prensão', 'Variados', 27.50),
            ('X-Calabresa', 'Variados', 29.50), ('Cala Bacon', 'Variados', 31.50),
            ('X-Frango', 'Variados', 29.00), ('Cala Frango', 'Variados', 31.50),
            ('Fran Bacon', 'Variados', 31.50), ('Cachorro Quente', 'Variados', 15.00),
            ('Cachorro Duplo', 'Variados', 17.00), ('Cachorro Triplo C/ Queijo', 'Variados', 25.00),
            ('Refrigerante Lata', 'Bebidas', 6.00), ('Coca 1L', 'Bebidas', 11.00),
            ('Sucos Naturais', 'Bebidas', 6.00), ('Água sem gás', 'Bebidas', 3.00),
            ('Água com Gás', 'Bebidas', 4.00), ('Heineken Lata', 'Bebidas', 8.50),
            ('Adic. Hamb. Artesanal 150g', 'Adicionais', 11.00), ('Adic. Hamb. Vegetariano', 'Adicionais', 7.00),
            ('Adic. Hamb. Tradicional', 'Adicionais', 7.00), ('Adic. Bacon', 'Adicionais', 8.00),
            ('Adic. Presunto', 'Adicionais', 3.00), ('Adic. Queijo Mussarela', 'Adicionais', 8.00),
            ('Adic. Calabresa', 'Adicionais', 8.00), ('Adic. Frango Desfiado', 'Adicionais', 8.00),
            ('Adic. Salsicha', 'Adicionais', 2.00), ('Adic. Purê', 'Adicionais', 3.00),
            ('Adic. Milho', 'Adicionais', 4.00), ('Adic. Batata Palha', 'Adicionais', 3.00),
            ('Adic. Catupiry Original', 'Adicionais', 8.00), ('Adic. Cheddar Catupiry', 'Adicionais', 7.00),
            ('Adic. Molho BBQ', 'Adicionais', 2.50), ('Adic. Alface', 'Adicionais', 2.00),
            ('Adic. Ovo', 'Adicionais', 3.00)
        ]
        cursor.executemany("INSERT INTO produtos (nome, categoria, preco) VALUES (?, ?, ?)", cardapio)
        conn.commit()

    conn.close()
    print("✅ Banco de Dados SnackFlow (v5.0) configurado com sucesso!")

if __name__ == "__main__":
    carregar_dados_iniciais()