import os
import pymysql
from tkinter import Tk, Frame, Label as tkLabel, Button as tkButton, Text, messagebox, END, StringVar
from tkinter import ttk # Themed Tkinter widgets
from joblib import load
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np # Added for arranging bar positions in horizontal chart

# --- Configurações Globais ---
MODELO_PATH = 'modelo_sentimentos.joblib'
VETORIZADOR_PATH = 'vetorizador.joblib'

# Configurações do Banco de Dados (ajuste conforme necessário)
DB_HOST = "localhost"
DB_USER = "db_sentimentos"
DB_PASSWORD = "Db@senti"
DB_NAME = "tb_sentimentos"

# --- Cores para o Tema ---
BG_PRIMARY = '#2E3B4E'
BG_SECONDARY = '#3A4A5F'
FG_PRIMARY = '#E0E0E0'
ACCENT_PRIMARY = '#5D9CEC'
ACCENT_SUCCESS = '#62C462'
ACCENT_INFO = '#4A90E2'
ACCENT_WARNING = '#F5A623'
TEXT_INPUT_BG = '#4A5B70'
BORDER_COLOR = '#50637B'
BG_TREEVIEW_ODD_ROW = '#35455A'

# --- Carregamento do Modelo ---
modelo_global = None
vetorizador_global = None

def carregar_recursos_globais():
    global modelo_global, vetorizador_global
    # ... (código existente sem alterações) ...
    print("DEBUG: Dentro de carregar_recursos_globais(). Verificando arquivos...")
    if not os.path.exists(MODELO_PATH) or not os.path.exists(VETORIZADOR_PATH):
        msg = []
        if not os.path.exists(MODELO_PATH):
            msg.append(f"Arquivo do modelo NÃO ENCONTRADO em: {os.path.abspath(MODELO_PATH)}")
        if not os.path.exists(VETORIZADOR_PATH):
            msg.append(f"Arquivo do vetorizador NÃO ENCONTRADO em: {os.path.abspath(VETORIZADOR_PATH)}")
        full_msg = "\n".join(msg)
        print(f"ERRO CONSOLE: {full_msg}")
        messagebox.showerror("Erro Crítico", f"Não foi possível carregar arquivos essenciais:\n{full_msg}\nO programa será encerrado.")
        return False

    try:
        print("DEBUG: Arquivos encontrados. Tentando carregar modelo e vetorizador...")
        modelo_global = load(MODELO_PATH)
        vetorizador_global = load(VETORIZADOR_PATH)
        print("DEBUG: Modelo e vetorizador carregados com sucesso!")
        return True
    except Exception as e:
        print(f"ERRO CONSOLE: Falha ao carregar modelo/vetorizador: {e}")
        messagebox.showerror("Erro Crítico", f"Falha ao carregar modelo/vetorizador: {e}\nO programa será encerrado.")
        return False


# --- Conexão com o Banco de Dados ---
def conectar_db():
    # ... (código existente sem alterações) ...
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("DEBUG: Conectado ao MySQL com sucesso.")
        return conn
    except pymysql.MySQLError as err:
        print(f"❌ ERRO DB: Falha ao conectar ao banco de dados. Detalhes: {err}")
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ao MySQL: {err}")
        return None

# --- Funções Principais de Negócio ---
def classificar_sentimento_core(frase):
    # ... (código existente sem alterações) ...
    if not modelo_global or not vetorizador_global:
        messagebox.showerror("Erro", "Modelo de sentimento não carregado.")
        return "Indefinido"
    frase_limpa = [frase.lower().strip()]
    X_transformado = vetorizador_global.transform(frase_limpa)
    resultado_pred = modelo_global.predict(X_transformado)[0]
    mapa_sentimento = {0: 'Negativo', 1: 'Neutro', 2: 'Positivo'}
    return mapa_sentimento.get(resultado_pred, 'Desconhecido')

# --- Funções de Banco de Dados (CRUD e Consultas) ---
def obter_categorias(conn):
    # ... (código existente sem alterações) ...
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT categoria_id, nome_categoria FROM Categorias ORDER BY nome_categoria")
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        messagebox.showerror("Erro DB", f"Erro ao buscar categorias: {e}")
        return []

def adicionar_categoria(conn, nome_categoria):
    # ... (código existente sem alterações) ...
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO Categorias (nome_categoria) VALUES (%s)", (nome_categoria,))
        conn.commit()
        return cursor.lastrowid
    except pymysql.MySQLError as e:
        messagebox.showerror("Erro DB", f"Erro ao adicionar categoria: {e}")
        return None

