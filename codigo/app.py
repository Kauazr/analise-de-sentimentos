# ARQUIVO: app.py
"""
Ponto de entrada principal da aplicação.
Este script é responsável por orquestrar a inicialização:
1. Verifica os pré-requisitos (arquivos de DB e ML).
2. Mostra a tela de login.
3. Após o login, inicia a interface principal com o perfil correto.
"""

import os
from tkinter import Tk, messagebox

# Importo meus próprios módulos
from config import DB_PATH, BG_PRIMARY
from interface import AppSentimentos
from login import LoginWindow
import database as db
import ml_model as ml

class ApplicationController:
    """
    Classe que controla o fluxo da aplicação. Decidi usar uma classe aqui
    para organizar melhor o estado (janela raiz, conexão, etc.).
    """
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()  # Escondo a janela principal no início
        self.login_window = None
        self.db_conn = None

    def start(self):
        """Inicia os pré-requisitos e mostra a tela de login."""
        # Passo 1: Verificações iniciais
        if not os.path.exists(DB_PATH):
            messagebox.showerror("Erro Crítico", f"O arquivo '{os.path.basename(DB_PATH)}' não foi encontrado.\nExecute 'popular_banco.py' primeiro.")
            return
        if not ml.carregar_recursos_globais():
            return

        # Passo 2: Conexão com o banco de dados
        self.db_conn = db.conectar_db()
        if not self.db_conn:
            return
            
        # Passo 3: Exibição da tela de login
        self.show_login_screen()
        self.root.mainloop()

    def show_login_screen(self):
        """Prepara e exibe a janela de login."""
        self.root.title("Login - VisageStats Pro")
        self.root.geometry("400x300")
        self.root.configure(bg=BG_PRIMARY)
        
        # Crio a tela de login e passo a função 'on_login_success' como callback
        self.login_window = LoginWindow(self.root, on_login_success=self.on_login_success)
        self.root.deiconify() # Mostro a janela raiz, que agora contém o login

    def on_login_success(self, user_role):
        """
        Esta função é chamada pela tela de login quando o usuário acerta a senha.
        Ela recebe o perfil do usuário como argumento.
        """
        # Destruo a tela de login para liberar os recursos
        if self.login_window:
            self.login_window.destroy()

        # Crio a interface principal, passando a janela, a conexão e o perfil do usuário
        main_app = AppSentimentos(self.root, self.db_conn, user_role)

# Ponto de entrada padrão do Python
if __name__ == "__main__":
    controller = ApplicationController()
    controller.start()