import pymysql

# --- Configurações do Banco de Dados (as mesmas do app.py) ---
DB_HOST = "localhost"
DB_USER = "db_sentimentos"
DB_PASSWORD = "Db@senti" # Sua senha
DB_NAME = "tb_sentimentos"

def conectar_db():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except pymysql.MySQLError as err:
        print(f"❌ ERRO DB: Falha ao conectar ao banco de dados. Detalhes: {err}")
        return None

def popular_dados():
    conn = conectar_db()
    if not conn:
        print("Não foi possível conectar ao banco para popular os dados.")
        return

    try:
        with conn.cursor() as cursor:
            print("Populando categorias...")
            categorias_data = [
                ("Shampoo",),
                ("Condicionador",),
                ("Máscara Capilar",),
                ("Selagem",),
                ("Tintura",)
            ]
            cursor.executemany("INSERT INTO Categorias (nome_categoria) VALUES (%s) ON DUPLICATE KEY UPDATE nome_categoria=nome_categoria;", categorias_data)
            conn.commit()
            print(f"{cursor.rowcount} categorias processadas.")

            # Buscar IDs das categorias inseridas
            cursor.execute("SELECT categoria_id, nome_categoria FROM Categorias")
            categorias_db = {cat['nome_categoria']: cat['categoria_id'] for cat in cursor.fetchall()}

            print("\nPopulando produtos...")
            produtos_data = [
                # Shampoos
                (categorias_db['Shampoo'], "Shampoo Hidratação Profunda LissEver"),
                (categorias_db['Shampoo'], "Shampoo Detox BrilhoTotal"),
                (categorias_db['Shampoo'], "Shampoo Força e Crescimento MaxHair"),
                # Condicionadores
                (categorias_db['Condicionador'], "Condicionador Maciez Extrema SilkTouch"),
                (categorias_db['Condicionador'], "Condicionador Restauração Pós-Química Revive"),
                # Máscaras
                (categorias_db['Máscara Capilar'], "Máscara Reconstrução Total SOS Fios"),
                (categorias_db['Máscara Capilar'], "Máscara Nutrição Intensa Ouro Marroquino"),
                # Selagens
                (categorias_db['Selagem'], "Selagem Térmica Efeito Liso Perfeito"),
                # Tinturas
                (categorias_db['Tintura'], "Tintura Cor Vibrante Chocolate Intenso"),
                (categorias_db['Tintura'], "Tintura Loiro Platinado Sem Amônia")
            ]
            cursor.executemany("INSERT INTO Produtos (categoria_id, nome_produto) VALUES (%s, %s) ON DUPLICATE KEY UPDATE nome_produto=nome_produto;", produtos_data)
            conn.commit()
            print(f"{cursor.rowcount} produtos processados.")

            # Buscar IDs dos produtos inseridos
            cursor.execute("SELECT produto_id, nome_produto FROM Produtos")
            produtos_db = {prod['nome_produto']: prod['produto_id'] for prod in cursor.fetchall()}

            print("\nPopulando avaliações (exemplos)...")
            avaliacoes_data = [
                # Shampoo Hidratação Profunda LissEver
                (produtos_db['Shampoo Hidratação Profunda LissEver'], "Deixou meu cabelo super macio e cheiroso, amei!", "Positivo"),
                (produtos_db['Shampoo Hidratação Profunda LissEver'], "Realmente hidrata, senti a diferença na primeira lavagem.", "Positivo"),
                (produtos_db['Shampoo Hidratação Profunda LissEver'], "Bom shampoo, mas esperava um pouco mais pelo preço.", "Neutro"),
                (produtos_db['Shampoo Hidratação Profunda LissEver'], "Não vi muita diferença no meu cabelo, infelizmente.", "Negativo"),
                (produtos_db['Shampoo Hidratação Profunda LissEver'], "Excelente! Comprarei novamente com certeza.", "Positivo"),
                (produtos_db['Shampoo Hidratação Profunda LissEver'], "A textura é ótima e faz bastante espuma.", "Positivo"),

                # Shampoo Detox BrilhoTotal
                (produtos_db['Shampoo Detox BrilhoTotal'], "Meu cabelo ficou com um brilho incrível, parece que limpou de verdade.", "Positivo"),
                (produtos_db['Shampoo Detox BrilhoTotal'], "Gostei do efeito detox, senti o couro cabeludo mais leve.", "Positivo"),
                (produtos_db['Shampoo Detox BrilhoTotal'], "É um bom shampoo, cumpre o que promete.", "Positivo"),
                (produtos_db['Shampoo Detox BrilhoTotal'], "Achei que ressecou um pouco as pontas.", "Negativo"),
                (produtos_db['Shampoo Detox BrilhoTotal'], "O cheiro é refrescante, muito bom.", "Positivo"),

                # Máscara Reconstrução Total SOS Fios
                (produtos_db['Máscara Reconstrução Total SOS Fios'], "Salvou meu cabelo depois da descoloração! Milagrosa.", "Positivo"),
                (produtos_db['Máscara Reconstrução Total SOS Fios'], "Textura densa, rende bastante e o resultado é ótimo.", "Positivo"),
                (produtos_db['Máscara Reconstrução Total SOS Fios'], "Máscara muito boa, mas o cheiro não me agradou tanto.", "Neutro"),
                (produtos_db['Máscara Reconstrução Total SOS Fios'], "Deixou meu cabelo um pouco pesado, talvez eu tenha usado demais.", "Negativo"),
                (produtos_db['Máscara Reconstrução Total SOS Fios'], "Recomendo para cabelos danificados, faz diferença.", "Positivo"),
                (produtos_db['Máscara Reconstrução Total SOS Fios'], "Meu cabelo ficou mais forte e menos quebradiço.", "Positivo"),

                # Tintura Cor Vibrante Chocolate Intenso
                (produtos_db['Tintura Cor Vibrante Chocolate Intenso'], "A cor ficou linda, exatamente como na caixa! Cobriu todos os brancos.", "Positivo"),
                (produtos_db['Tintura Cor Vibrante Chocolate Intenso'], "Fácil de aplicar e não ressecou meu cabelo.", "Positivo"),
                (produtos_db['Tintura Cor Vibrante Chocolate Intenso'], "A cor desbotou um pouco rápido para o meu gosto.", "Negativo"),
                (produtos_db['Tintura Cor Vibrante Chocolate Intenso'], "Gostei da tonalidade, ficou bem natural.", "Positivo"),
                (produtos_db['Tintura Cor Vibrante Chocolate Intenso'], "O cheiro é forte, mas o resultado compensa.", "Neutro"),
                (produtos_db['Tintura Cor Vibrante Chocolate Intenso'], "Cobertura perfeita e brilho intenso.", "Positivo"),
            ]
            # Adicionando mais algumas avaliações para outros produtos para ter mais dados
            avaliacoes_data.extend([
                (produtos_db['Condicionador Maciez Extrema SilkTouch'], "Deixa o cabelo super sedoso, desembaraça fácil.", "Positivo"),
                (produtos_db['Condicionador Maciez Extrema SilkTouch'], "Cheiro maravilhoso e resultado incrível.", "Positivo"),
                (produtos_db['Condicionador Maciez Extrema SilkTouch'], "Bom, mas nada de extraordinário.", "Neutro"),
                (produtos_db['Selagem Térmica Efeito Liso Perfeito'], "Alisou bem meu cabelo, reduziu o volume.", "Positivo"),
                (produtos_db['Selagem Térmica Efeito Liso Perfeito'], "O processo é um pouco demorado, mas vale a pena.", "Positivo"),
                (produtos_db['Selagem Térmica Efeito Liso Perfeito'], "Não durou tanto quanto eu esperava o efeito liso.", "Negativo"),
            ])

            cursor.executemany("INSERT INTO AvaliacoesProdutos (produto_id, texto_avaliacao, sentimento) VALUES (%s, %s, %s)", avaliacoes_data)
            conn.commit()
            print(f"{cursor.rowcount} avaliações de exemplo inseridas.")

            print("\n✨ Povoamento de dados de exemplo concluído! ✨")

    except pymysql.MySQLError as e:
        print(f"❌ ERRO durante o povoamento: {e}")
        conn.rollback() # Desfaz transações em caso de erro
    finally:
        if conn:
            conn.close()
            print("\nConexão com o banco de dados fechada.")

