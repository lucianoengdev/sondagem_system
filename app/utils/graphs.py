import re

def try_int(val):
    try:
        return int(float(str(val).replace(',', '.')))
    except:
        return 0

def preparar_dados_linear(dados_filtrados):
    lista_linear = []

    for furo in dados_filtrados:
        for amostra in furo['amostras']:
            raw_num = str(amostra.get('num', '')).strip()
            
            # --- CORREÇÃO SOLICITADA ---
            # Só aceita se começar com um DÍGITO (0-9).
            # Ignora "Nº", "m", "%", "-", ou vazios.
            if not raw_num or not re.match(r'^\d', raw_num):
                continue

            # Tratamento da Estaca e Posição
            raw_estaca = str(amostra.get('estaca', ''))
            if '/' in raw_estaca:
                partes = raw_estaca.split('/', 1)
                estaca_val = partes[0].strip()
                posicao_val = partes[1].strip()
            else:
                estaca_val = raw_estaca.strip()
                posicao_val = "-"

            # Remove o "m" ou " m" se vier grudado no texto da posição
            posicao_val = posicao_val.replace('m', '').strip()

            item = {
                'furo': raw_num,
                'estaca_raw': estaca_val, 
                'estaca_sort': try_int(estaca_val),
                'posicao': posicao_val,
                'prof': amostra.get('prof'),
                'exp': amostra.get('exp'),
                'isc': amostra.get('isc'),
                'trb': str(amostra.get('trb', '')).strip().upper()
            }
            lista_linear.append(item)

    # Ordenação Crescente pela Estaca
    lista_linear.sort(key=lambda x: x['estaca_sort'])

    return lista_linear