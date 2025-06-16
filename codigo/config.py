# CONTEÚDO ATUALIZADO DE: config.py

import os

# --- LÓGICA DE CAMINHOS ---
# Pega o caminho absoluto para o diretório onde este arquivo (config.py) está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cria caminhos completos e robustos para cada arquivo
DB_PATH = os.path.join(BASE_DIR, "sentimentos.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")
MODELO_PATH = os.path.join(BASE_DIR, 'modelo_sentimentos.joblib')
VETORIZADOR_PATH = os.path.join(BASE_DIR, 'vetorizador.joblib')

# --- USUÁRIOS E PERMISSÕES ---
# (Sem alterações aqui)
USERS = {
    "admin": {
        "password": "admin",
        "role": "programmer"
    },
    "cliente": {
        "password": "123",
        "role": "client"
    }
}

# --- Cores para o Tema ---
# (Sem alterações aqui)
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