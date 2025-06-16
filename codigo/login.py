# NOVO ARQUIVO: login.py

from tkinter import Frame, Label, Entry, Button, messagebox, ttk
from config import BG_PRIMARY, FG_PRIMARY, TEXT_INPUT_BG, ACCENT_PRIMARY, USERS

class LoginWindow(Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master, bg=BG_PRIMARY)
        self.on_login_success = on_login_success

        # Centraliza o frame de login na janela
        self.place(relx=0.5, rely=0.5, anchor="center")

        style = ttk.Style()
        style.configure('Login.TButton', font=('Arial', 10, 'bold'), padding=6)
        style.map('Login.TButton',
            background=[('active', ACCENT_PRIMARY), ('!disabled', ACCENT_PRIMARY)],
            foreground=[('active', 'white'), ('!disabled', 'white')]
        )
        
        Label(self, text="Login", font=('Arial', 18, 'bold'), bg=BG_PRIMARY, fg=FG_PRIMARY).pack(pady=20)
        
        # Frame para os campos de entrada
        frame_entries = Frame(self, bg=BG_PRIMARY)
        frame_entries.pack(pady=10, padx=30)
        
        Label(frame_entries, text="Usuário:", bg=BG_PRIMARY, fg=FG_PRIMARY).grid(row=0, column=0, sticky='w', pady=5)
        self.user_entry = Entry(frame_entries, bg=TEXT_INPUT_BG, fg=FG_PRIMARY, font=('Arial', 10), width=30, insertbackground=FG_PRIMARY, relief='flat')
        self.user_entry.grid(row=0, column=1, pady=5)
        
        Label(frame_entries, text="Senha:", bg=BG_PRIMARY, fg=FG_PRIMARY).grid(row=1, column=0, sticky='w', pady=5)
        self.pass_entry = Entry(frame_entries, bg=TEXT_INPUT_BG, fg=FG_PRIMARY, font=('Arial', 10), width=30, show="*", insertbackground=FG_PRIMARY, relief='flat')
        self.pass_entry.grid(row=1, column=1, pady=5)

        self.login_button = ttk.Button(self, text="Entrar", command=self._attempt_login, style='Login.TButton', width=20)
        self.login_button.pack(pady=30)

        # Permite pressionar Enter para logar
        self.master.bind('<Return>', lambda event: self._attempt_login())

    def _attempt_login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()

        user_data = USERS.get(username)

        if user_data and user_data["password"] == password:
            messagebox.showinfo("Sucesso", f"Login bem-sucedido! Bem-vindo(a), {username}.")
            # Chama a função de callback passando o perfil do usuário
            self.on_login_success(user_data["role"])
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")