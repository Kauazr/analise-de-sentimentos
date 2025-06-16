# ARQUIVO: database.py
"""
Este módulo concentra todas as funções que interagem diretamente
com o banco de dados SQLite. Manter isso separado organiza o projeto.
"""

import sqlite3
from tkinter import messagebox
from config import DB_PATH

def conectar_db():
    """
    Cria e retorna uma conexão com o banco de dados SQLite.
    Também configuro o row_factory para que eu possa acessar os resultados
    como dicionários (ex: linha['coluna']) e habilito as chaves estrangeiras.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        print("DEBUG: Conexão com o SQLite bem-sucedida.")
        return conn
    except sqlite3.Error as err:
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ao SQLite: {err}")
        return None

# --- FUNÇÕES DE CONSULTA E MANIPULAÇÃO DE DADOS ---

def obter_categorias(conn):
    """Busca todas as categorias do banco, ordenadas por nome."""
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT categoria_id, nome_categoria FROM Categorias ORDER BY nome_categoria")
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro DB", f"Erro ao buscar categorias: {e}")
        return []

def adicionar_produto(conn, categoria_id, nome_produto):
    """
    Adiciona um novo produto ao banco. Primeiro, verifico se o produto já existe
    naquela categoria para não criar duplicatas.
    """
    try:
        with conn:
            cursor = conn.cursor()
            # Primeiro, verifico se o produto já existe para não duplicar
            cursor.execute("SELECT produto_id FROM Produtos WHERE categoria_id = ? AND nome_produto = ?", (categoria_id, nome_produto))
            existente = cursor.fetchone()
            if existente:
                return existente['produto_id']
            
            # Se não existe, eu insiro o novo produto
            cursor.execute("INSERT INTO Produtos (categoria_id, nome_produto) VALUES (?, ?)", (categoria_id, nome_produto))
        return cursor.lastrowid
    except sqlite3.Error as e:
        messagebox.showerror("Erro DB", f"Erro ao adicionar produto: {e}")
        return None

def obter_produtos_por_categoria(conn, categoria_id):
    """Retorna todos os produtos de uma categoria específica."""
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT produto_id, nome_produto FROM Produtos WHERE categoria_id = ? ORDER BY nome_produto", (categoria_id,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro DB", f"Erro ao buscar produtos: {e}")
        return []

def salvar_avaliacao_produto(conn, produto_id, texto_avaliacao, sentimento):
    """Salva uma nova avaliação de produto no banco de dados."""
    try:
        with conn:
            conn.execute(
                "INSERT INTO AvaliacoesProdutos (produto_id, texto_avaliacao, sentimento) VALUES (?, ?, ?)",
                (produto_id, texto_avaliacao, sentimento.lower())
            )
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Erro DB", f"Erro ao salvar avaliação do produto: {e}")
        return False

def salvar_frase_pesquisada(conn, texto_frase, sentimento_analisado, fonte="Manual"):
    """Salva uma frase genérica (não atrelada a produto) no banco."""
    try:
        with conn:
            conn.execute(
                "INSERT INTO FrasesPesquisadas (texto_frase, sentimento_analisado, fonte) VALUES (?, ?, ?)",
                (texto_frase, sentimento_analisado.lower(), fonte)
            )
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Erro DB", f"Erro ao salvar frase pesquisada: {e}")
        return False

def obter_dados_relatorio_geral(conn):
    """Busca os dados agregados para o relatório geral (pizza)."""
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sentimento_analisado, COUNT(*) as total FROM FrasesPesquisadas GROUP BY sentimento_analisado")
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro DB", f"Erro ao obter dados para relatório geral: {e}")
        return []

def obter_dados_relatorio_produtos_categoria(conn, categoria_id):
    """Busca dados agregados de produtos para o relatório de produtos (barras)."""
    try:
        with conn:
            cursor = conn.cursor()
            sql = """
            SELECT p.nome_produto, ap.sentimento, COUNT(ap.avaliacao_id) as total
            FROM AvaliacoesProdutos ap
            JOIN Produtos p ON ap.produto_id = p.produto_id
            WHERE p.categoria_id = ?
            GROUP BY p.nome_produto, ap.sentimento
            ORDER BY p.nome_produto, ap.sentimento;
            """
            cursor.execute(sql, (categoria_id,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro DB", f"Erro ao obter dados para relatório de produtos: {e}")
        return []