def obter_produtos_por_categoria(conn, categoria_id):
    # ... (código existente sem alterações) ...
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT produto_id, nome_produto FROM Produtos WHERE categoria_id = %s ORDER BY nome_produto", (categoria_id,))
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        messagebox.showerror("Erro DB", f"Erro ao buscar produtos: {e}")
        return []

def adicionar_produto(conn, categoria_id, nome_produto):
    # ... (código existente sem alterações) ...
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT produto_id FROM Produtos WHERE categoria_id = %s AND nome_produto = %s", (categoria_id, nome_produto))
            existente = cursor.fetchone()
            if existente:
                return existente['produto_id']
            
            cursor.execute("INSERT INTO Produtos (categoria_id, nome_produto) VALUES (%s, %s)", (categoria_id, nome_produto))
        conn.commit()
        return cursor.lastrowid
    except pymysql.MySQLError as e:
        messagebox.showerror("Erro DB", f"Erro ao adicionar produto: {e}")
        return None

def salvar_avaliacao_produto(conn, produto_id, texto_avaliacao, sentimento):
    # ... (código existente sem alterações) ...
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO AvaliacoesProdutos (produto_id, texto_avaliacao, sentimento) VALUES (%s, %s, %s)",
                (produto_id, texto_avaliacao, sentimento.lower())
            )
        conn.commit()
        return True
    except pymysql.MySQLError as e:
        messagebox.showerror("Erro DB", f"Erro ao salvar avaliação do produto: {e}")
        return False

def salvar_frase_pesquisada(conn, texto_frase, sentimento_analisado, fonte="Manual"):
    # ... (código existente sem alterações) ...
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO FrasesPesquisadas (texto_frase, sentimento_analisado, fonte) VALUES (%s, %s, %s)",
                (texto_frase, sentimento_analisado.lower(), fonte)
            )
        conn.commit()
        return True
    except pymysql.MySQLError as e:
        messagebox.showerror("Erro DB", f"Erro ao salvar frase pesquisada: {e}")
        return False

def obter_dados_relatorio_geral(conn):
    # ... (código existente sem alterações) ...
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT sentimento_analisado, COUNT(*) as total FROM FrasesPesquisadas GROUP BY sentimento_analisado")
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        messagebox.showerror("Erro DB", f"Erro ao obter dados para relatório geral: {e}")
        return []

