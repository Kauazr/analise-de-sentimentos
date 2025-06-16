# ARQUIVO: popular_banco.py
"""
Script utilitário para criar e popular o banco de dados do zero.

Ele lê a estrutura das tabelas do arquivo 'schema.sql' e depois
insere um conjunto de dados iniciais (categorias, produtos e avaliações)
para que a aplicação tenha informações para exibir desde o primeiro uso.
"""

import sqlite3
import os
from config import DB_PATH, SCHEMA_PATH

def criar_e_popular_banco():
    """
    Orquestra a criação e o povoamento do banco de dados.
    1. Remove o arquivo de banco de dados antigo para garantir um início limpo.
    2. Cria um novo arquivo de banco de dados e as tabelas a partir do schema.
    3. Insere os dados iniciais em cada tabela.
    """
    # Para garantir um início limpo, removo o banco de dados antigo se ele existir.
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Banco de dados '{os.path.basename(DB_PATH)}' antigo removido.")

    try:
        # Conecta ao banco (o que cria o arquivo .db se ele não existir).
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        print(f"Banco de dados '{os.path.basename(DB_PATH)}' criado.")

        # Leio e executo o arquivo schema.sql de uma vez para criar todas as tabelas.
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            schema_script = f.read()
        cursor.executescript(schema_script)
        print(f"Schema do arquivo '{os.path.basename(SCHEMA_PATH)}' executado.")
        conn.commit()

        # --- Inserção de Categorias ---
        print("\nPopulando categorias...")
        categorias_data = [
            ('Shampoo',), ('Condicionador',), ('Máscara Capilar',), ('Selagem',), ('Tintura',),
            ('Botox',), ('Progressiva',), ('Máscara de Hidratação',), ('Óleo',), ('Liven',),
            ('Reparador de Ponta',), ('Gel Finalizador',), ('Spray',), ('Pomada Capilar',)
        ]
        # Uso INSERT OR IGNORE para evitar erros caso tente inserir uma categoria que já existe.
        cursor.executemany("INSERT OR IGNORE INTO Categorias (nome_categoria) VALUES (?)", categorias_data)
        conn.commit()
        print(f"{cursor.rowcount} categorias processadas.")

        # --- Inserção de Produtos ---
        # Preciso dos IDs das categorias para criar a relação de chave estrangeira.
        cursor.execute("SELECT categoria_id, nome_categoria FROM Categorias")
        categorias_db = {cat['nome_categoria']: cat['categoria_id'] for cat in cursor.fetchall()}

        print("\nPopulando produtos...")
        produtos_data = [
            (categorias_db.get('Shampoo'), "Shampoo Hidratação Profunda LissEver"),
            (categorias_db.get('Shampoo'), "Shampoo Detox BrilhoTotal"),
            (categorias_db.get('Condicionador'), "Condicionador Maciez Extrema SilkTouch"),
            (categorias_db.get('Máscara Capilar'), "Máscara Reconstrução Total SOS Fios"),
            (categorias_db.get('Tintura'), "Tintura Cor Vibrante Chocolate Intenso"),
        ]
        cursor.executemany("INSERT OR IGNORE INTO Produtos (categoria_id, nome_produto) VALUES (?, ?)", produtos_data)
        conn.commit()
        print(f"{cursor.rowcount} produtos processados.")

        # --- Inserção de Avaliações de Exemplo ---
        # Da mesma forma, pego os IDs dos produtos para criar as avaliações.
        cursor.execute("SELECT produto_id, nome_produto FROM Produtos")
        produtos_db = {prod['nome_produto']: prod['produto_id'] for prod in cursor.fetchall()}

        print("\nPopulando avaliações (exemplos)...")
        avaliacoes_data = [
            (produtos_db.get('Shampoo Hidratação Profunda LissEver'), "Deixou meu cabelo super macio e cheiroso, amei!", "positivo"),
            (produtos_db.get('Shampoo Hidratação Profunda LissEver'), "Bom shampoo, mas esperava um pouco mais pelo preço.", "neutro"),
            (produtos_db.get('Shampoo Hidratação Profunda LissEver'), "Não vi muita diferença no meu cabelo, infelizmente.", "negativo"),
            (produtos_db.get('Shampoo Detox BrilhoTotal'), "Meu cabelo ficou com um brilho incrível, parece que limpou de verdade.", "positivo"),
            (produtos_db.get('Máscara Reconstrução Total SOS Fios'), "Salvou meu cabelo depois da descoloração! Milagrosa.", "positivo"),
            (produtos_db.get('Tintura Cor Vibrante Chocolate Intenso'), "A cor ficou linda, exatamente como na caixa! Cobriu todos os brancos.", "positivo"),
            (produtos_db.get('Tintura Cor Vibrante Chocolate Intenso'), "A cor desbotou um pouco rápido para o meu gosto.", "negativo"),
            (produtos_db.get('Condicionador Maciez Extrema SilkTouch'), "Deixa o cabelo super sedoso, desembaraça fácil.", "positivo"),
        ]
        cursor.executemany("INSERT INTO AvaliacoesProdutos (produto_id, texto_avaliacao, sentimento) VALUES (?, ?, ?)", avaliacoes_data)
        conn.commit()
        print(f"{cursor.rowcount} avaliações de exemplo inseridas.")

        print("\n✨ Povoamento de dados de exemplo concluído! ✨")

    except sqlite3.Error as e:
        print(f"❌ ERRO durante o povoamento: {e}")
        if conn:
            conn.rollback() # Desfaço as alterações em caso de erro
    finally:
        if conn:
            conn.close()
            print("\nConexão com o banco de dados fechada.")

# Este bloco só é executado quando o script é chamado diretamente (ex: python popular_banco.py)
if __name__ == "__main__":
    # Adiciono uma confirmação para evitar apagar o banco de dados por acidente.
    confirmacao = input(f"Este script irá recriar o banco de dados '{os.path.basename(DB_PATH)}'. Deseja continuar? (s/n): ")
    if confirmacao.lower() == 's':
        criar_e_popular_banco()
    else:
        print("Operação de povoamento cancelada pelo usuário.")