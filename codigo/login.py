# ARQUIVO: login.py
"""
Módulo que define a classe da janela de login da aplicação.
"""

from tkinter import Frame, Label, Entry, Button, messagebox, ttk
from config import BG_PRIMARY, FG_PRIMARY, TEXT_INPUT_BG, ACCENT_PRIMARY, USERS

class LoginWindow(Frame):
    """
    Cria um Frame do Tkinter que contém os campos de usuário, senha e o botão de login.
    """
    def __init__(self, master, on_login_success):
        """
        Inicializa o frame de login.
        - master: A janela principal (root) onde este frame será colocado.
        - on_login_success: Uma função (callback) que será chamada quando o login for bem-sucedido.
                        É assim que a tela de login se comunica com o resto do app.
        """
        super().__init__(master, bg=BG_PRIMARY)
        self.on_login_success = on_login_success

        # Uso o 'place' para centralizar o frame na janela, fica mais bonito.
        self.place(relx=0.5, rely=0.5, anchor="center")

        # Configurações de estilo específicas para esta janela
        style = ttk.Style()
        style.configure('Login.TButton', font=('Arial', 10, 'bold'), padding=6)
        style.map('Login.TButton',
            background=[('active', ACCENT_PRIMARY), ('!disabled', ACCENT_PRIMARY)],
            foreground=[('active', 'white'), ('!disabled', 'white')]
        )
        
        Label(self, text="Login", font=('Arial', 18, 'bold'), bg=BG_PRIMARY, fg=FG_PRIMARY).pack(pady=20)
        
        # Crio um frame interno para alinhar os campos de entrada com grid
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

        # Facilidade para o usuário: permite logar pressionando a tecla Enter
        self.master.bind('<Return>', lambda event: self._attempt_login())

    def _attempt_login(self):
        """
        Pega os dados dos campos de entrada, verifica se são válidos e,
        em caso de sucesso, chama a função de callback `on_login_success`.
        """
        username = self.user_entry.get()
        password = self.pass_entry.get()

        user_data = USERS.get(username)

        # Verifico se o usuário existe e se a senha está correta
        if user_data and user_data["password"] == password:
            messagebox.showinfo("Sucesso", f"Login bem-sucedido! Bem-vindo(a), {username}.")
            # Chamo a função que foi passada no __init__, enviando o perfil do usuário
            self.on_login_success(user_data["role"])
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")