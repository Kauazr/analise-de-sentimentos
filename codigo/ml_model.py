# ARQUIVO: ml_model.py
"""
Módulo responsável pela lógica de Machine Learning.
Ele carrega os modelos treinados e fornece uma função para classificar
o sentimento de novas frases.
"""

import os
from joblib import load
from tkinter import messagebox
from config import MODELO_PATH, VETORIZADOR_PATH

# Variáveis globais para armazenar os modelos carregados e evitar recarregá-los
modelo_global = None
vetorizador_global = None

def carregar_recursos_globais():
    """
    Carrega o modelo e o vetorizador do disco para a memória.
    Essa função é chamada uma vez, no início da aplicação.
    """
    global modelo_global, vetorizador_global
    print("DEBUG: Carregando recursos de ML...")
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

def classificar_sentimento_core(frase):
    """
    Recebe uma string, a processa e retorna seu sentimento previsto.
    1. Limpa e formata a frase.
    2. Usa o vetorizador para transformá-la em números.
    3. Usa o modelo para prever o sentimento.
    4. Mapeia o resultado numérico para um texto ('Positivo', 'Neutro', 'Negativo').
    """
    if not modelo_global or not vetorizador_global:
        messagebox.showerror("Erro", "Modelo de sentimento não carregado.")
        return "Indefinido"
        
    frase_limpa = [frase.lower().strip()]
    X_transformado = vetorizador_global.transform(frase_limpa)
    resultado_pred = modelo_global.predict(X_transformado)[0]
    
    mapa_sentimento = {0: 'Negativo', 1: 'Neutro', 2: 'Positivo'}
    return mapa_sentimento.get(resultado_pred, 'Desconhecido')