if __name__ == "__main__":
    # CUIDADO: Este script irá inserir dados.
    # Considere fazer um backup do seu banco se ele já tiver dados importantes.
    confirmacao = input("Este script irá popular o banco de dados com dados de exemplo. Deseja continuar? (s/N): ")
    if confirmacao.lower() == 's':
        # Primeiro, vamos garantir que as tabelas existem
        # (O ideal seria ter um script de migração separado, mas para simplificar...)
        conn_check = conectar_db()
        if conn_check:
            try:
                with conn_check.cursor() as cursor_check:
                    print("Verificando/Criando tabelas necessárias...")
                    cursor_check.execute("""
                    CREATE TABLE IF NOT EXISTS Categorias (
                        categoria_id INT AUTO_INCREMENT PRIMARY KEY,
                        nome_categoria VARCHAR(100) UNIQUE NOT NULL
                    );""")
                    cursor_check.execute("""
                    CREATE TABLE IF NOT EXISTS Produtos (
                        produto_id INT AUTO_INCREMENT PRIMARY KEY,
                        categoria_id INT,
                        nome_produto VARCHAR(255) NOT NULL,
                        UNIQUE KEY idx_cat_prod (categoria_id, nome_produto), -- Para evitar duplicatas exatas de produto na categoria
                        FOREIGN KEY (categoria_id) REFERENCES Categorias(categoria_id) ON DELETE CASCADE
                    );""")
                    cursor_check.execute("""
                    CREATE TABLE IF NOT EXISTS AvaliacoesProdutos (
                        avaliacao_id INT AUTO_INCREMENT PRIMARY KEY,
                        produto_id INT,
                        texto_avaliacao TEXT NOT NULL,
                        sentimento VARCHAR(50) NOT NULL,
                        data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (produto_id) REFERENCES Produtos(produto_id) ON DELETE CASCADE
                    );""")
                    cursor_check.execute("""
                    CREATE TABLE IF NOT EXISTS FrasesPesquisadas (
                        frase_id INT AUTO_INCREMENT PRIMARY KEY,
                        texto_frase TEXT NOT NULL,
                        sentimento_analisado VARCHAR(50),
                        fonte VARCHAR(255) DEFAULT 'Manual',
                        data_adicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );""")
                conn_check.commit()
                print("Estrutura de tabelas verificada/criada.")
            except pymysql.MySQLError as e_struct:
                print(f"Erro ao verificar/criar estrutura de tabelas: {e_struct}")
            finally:
                conn_check.close()
            
            # Agora, popular os dados
            popular_dados()
        else:
            print("Não foi possível conectar para verificar/criar tabelas.")
    else:
        print("Operação de povoamento cancelada pelo usuário.")