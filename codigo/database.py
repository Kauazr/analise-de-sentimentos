# CONTEÚDO ATUALIZADO DE: database.py

import sqlite3
from tkinter import messagebox
from config import DB_PATH # MUDANÇA: Usando DB_PATH em vez de DB_NAME

def conectar_db():
    try:
        conn = sqlite3.connect(DB_PATH) # MUDANÇA: Usando o caminho completo
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        print("DEBUG: Conectado ao SQLite com sucesso.")
        return conn
    except sqlite3.Error as err:
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ao SQLite: {err}")
        return None

# ... O resto do arquivo database.py continua exatamente o mesmo ...
def obter_categorias(conn):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT categoria_id, nome_categoria FROM Categorias ORDER BY nome_categoria")
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro DB", f"Erro ao buscar categorias: {e}")
        return []

def adicionar_produto(conn, categoria_id, nome_produto):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT produto_id FROM Produtos WHERE categoria_id = ? AND nome_produto = ?", (categoria_id, nome_produto))
            existente = cursor.fetchone()
            if existente:
                return existente['produto_id']
            
            cursor.execute("INSERT INTO Produtos (categoria_id, nome_produto) VALUES (?, ?)", (categoria_id, nome_produto))
        return cursor.lastrowid
    except sqlite3.Error as e:
        messagebox.showerror("Erro DB", f"Erro ao adicionar produto: {e}")
        return None

def obter_produtos_por_categoria(conn, categoria_id):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT produto_id, nome_produto FROM Produtos WHERE categoria_id = ? ORDER BY nome_produto", (categoria_id,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro DB", f"Erro ao buscar produtos: {e}")
        return []

def salvar_avaliacao_produto(conn, produto_id, texto_avaliacao, sentimento):
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
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sentimento_analisado, COUNT(*) as total FROM FrasesPesquisadas GROUP BY sentimento_analisado")
            return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Erro DB", f"Erro ao obter dados para relatório geral: {e}")
        return []

def obter_dados_relatorio_produtos_categoria(conn, categoria_id):
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