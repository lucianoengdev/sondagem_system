import json
import os

DATA_FILE = 'temp_data.json'
FILTERS_FILE = 'temp_filters.json'

def salvar_dados_temporarios(dados):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
        
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

LINEAR_FILE = 'temp_linear.json'

def salvar_dados_linear(dados):
    """Salva o 'snapshot' dos dados para o gráfico linear."""
    with open(LINEAR_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar_dados_linear():
    """Lê os dados congelados. Se não existir, retorna None."""
    if os.path.exists(LINEAR_FILE):
        with open(LINEAR_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None