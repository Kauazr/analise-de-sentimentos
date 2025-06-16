# CONTEÚDO ATUALIZADO DE: ml_model.py

import os
from joblib import load
from tkinter import messagebox
# MUDANÇA: Usando os caminhos completos do config
from config import MODELO_PATH, VETORIZADOR_PATH

modelo_global = None
vetorizador_global = None

def carregar_recursos_globais():
    global modelo_global, vetorizador_global
    print("DEBUG: Carregando recursos de ML...")
    # MUDANÇA: A verificação de existência agora usa os caminhos completos
    if not os.path.exists(MODELO_PATH) or not os.path.exists(VETORIZADOR_PATH):
        messagebox.showerror("Erro Crítico", "Arquivos de modelo não encontrados.")
        return False
    try:
        modelo_global = load(MODELO_PATH)
        vetorizador_global = load(VETORIZADOR_PATH)
        print("DEBUG: Modelo e vetorizador carregados.")
        return True
    except Exception as e:
        messagebox.showerror("Erro Crítico", f"Falha ao carregar modelo: {e}")
        return False
        
# ... O resto do arquivo ml_model.py continua exatamente o mesmo ...
def classificar_sentimento_core(frase):
    if not modelo_global or not vetorizador_global:
        messagebox.showerror("Erro", "Modelo de sentimento não carregado.")
        return "Indefinido"
    frase_limpa = [frase.lower().strip()]
    X_transformado = vetorizador_global.transform(frase_limpa)
    resultado_pred = modelo_global.predict(X_transformado)[0]
    mapa_sentimento = {0: 'Negativo', 1: 'Neutro', 2: 'Positivo'}
    return mapa_sentimento.get(resultado_pred, 'Desconhecido')