def obter_dados_relatorio_produtos_categoria(conn, categoria_id):
    # ... (código existente sem alterações) ...
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT p.nome_produto, ap.sentimento, COUNT(ap.avaliacao_id) as total
            FROM AvaliacoesProdutos ap
            JOIN Produtos p ON ap.produto_id = p.produto_id
            WHERE p.categoria_id = %s
            GROUP BY p.nome_produto, ap.sentimento
            ORDER BY p.nome_produto, ap.sentimento;
            """
            cursor.execute(sql, (categoria_id,))
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        messagebox.showerror("Erro DB", f"Erro ao obter dados para relatório de produtos: {e}")
        return []

# --- Lógica da Interface Gráfica ---
class AppSentimentos:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("VisageStats Pro - Análise de Sentimentos 💇")
        self.root.geometry("850x800") # Aumentei um pouco a altura para o gráfico horizontal
        self.root.configure(bg=BG_PRIMARY)

        self.setup_estilos()

        if not carregar_recursos_globais():
            self.root.destroy()
            return

        self.conn = conectar_db()
        if not self.conn:
            self.root.destroy()
            return
        
        self.categorias_dict = {}
        self.categoria_selecionada_var = StringVar(self.root)
        self.produtos_para_categoria_atual = []
        self.produto_selecionado_ou_novo_var = StringVar(self.root)
        
        self.ordenacao_relatorio_produtos_var = StringVar(self.root)


        self.setup_ui()
        self.carregar_dados_iniciais_ui()

    def setup_estilos(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam') #

        self.style.configure('.', background=BG_PRIMARY, foreground=FG_PRIMARY, font=('Arial', 10)) #
        self.style.configure('TFrame', background=BG_PRIMARY) #
        self.style.configure('TLabel', background=BG_PRIMARY, foreground=FG_PRIMARY, font=('Arial', 11)) #
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold')) #
        
        self.style.configure('TNotebook', background=BG_PRIMARY, borderwidth=0) #
        self.style.configure('TNotebook.Tab', background=BG_SECONDARY, foreground=FG_PRIMARY, padding=[10, 5], font=('Arial', 10, 'bold')) #
        self.style.map('TNotebook.Tab',
            background=[('selected', ACCENT_PRIMARY), ('active', BG_SECONDARY)],
            foreground=[('selected', FG_PRIMARY), ('active', FG_PRIMARY)]
        ) #

        self.style.configure('TButton', foreground='white', font=('Arial', 10, 'bold'), padding=6, borderwidth=1) #
        self.style.map('TButton',
            background=[('active', ACCENT_PRIMARY), ('pressed', BG_SECONDARY), ('!disabled', ACCENT_PRIMARY)], 
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
        ) #
        self.style.configure('Success.TButton', background=ACCENT_SUCCESS, foreground='white') #
        self.style.configure('Info.TButton', background=ACCENT_INFO, foreground='white') #
        self.style.configure('Warning.TButton', background=ACCENT_WARNING, foreground='black') #

        self.style.configure('TEntry', fieldbackground=TEXT_INPUT_BG, foreground=FG_PRIMARY, bordercolor=BORDER_COLOR, insertcolor=FG_PRIMARY) #
        
        # --- ESTILO COMBOBOX ATUALIZADO ---
        self.style.configure('TCombobox', 
                             fieldbackground=TEXT_INPUT_BG, #
                             bordercolor=BORDER_COLOR, #
                             arrowcolor=FG_PRIMARY, #
                             padding=4
                             ) #
        self.style.map('TCombobox',
            foreground=[
                ('readonly', FG_PRIMARY), # Cor do texto principal no estado readonly (QUANDO SELECIONADO E COM FOCO OU SEM FOCO)
                ('disabled', '#999999') # Cor do texto quando desabilitado
            ],
            fieldbackground=[
                ('readonly', TEXT_INPUT_BG) # Cor de fundo do campo de entrada no estado readonly
            ],
            selectbackground=[ # Cor de fundo do item selecionado NA LISTA SUSPENSA (dropdown)
                ('readonly', ACCENT_PRIMARY), 
                ('focus', ACCENT_PRIMARY) 
            ],
            selectforeground=[ # Cor do texto do item selecionado NA LISTA SUSPENSA (dropdown)
                ('readonly', FG_PRIMARY),
                ('focus', FG_PRIMARY)
            ]
        )
        # Estilos para a lista suspensa (Listbox)
        self.root.option_add('*TCombobox*Listbox.background', TEXT_INPUT_BG) #
        self.root.option_add('*TCombobox*Listbox.foreground', FG_PRIMARY) #
        self.root.option_add('*TCombobox*Listbox.selectBackground', ACCENT_PRIMARY) #
        self.root.option_add('*TCombobox*Listbox.selectForeground', FG_PRIMARY) #
        # --- FIM ESTILO COMBOBOX ---

        self.style.configure('Treeview', 
                             background=BG_SECONDARY, 
                             fieldbackground=BG_SECONDARY, 
                             foreground=FG_PRIMARY,
                             font=('Arial', 10),
                             rowheight=28) #
        self.style.configure('Treeview.Heading', 
                             background=ACCENT_PRIMARY, 
                             foreground='white', 
                             font=('Arial', 11, 'bold'), 
                             relief='flat',
                             padding=[5,5]) #
        self.style.map('Treeview.Heading', background=[('active', BG_SECONDARY)]) #

        self.style.configure('OddRow.Treeview', background=BG_TREEVIEW_ODD_ROW, foreground=FG_PRIMARY) #
        self.style.configure('EvenRow.Treeview', background=BG_SECONDARY, foreground=FG_PRIMARY) #
        
        self.text_widget_style = {'background': TEXT_INPUT_BG, 'foreground': FG_PRIMARY, 
                                  'font': ('Arial', 10), 'borderwidth': 1, 'relief': 'sunken',
                                  'insertbackground': FG_PRIMARY} #

    def setup_ui(self):
        # ... (código existente sem alterações) ...
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.tab_avaliar_produto = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_avaliar_produto, text='Avaliar Produto')
        self.criar_aba_avaliar_produto()

        self.tab_relatorio_produtos = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_relatorio_produtos, text='Relatório de Produtos')
        self.criar_aba_relatorio_produtos()

        self.tab_frases_pesquisa = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_frases_pesquisa, text='Adicionar Frases')
        self.criar_aba_frases_pesquisa()
        
        self.tab_relatorio_geral = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_relatorio_geral, text='Relatório Geral')
        self.criar_aba_relatorio_geral()

        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def carregar_dados_iniciais_ui(self):
        # ... (código existente sem alterações) ...
        categorias_data = obter_categorias(self.conn)
        self.categorias_dict = {cat['nome_categoria']: cat['categoria_id'] for cat in categorias_data}
        
        nomes_categorias = list(self.categorias_dict.keys())
        if nomes_categorias:
            self.categoria_selecionada_var.set(nomes_categorias[0])
            if hasattr(self, 'relatorio_categoria_combobox'): 
                 self.relatorio_categoria_combobox['values'] = nomes_categorias 
                 self.relatorio_categoria_selecionada_var.set(nomes_categorias[0]) 

        if hasattr(self, 'categoria_combobox'): 
            self.categoria_combobox['values'] = nomes_categorias 
            if nomes_categorias: 
                self.atualizar_produtos_combobox() 
        
        if hasattr(self, 'ordenacao_relatorio_produtos_combobox'): 
            self.ordenacao_relatorio_produtos_combobox['values'] = [
                "Produto (A-Z)", "Mais Positivas", "Mais Neutras", 
                "Mais Negativas", "Mais Avaliações"
            ]
            self.ordenacao_relatorio_produtos_var.set("Produto (A-Z)")


    def criar_aba_avaliar_produto(self):
        # ... (código existente sem alterações) ...
        frame = self.tab_avaliar_produto
        
        ttk.Label(frame, text="Avaliar Produto de Salão", style='Header.TLabel').pack(pady=20)

        ttk.Label(frame, text="Categoria do Produto:").pack(pady=(10,0))
        self.categoria_combobox = ttk.Combobox(frame, textvariable=self.categoria_selecionada_var, state='readonly', width=40, font=('Arial', 10))
        self.categoria_combobox.pack(pady=5)
        self.categoria_combobox.bind('<<ComboboxSelected>>', self.atualizar_produtos_combobox)

        ttk.Label(frame, text="Nome do Produto (digite um novo ou selecione):").pack(pady=(10,0))
        self.produto_combobox = ttk.Combobox(frame, textvariable=self.produto_selecionado_ou_novo_var, width=40, font=('Arial', 10))
        self.produto_combobox.pack(pady=5)

        ttk.Label(frame, text="Digite a avaliação do produto:").pack(pady=(10,0))
        self.avaliacao_produto_texto = Text(frame, height=6, width=60, **self.text_widget_style)
        self.avaliacao_produto_texto.pack(pady=5)

        self.btn_analisar_produto = ttk.Button(frame, text="Analisar e Salvar Avaliação", command=self.analisar_e_salvar_avaliacao_produto, style='Success.TButton')
        self.btn_analisar_produto.pack(pady=20)

        self.resultado_produto_label = ttk.Label(frame, text="Sentimento: ---", font=("Arial", 12))
        self.resultado_produto_label.pack(pady=10)

    def atualizar_produtos_combobox(self, event=None):
        # ... (código existente sem alterações) ...
        nome_cat_selecionada = self.categoria_selecionada_var.get()
        if not nome_cat_selecionada:
            self.produtos_para_categoria_atual = []
        else:
            categoria_id = self.categorias_dict.get(nome_cat_selecionada)
            if categoria_id:
                produtos_data = obter_produtos_por_categoria(self.conn, categoria_id) 
                self.produtos_para_categoria_atual = [prod['nome_produto'] for prod in produtos_data] 
                print(f"DEBUG UI: Produtos para '{nome_cat_selecionada}': {self.produtos_para_categoria_atual}")  
            else:
                self.produtos_para_categoria_atual = []
        
        self.produto_combobox['values'] = self.produtos_para_categoria_atual 
        if self.produtos_para_categoria_atual:
            self.produto_selecionado_ou_novo_var.set(self.produtos_para_categoria_atual[0]) 
        else:
            self.produto_selecionado_ou_novo_var.set("")


    def analisar_e_salvar_avaliacao_produto(self):
        # ... (código existente sem alterações) ...
        nome_categoria_selecionada = self.categoria_selecionada_var.get()
        nome_produto_input = self.produto_selecionado_ou_novo_var.get().strip()
        texto_avaliacao = self.avaliacao_produto_texto.get("1.0", END).strip()
        
        if not nome_categoria_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma categoria.")
            return
        if not nome_produto_input:
            messagebox.showwarning("Aviso", "Digite ou selecione o nome do produto.")
            return
        if not texto_avaliacao:
            messagebox.showwarning("Aviso", "Digite uma avaliação para o produto.")
            return

        categoria_id = self.categorias_dict.get(nome_categoria_selecionada)
        if not categoria_id:
            messagebox.showerror("Erro", "Categoria selecionada inválida.")
            return

        produto_id = adicionar_produto(self.conn, categoria_id, nome_produto_input) 

        if not produto_id:
            messagebox.showerror("Erro DB", f"Não foi possível obter/adicionar o produto '{nome_produto_input}'.")
            return

        sentimento = classificar_sentimento_core(texto_avaliacao) 
        self.resultado_produto_label.config(text=f"Sentimento: {sentimento.upper()}") 

        if salvar_avaliacao_produto(self.conn, produto_id, texto_avaliacao, sentimento): 
            messagebox.showinfo("Sucesso", f"Avaliação para '{nome_produto_input}' salva com sentimento: {sentimento.upper()}!")
            self.avaliacao_produto_texto.delete("1.0", END) 
            self.atualizar_produtos_combobox() 
        else:
            messagebox.showerror("Erro DB", "Falha ao salvar avaliação no banco de dados.")


    def criar_aba_relatorio_produtos(self): 
        frame = self.tab_relatorio_produtos 
        ttk.Label(frame, text="Relatório de Desempenho de Produtos", style='Header.TLabel').pack(pady=15) 

        controles_frame = ttk.Frame(frame, style='TFrame') 
        controles_frame.pack(pady=5, fill='x') #

        ttk.Label(controles_frame, text="Selecione a Categoria:").grid(row=0, column=0, padx=5, pady=5, sticky='w') 
        self.relatorio_categoria_selecionada_var = StringVar(frame) 
        self.relatorio_categoria_combobox = ttk.Combobox(controles_frame, textvariable=self.relatorio_categoria_selecionada_var, state='readonly', width=30, font=('Arial', 10)) 
        self.relatorio_categoria_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='ew') 

        ttk.Label(controles_frame, text="Ordenar por:").grid(row=1, column=0, padx=5, pady=5, sticky='w') 
        self.ordenacao_relatorio_produtos_combobox = ttk.Combobox(controles_frame, textvariable=self.ordenacao_relatorio_produtos_var, state='readonly', width=30, font=('Arial', 10)) 
        self.ordenacao_relatorio_produtos_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='ew') 
        self.ordenacao_relatorio_produtos_combobox.bind('<<ComboboxSelected>>', 
            lambda event: self.gerar_e_mostrar_relatorio_produtos() if self.relatorio_categoria_selecionada_var.get() else None)


        btn_gerar_rel_prod = ttk.Button(controles_frame, text="Gerar/Atualizar Relatório", command=self.gerar_e_mostrar_relatorio_produtos, style='Info.TButton') 
        btn_gerar_rel_prod.grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky='nswe') 
        
        controles_frame.columnconfigure(1, weight=1) 

        self.frame_grafico_prod = ttk.Frame(frame, style='TFrame') 
        self.frame_grafico_prod.pack(pady=10, fill="both", expand=True) 
        
        container_treeview_prod = ttk.Frame(frame, style='TFrame') 
        container_treeview_prod.pack(pady=10, fill="x", expand=False) 

        colunas = ("produto", "positivas", "neutras", "negativas", "total_avaliacoes") 
        self.tree_produtos = ttk.Treeview(container_treeview_prod, columns=colunas, show="headings", style='Treeview') 
        
        self.tree_produtos.heading("produto", text="Produto") 
        self.tree_produtos.heading("positivas", text="Positivas 👍") 
        self.tree_produtos.heading("neutras", text="Neutras 😐") 
        self.tree_produtos.heading("negativas", text="Negativas 👎") 
        self.tree_produtos.heading("total_avaliacoes", text="Total 🧮") 
        
        self.tree_produtos.column("produto", width=280, anchor='w') 
        self.tree_produtos.column("positivas", width=110, anchor='center') 
        self.tree_produtos.column("neutras", width=110, anchor='center') 
        self.tree_produtos.column("negativas", width=110, anchor='center') 
        self.tree_produtos.column("total_avaliacoes", width=100, anchor='center') 
        
        self.tree_produtos.pack(side="left", fill="x", expand=True) 
        
        scrollbar_prod = ttk.Scrollbar(container_treeview_prod, orient="vertical", command=self.tree_produtos.yview) 
        self.tree_produtos.configure(yscrollcommand=scrollbar_prod.set) 
        scrollbar_prod.pack(side="right", fill="y") 
        
        self.canvas_grafico_prod = None 


    def gerar_e_mostrar_relatorio_produtos(self): #
        nome_categoria_selecionada = self.relatorio_categoria_selecionada_var.get() #
        if not nome_categoria_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma categoria para gerar o relatório.") #
            return

        categoria_id = self.categorias_dict.get(nome_categoria_selecionada) #
        if not categoria_id:
            messagebox.showerror("Erro", "Categoria não encontrada.") #
            return

        dados_brutos = obter_dados_relatorio_produtos_categoria(self.conn, categoria_id) #

        if self.canvas_grafico_prod: #
            self.canvas_grafico_prod.get_tk_widget().destroy() #
            self.canvas_grafico_prod = None #
        
        for i in self.tree_produtos.get_children(): #
            self.tree_produtos.delete(i) #

        if not dados_brutos: #
            messagebox.showinfo("Relatório", f"Não há avaliações para produtos na categoria '{nome_categoria_selecionada}'.") #
            if self.canvas_grafico_prod: #
                self.canvas_grafico_prod.get_tk_widget().destroy() #
                self.canvas_grafico_prod = None #
            return

        dados_processados_tabela = {} #
        for row in dados_brutos: #
            produto = row['nome_produto'] #
            sentimento = row['sentimento'].capitalize() #
            total = row['total'] #
            if produto not in dados_processados_tabela: #
                dados_processados_tabela[produto] = {'Positivo': 0, 'Neutro': 0, 'Negativo': 0, 'Total': 0} #
            if sentimento in dados_processados_tabela[produto]: #
                 dados_processados_tabela[produto][sentimento] += total #
            dados_processados_tabela[produto]['Total'] += total #
            
        ordenacao_selecionada = self.ordenacao_relatorio_produtos_var.get() #
        
        lista_produtos_ordenada = list(dados_processados_tabela.items()) # 

        if ordenacao_selecionada == "Produto (A-Z)": #
            lista_produtos_ordenada.sort(key=lambda item: item[0]) # 
        elif ordenacao_selecionada == "Mais Positivas": #
            lista_produtos_ordenada.sort(key=lambda item: item[1].get('Positivo', 0), reverse=True) #
        elif ordenacao_selecionada == "Mais Neutras": #
            lista_produtos_ordenada.sort(key=lambda item: item[1].get('Neutro', 0), reverse=True) #
        elif ordenacao_selecionada == "Mais Negativas": #
            lista_produtos_ordenada.sort(key=lambda item: item[1].get('Negativo', 0), reverse=True) #
        elif ordenacao_selecionada == "Mais Avaliações": #
            lista_produtos_ordenada.sort(key=lambda item: item[1].get('Total', 0), reverse=True) #
        
        row_count = 0 #
        for produto, s_contagem in lista_produtos_ordenada: # 
            tag = 'EvenRow.Treeview' if row_count % 2 == 0 else 'OddRow.Treeview' #
            self.tree_produtos.insert("", "end", values=( #
                produto, s_contagem.get('Positivo',0), s_contagem.get('Neutro',0), #
                s_contagem.get('Negativo',0), s_contagem.get('Total',0) #
            ), tags=(tag,)) #
            row_count += 1 #

        # --- ATUALIZAÇÃO GRÁFICO PARA HORIZONTAL E TOP N ---
        MAX_PRODUCTS_FOR_GRAPH = 15 
        produtos_para_grafico_original_order = lista_produtos_ordenada[:MAX_PRODUCTS_FOR_GRAPH]
        
        # Para barh, é comum querer o item "maior" (ou primeiro na lista ordenada) no topo.
        # As barras são plotadas de baixo para cima (índice 0 na base).
        # Então, invertemos a lista para plotagem.
        produtos_para_grafico = produtos_para_grafico_original_order[::-1]

        nomes_produtos_graf = [item[0] for item in produtos_para_grafico]
        cont_p = np.array([item[1].get('Positivo',0) for item in produtos_para_grafico])
        cont_n = np.array([item[1].get('Neutro',0) for item in produtos_para_grafico])
        cont_ng = np.array([item[1].get('Negativo',0) for item in produtos_para_grafico])

        num_graf_prods = len(nomes_produtos_graf)
        if num_graf_prods == 0: # Segurança, embora já coberto pelo 'if not dados_brutos'
             if self.canvas_grafico_prod:
                self.canvas_grafico_prod.get_tk_widget().destroy()
                self.canvas_grafico_prod = None
             return

        # Altura dinâmica da figura
        fig_height_graph = max(3.5, min(12, 1.5 + num_graf_prods * 0.45)) # Ajuste a heurística conforme necessário

        fig = Figure(figsize=(7, fig_height_graph), dpi=100) #
        fig.patch.set_facecolor(BG_PRIMARY) #
        ax = fig.add_subplot(111) #
        ax.set_facecolor(BG_SECONDARY) #

        bar_height_single = 0.25 # Altura de uma única barra no grupo
        y_indices = np.arange(num_graf_prods) # Posições Y para cada grupo de barras de produto

        # Plotagem das barras agrupadas horizontalmente
        ax.barh(y_indices + bar_height_single, cont_p, bar_height_single, label='Positivas', color=ACCENT_SUCCESS)
        ax.barh(y_indices, cont_n, bar_height_single, label='Neutras', color=FG_PRIMARY)
        ax.barh(y_indices - bar_height_single, cont_ng, bar_height_single, label='Negativas', color=ACCENT_WARNING)
        
        ax.set_ylabel('Produtos', color=FG_PRIMARY, fontsize=9) #
        ax.set_xlabel('Nº Avaliações', color=FG_PRIMARY, fontsize=9) #
        
        title_text = f'Sentimentos em "{nome_categoria_selecionada}"'
        if len(lista_produtos_ordenada) > MAX_PRODUCTS_FOR_GRAPH:
            title_text = f'Top {MAX_PRODUCTS_FOR_GRAPH} Produtos (Sentimentos) em "{nome_categoria_selecionada}"'
        ax.set_title(title_text, color=FG_PRIMARY, fontsize=10) #
        
        ax.set_yticks(y_indices) #
        ax.set_yticklabels(nomes_produtos_graf, color=FG_PRIMARY, fontsize=8) #
        ax.tick_params(axis='x', colors=FG_PRIMARY, labelsize=8) #
        ax.tick_params(axis='y', colors=FG_PRIMARY, labelsize=8) # (já coberto por set_yticklabels)
        
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)) # Garante ticks inteiros para contagens

        leg = ax.legend(fontsize=8) #
        for text in leg.get_texts(): text.set_color(FG_PRIMARY) #
        
        ax.spines['bottom'].set_color(FG_PRIMARY) #
        ax.spines['top'].set_color(BG_SECONDARY)  # Menos destaque para topo
        ax.spines['right'].set_color(BG_SECONDARY) # Menos destaque para direita
        ax.spines['left'].set_color(FG_PRIMARY) #
        
        fig.tight_layout(pad=1.2) # Ajusta o layout para evitar sobreposições

        self.canvas_grafico_prod = FigureCanvasTkAgg(fig, master=self.frame_grafico_prod) #
        self.canvas_grafico_prod.draw() #
        self.canvas_grafico_prod.get_tk_widget().pack(side="top", fill="both", expand=True) #
        # --- FIM ATUALIZAÇÃO GRÁFICO ---


    def criar_aba_frases_pesquisa(self):
        # ... (código existente sem alterações) ...
        frame = self.tab_frases_pesquisa 
        ttk.Label(frame, text="Adicionar Frases de Pesquisa", style='Header.TLabel').pack(pady=20) 

        ttk.Label(frame, text="Digite ou cole a frase/avaliação encontrada:").pack(pady=(10,0)) 
        self.frase_pesquisada_texto = Text(frame, height=8, width=70, **self.text_widget_style) 
        self.frase_pesquisada_texto.pack(pady=5) 
        
        self.btn_analisar_frase_pesq = ttk.Button(frame, text="Analisar e Salvar Frase", command=self.analisar_e_salvar_frase_pesquisada, style='Warning.TButton') 
        self.btn_analisar_frase_pesq.pack(pady=20) 

        self.resultado_frase_pesq_label = ttk.Label(frame, text="Sentimento: ---", font=("Arial", 12)) 
        self.resultado_frase_pesq_label.pack(pady=10) 
        
    def analisar_e_salvar_frase_pesquisada(self):
        # ... (código existente sem alterações) ...
        texto_frase = self.frase_pesquisada_texto.get("1.0", END).strip() 
        if not texto_frase:
            messagebox.showwarning("Aviso", "Digite uma frase para analisar.") 
            return

        sentimento = classificar_sentimento_core(texto_frase) 
        self.resultado_frase_pesq_label.config(text=f"Sentimento: {sentimento.upper()}") 

        if salvar_frase_pesquisada(self.conn, texto_frase, sentimento): 
            messagebox.showinfo("Sucesso", f"Frase pesquisada salva com sentimento: {sentimento.upper()}!") 
            self.frase_pesquisada_texto.delete("1.0", END) 
        else:
            messagebox.showerror("Erro DB", "Falha ao salvar frase pesquisada no banco de dados.") 


    def criar_aba_relatorio_geral(self):
        # ... (código existente sem alterações) ...
        frame = self.tab_relatorio_geral 
        ttk.Label(frame, text="Relatório Geral de Frases Pesquisadas", style='Header.TLabel').pack(pady=20) 
        
        btn_gerar_rel_geral = ttk.Button(frame, text="Gerar Relatório Geral", command=self.gerar_e_mostrar_relatorio_geral, style='Info.TButton') 
        btn_gerar_rel_geral.pack(pady=15) 
        
        self.frame_grafico_geral = ttk.Frame(frame, style='TFrame') 
        self.frame_grafico_geral.pack(pady=10, fill="both", expand=True) 
        self.canvas_grafico_geral = None 


    def gerar_e_mostrar_relatorio_geral(self):
        # ... (código existente sem alterações) ...
        dados = obter_dados_relatorio_geral(self.conn) 
        if self.canvas_grafico_geral: 
            self.canvas_grafico_geral.get_tk_widget().destroy() 
            self.canvas_grafico_geral = None 
        if not dados: 
            messagebox.showinfo("Relatório", "Não há frases pesquisadas suficientes para gerar o relatório.") 
            return

        sentimentos_map = {d['sentimento_analisado'].capitalize(): d['total'] for d in dados} 
        labels = list(sentimentos_map.keys()) 
        sizes = list(sentimentos_map.values()) 
        
        pie_colors = [] 
        for label in labels: 
            if label == 'Positivo': pie_colors.append(ACCENT_SUCCESS) 
            elif label == 'Negativo': pie_colors.append(ACCENT_WARNING) 
            elif label == 'Neutro': pie_colors.append('#888888') 
            else: pie_colors.append(ACCENT_INFO) 

        fig = Figure(figsize=(6,5), dpi=100) 
        fig.patch.set_facecolor(BG_PRIMARY) 
        ax = fig.add_subplot(111) 

        wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.1f%%',  
                                          startangle=140, colors=pie_colors, 
                                          pctdistance=0.85) 
        for text_obj in texts: text_obj.set_color(FG_PRIMARY) 
        for autotext_obj in autotexts: autotext_obj.set_color('black') 

        ax.set_title('Distribuição de Sentimentos (Frases Pesquisadas)', color=FG_PRIMARY) 
        ax.axis('equal') 
        
        legend_labels = [f'{l}: {s:.1f}%' for l, s in zip(labels, (100.*val/sum(sizes) if sum(sizes) > 0 else 0 for val in sizes))] 
        leg = ax.legend(wedges, legend_labels, title="Sentimentos", loc="center left",  
                   bbox_to_anchor=(0.9, 0, 0.5, 1), facecolor=BG_SECONDARY, edgecolor=BORDER_COLOR) 
        for text_obj in leg.get_texts(): text_obj.set_color(FG_PRIMARY) 
        leg.get_title().set_color(FG_PRIMARY) 
        fig.tight_layout() 

        self.canvas_grafico_geral = FigureCanvasTkAgg(fig, master=self.frame_grafico_geral) 
        self.canvas_grafico_geral.draw() 
        self.canvas_grafico_geral.get_tk_widget().pack(side="top", fill="both", expand=True) 

    def ao_fechar(self):
        # ... (código existente sem alterações) ...
        print("DEBUG: Fechando aplicação...") 
        if self.conn: 
            self.conn.close() 
            print("DEBUG: Conexão com o banco de dados fechada.") 
        self.root.destroy() 

# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    root = Tk() #
    app = AppSentimentos(root) #
    if hasattr(app, 'conn') and app.conn is not None and modelo_global is not None : #
         root.mainloop() #
    else:
        print("ERRO CRÍTICO FINAL: Não foi possível iniciar a UI devido a falhas anteriores.") #