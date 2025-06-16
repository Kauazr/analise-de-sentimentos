# NOVO ARQUIVO: app.py (Principal)

import os
from tkinter import Tk, messagebox

# Importa os módulos que criamos
from interface import AppSentimentos
import database as db
import ml_model as ml
from config import DB_NAME

def main():
    """Função principal para iniciar a aplicação."""
    
    # 1. Verifica se o arquivo de banco de dados existe
    if not os.path.exists(DB_NAME):
        messagebox.showinfo("Banco de Dados não encontrado", 
                            f"O arquivo '{DB_NAME}' não foi encontrado.\n"
                            "Execute 'popular_banco.py' primeiro para criá-lo.")
        return # Encerra a aplicação se o DB não existir

    # 2. Carrega os modelos de Machine Learning
    if not ml.carregar_recursos_globais():
        return # Encerra se os modelos não puderem ser carregados

    # 3. Estabelece a conexão com o banco de dados
    conn = db.conectar_db()
    if not conn:
        return # Encerra se a conexão falhar

    # 4. Cria a janela principal do Tkinter
    root = Tk()

    # 5. Cria a instância da nossa interface, passando a janela e a conexão
    app_ui = AppSentimentos(root, conn)

    # 6. Inicia o loop principal da aplicação
    root.mainloop()

if __name__ == "__main__":
    main()