# CONTEÚDO ATUALIZADO DE: app.py (Principal)

import os
from tkinter import Tk, messagebox
from config import DB_PATH, BG_PRIMARY # MUDANÇA: Usando DB_PATH
from interface import AppSentimentos
from login import LoginWindow
import database as db
import ml_model as ml

class ApplicationController:
    # ... (sem alterações no ApplicationController) ...
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()
        self.login_window = None
        self.db_conn = None
    def start(self):
        # MUDANÇA: Verifica a existência do DB_PATH
        if not os.path.exists(DB_PATH):
            messagebox.showerror("Erro Crítico", f"O arquivo '{os.path.basename(DB_PATH)}' não foi encontrado.\nExecute 'popular_banco.py' primeiro.")
            return
        if not ml.carregar_recursos_globais():
            return
        self.db_conn = db.conectar_db()
        if not self.db_conn:
            return
        self.show_login_screen()
        self.root.mainloop()
    def show_login_screen(self):
        self.root.title("Login - VisageStats Pro")
        self.root.geometry("400x300")
        self.root.configure(bg=BG_PRIMARY)
        self.login_window = LoginWindow(self.root, on_login_success=self.on_login_success)
        self.root.deiconify()
    def on_login_success(self, user_role):
        if self.login_window:
            self.login_window.destroy()
        main_app = AppSentimentos(self.root, self.db_conn, user_role)

def main():
    controller = ApplicationController()
    controller.start()

if __name__ == "__main__":
    main()