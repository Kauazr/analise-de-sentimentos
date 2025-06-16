# ARQUIVO: config.py
"""
Módulo para centralizar todas as configurações e constantes da aplicação.
Isso facilita a manutenção, pois qualquer ajuste de cor, caminho ou usuário
é feito em um único lugar.
"""

import os

# --- LÓGICA DE CAMINHOS ---
# Crio caminhos absolutos para garantir que o programa encontre seus arquivos
# não importa de qual diretório ele seja executado.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "sentimentos.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")
MODELO_PATH = os.path.join(BASE_DIR, 'modelo_sentimentos.joblib')
VETORIZADOR_PATH = os.path.join(BASE_DIR, 'vetorizador.joblib')

# --- USUÁRIOS E PERMISSÕES ---
# Defino os usuários, senhas e seus perfis de acesso.
# 'programmer' tem acesso total, 'client' tem acesso restrito.
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

# --- PALETA DE CORES PARA O TEMA ---
# Defino todas as cores da interface aqui para manter um padrão visual.
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