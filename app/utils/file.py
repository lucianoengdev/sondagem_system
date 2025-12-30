import json
import os

DATA_FILE = 'temp_data.json'
FILTERS_FILE = 'temp_filters.json'

def salvar_dados_temporarios(dados):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
        
    # Quando salvamos novos dados brutos, limpamos os filtros antigos
    salvar_filtros([]) 

def carregar_dados_temporarios():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def salvar_filtros(filtros):
    with open(FILTERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(filtros, f, ensure_ascii=False, indent=4)

def carregar_filtros():
    if os.path.exists(FILTERS_FILE):
        with open(FILTERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []