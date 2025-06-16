import sqlite3
import os

# MUDANÇA: Configuração para usar um arquivo de banco de dados SQLite
DB_NAME = "sentimentos.db"

script_dir = os.path.dirname(__file__)
SCHEMA_FILE = os.path.join(script_dir, "schema.sql")

def criar_e_popular_banco():
    # Remove o banco de dados antigo, se existir, para começar do zero
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Banco de dados '{DB_NAME}' antigo removido.")

    try:
        # Conecta ao banco (isso criará o arquivo se ele não existir)
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row # Para acessar colunas por nome
        cursor = conn.cursor()
        print(f"Banco de dados '{DB_NAME}' criado.")

        # Lê e executa o script de criação de tabelas
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
            schema_script = f.read()
        cursor.executescript(schema_script)
        print(f"Schema do arquivo '{SCHEMA_FILE}' executado.")
        conn.commit()

        # --- Inserção de dados ---
        print("\nPopulando categorias...")
        categorias_data = [
            ('Shampoo',), ('Condicionador',), ('Máscara Capilar',), ('Selagem',), ('Tintura',),
            ('Botox',), ('Progressiva',), ('Máscara de Hidratação',), ('Óleo',), ('Liven',),
            ('Reparador de Ponta',), ('Gel Finalizador',), ('Spray',), ('Pomada Capilar',)
        ]
        # MUDANÇA: Usando INSERT OR IGNORE para evitar erros de duplicatas
        cursor.executemany("INSERT OR IGNORE INTO Categorias (nome_categoria) VALUES (?)", categorias_data)
        conn.commit()
        print(f"{cursor.rowcount} categorias processadas.")

        # Buscar IDs das categorias inseridas
        cursor.execute("SELECT categoria_id, nome_categoria FROM Categorias")
        categorias_db = {cat['nome_categoria']: cat['categoria_id'] for cat in cursor.fetchall()}

        print("\nPopulando produtos...")
        produtos_data = [
            (categorias_db.get('Shampoo'), "Shampoo Hidratação Profunda LissEver"),
            (categorias_db.get('Shampoo'), "Shampoo Detox BrilhoTotal"),
            (categorias_db.get('Shampoo'), "Shampoo Força e Crescimento MaxHair"),
            (categorias_db.get('Condicionador'), "Condicionador Maciez Extrema SilkTouch"),
            (categorias_db.get('Condicionador'), "Condicionador Restauração Pós-Química Revive"),
            (categorias_db.get('Máscara Capilar'), "Máscara Reconstrução Total SOS Fios"),
            (categorias_db.get('Máscara Capilar'), "Máscara Nutrição Intensa Ouro Marroquino"),
            (categorias_db.get('Selagem'), "Selagem Térmica Efeito Liso Perfeito"),
            (categorias_db.get('Tintura'), "Tintura Cor Vibrante Chocolate Intenso"),
            (categorias_db.get('Tintura'), "Tintura Loiro Platinado Sem Amônia")
        ]
        cursor.executemany("INSERT OR IGNORE INTO Produtos (categoria_id, nome_produto) VALUES (?, ?)", produtos_data)
        conn.commit()
        print(f"{cursor.rowcount} produtos processados.")

        # Buscar IDs dos produtos inseridos
        cursor.execute("SELECT produto_id, nome_produto FROM Produtos")
        produtos_db = {prod['nome_produto']: prod['produto_id'] for prod in cursor.fetchall()}

        print("\nPopulando avaliações (exemplos)...")
        avaliacoes_data = [
            (produtos_db.get('Shampoo Hidratação Profunda LissEver'), "Deixou meu cabelo super macio e cheiroso, amei!", "positivo"),
            (produtos_db.get('Shampoo Hidratação Profunda LissEver'), "Realmente hidrata, senti a diferença na primeira lavagem.", "positivo"),
            (produtos_db.get('Shampoo Hidratação Profunda LissEver'), "Bom shampoo, mas esperava um pouco mais pelo preço.", "neutro"),
            (produtos_db.get('Shampoo Hidratação Profunda LissEver'), "Não vi muita diferença no meu cabelo, infelizmente.", "negativo"),
            (produtos_db.get('Shampoo Detox BrilhoTotal'), "Meu cabelo ficou com um brilho incrível, parece que limpou de verdade.", "positivo"),
            (produtos_db.get('Shampoo Detox BrilhoTotal'), "Achei que ressecou um pouco as pontas.", "negativo"),
            (produtos_db.get('Máscara Reconstrução Total SOS Fios'), "Salvou meu cabelo depois da descoloração! Milagrosa.", "positivo"),
            (produtos_db.get('Máscara Reconstrução Total SOS Fios'), "Recomendo para cabelos danificados, faz diferença.", "positivo"),
            (produtos_db.get('Tintura Cor Vibrante Chocolate Intenso'), "A cor ficou linda, exatamente como na caixa! Cobriu todos os brancos.", "positivo"),
            (produtos_db.get('Tintura Cor Vibrante Chocolate Intenso'), "A cor desbotou um pouco rápido para o meu gosto.", "negativo"),
            (produtos_db.get('Condicionador Maciez Extrema SilkTouch'), "Deixa o cabelo super sedoso, desembaraça fácil.", "positivo"),
            (produtos_db.get('Selagem Térmica Efeito Liso Perfeito'), "Alisou bem meu cabelo, reduziu o volume.", "positivo"),
        ]
        cursor.executemany("INSERT INTO AvaliacoesProdutos (produto_id, texto_avaliacao, sentimento) VALUES (?, ?, ?)", avaliacoes_data)
        conn.commit()
        print(f"{cursor.rowcount} avaliações de exemplo inseridas.")

        print("\n✨ Povoamento de dados de exemplo concluído! ✨")

    except sqlite3.Error as e:
        print(f"❌ ERRO durante o povoamento: {e}")
        if conn:
            conn.rollback() # Desfaz transações em caso de erro
    finally:
        if conn:
            conn.close()
            print("\nConexão com o banco de dados fechada.")

if __name__ == "__main__":
    confirmacao = input(f"Este script irá recriar e popular o banco de dados '{DB_NAME}' com dados de exemplo. Deseja continuar? (s/N): ")
    if confirmacao.lower() == 's':
        criar_e_popular_banco()
    else:
        print("Operação de povoamento cancelada pelo usuário.")