import math
import re
from .file import carregar_segmentos, carregar_dados_temporarios, salvar_estatisticas, carregar_filtros
from .filters import aplicar_filtros

def safe_float(val, default=None):
    if val is None or val == '': return default
    try:
        return float(str(val).replace(',', '.'))
    except:
        return default

def get_estaca_num(estaca_str):
    match = re.search(r'^(\d+)', str(estaca_str).strip())
    return int(match.group(1)) if match else -1

def calcular_estatisticas_segmentos():
    # 1. Carrega dados
    dados_brutos = carregar_dados_temporarios()
    filtros = carregar_filtros()
    dados_filtrados = aplicar_filtros(dados_brutos, filtros)
    segmentos = carregar_segmentos()

    if not segmentos: return None

    relatorio = []

    # Estrutura: key = chave no JSON do PDF, label = Nome Visual
    parametros = [
        {'group': 'Índices Físicos', 'rows': [
            {'key': 'll', 'label': 'LL'},
            {'key': 'ip', 'label': 'IP'}
        ]},
        {'group': 'Granulometria', 'rows': [
            {'key': 'g_val_0', 'label': '# 2"', 'is_gran': True},
            {'key': 'g_val_1', 'label': '# 1 1/2"', 'is_gran': True},
            {'key': 'g_val_2', 'label': '# 1"', 'is_gran': True},
            {'key': 'g_val_3', 'label': '# 3/4"', 'is_gran': True},
            {'key': 'g_val_4', 'label': '# 3/8"', 'is_gran': True},
            {'key': 'g_val_5', 'label': '# 4', 'is_gran': True},
            {'key': 'g_val_6', 'label': '# 10', 'is_gran': True},
            {'key': 'g_val_7', 'label': '# 16', 'is_gran': True},
            {'key': 'g_val_8', 'label': '# 30', 'is_gran': True},
            {'key': 'g_val_9', 'label': '# 40', 'is_gran': True},
            {'key': 'g_val_10', 'label': '# 50', 'is_gran': True},
            {'key': 'g_val_11', 'label': '# 100', 'is_gran': True},
            {'key': 'g_val_12', 'label': '# 200', 'is_gran': True}
        ]},
        {'group': 'Compactação', 'rows': [
            {'key': 'comp_h', 'label': 'Umidade (%)'}, 
            {'key': 'comp_ys', 'label': 'D. Máx. γs (g/cm³)', 'precision': 3},
            {'key': 'exp', 'label': 'Expansão (%)'},
            {'key': 'isc', 'label': 'ISC (%)'},
            {'key': 'isc', 'label': 'ISC % (em relação a ótima)'}
        ]}
    ]

    flat_params = []
    for grupo in parametros:
        for row in grupo['rows']:
            flat_params.append(row)

    for seg in segmentos:
        inicio, fim = seg['inicio'], seg['fim']
        
        valores_por_parametro = {p['label']: [] for p in flat_params}
        
        memoria_calculo = []
        
        count_furos = 0

        for furo in dados_filtrados:
            for amostra in furo['amostras']:
                if not amostra.get('num') or not re.match(r'^\d', str(amostra.get('num'))):
                    continue

                estaca = get_estaca_num(amostra.get('estaca', ''))
                
                dentro = False
                if seg['id'] == len(segmentos):
                    if inicio <= estaca <= fim: dentro = True
                else:
                    if inicio <= estaca < fim: dentro = True
                
                if dentro:
                    count_furos += 1
                    
                    linha_memoria = {
                        'furo': amostra.get('num'),
                        'estaca': amostra.get('estaca'),
                        'prof': amostra.get('prof'),
                        'trb': amostra.get('trb')
                    }

                    for p in flat_params:
                        val = None
                        
                        if p.get('is_gran'):
                            idx = int(p['key'].split('_')[-1])
                            try:
                                raw_val = amostra['g_val'][idx]
                                val = safe_float(raw_val)
                                if val is None: val = 100.0 
                            except:
                                val = 100.0
                        else:
                            val = safe_float(amostra.get(p['key']))
                        
                        if val is not None:
                            valores_por_parametro[p['label']].append(val)
                            linha_memoria[p['key']] = val
                        else:
                            linha_memoria[p['key']] = "-"
                    
                    memoria_calculo.append(linha_memoria)

        # Calcula Estatísticas
        grupos_calculados = []
        
        for grupo in parametros:
            rows_calc = []
            for p in grupo['rows']:
                vals = valores_por_parametro[p['label']]
                n = len(vals)
                
                media = 0
                desvio = 0
                xmin = 0
                umin = 0
                xmax = 0
                
                casas = p.get('precision', 2)

                if n > 0:
                    media = sum(vals) / n
                    if n > 1:
                        variancia = sum((x - media) ** 2 for x in vals) / (n - 1)
                        desvio = math.sqrt(variancia)
                    else:
                        desvio = 0
                    
                    termo1 = (1.29 * desvio) / math.sqrt(n)
                    termo2 = 0.68 * desvio
                    
                    xmin = media - termo1 - termo2
                    umin = media - termo1
                    xmax = media + termo1 + termo2

                    if n == 1:
                        xmin = media
                        xmax = media
                
                fmt = f"{{:.{casas}f}}"
                
                rows_calc.append({
                    'label': p['label'],
                    'media': fmt.format(media).replace('.', ',') if n > 0 else "-",
                    'desvio': fmt.format(desvio).replace('.', ',') if n > 0 else "-",
                    'n': n,
                    'n_display': count_furos,
                    'xmin': fmt.format(xmin).replace('.', ',') if n > 0 else "-",
                    'umin': fmt.format(umin).replace('.', ',') if n > 0 else "-",
                    'xmax': fmt.format(xmax).replace('.', ',') if n > 0 else "-"
                })
            
            grupos_calculados.append({
                'group_name': grupo['group'],
                'rows': rows_calc
            })

        relatorio.append({
            'id': seg['id'],
            'inicio': seg['inicio'],
            'fim': seg['fim'],
            'grupos': grupos_calculados,
            'memoria': memoria_calculo   
        })

    salvar_estatisticas(relatorio)
    return relatorio