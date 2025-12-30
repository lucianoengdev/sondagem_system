import re

def parse_float_br(valor_str):
    """Converte '12,5' ou '12.5' para float 12.5. Retorna None se falhar."""
    if not valor_str: return None
    try:
        clean = str(valor_str).replace(',', '.').strip()
        return float(clean)
    except:
        return None

def extract_first_int(valor_str):
    """Pega '8 / 4,0m' e retorna 8. Pega '15 AM-1' e retorna 15."""
    if not valor_str: return None
    try:
        # Regex para pegar o primeiro número inteiro encontrado no início
        match = re.search(r'^(\d+)', str(valor_str).strip())
        if match:
            return int(match.group(1))
    except:
        pass
    return None

def parse_profundidade(prof_str, tipo):
    """
    tipo: 'INICIAL', 'FINAL', 'ESPESSURA'
    Espera string '0,08 - 1,00'
    """
    if not prof_str or '-' not in str(prof_str): return None
    try:
        partes = str(prof_str).split('-')
        ini = parse_float_br(partes[0])
        fim = parse_float_br(partes[1])
        
        if tipo == 'INICIAL': return ini
        if tipo == 'FINAL': return fim
        if tipo == 'ESPESSURA': return fim - ini
    except:
        return None
    return None

def aplicar_filtros(dados_originais, filtros):
    """
    Aplica filtros de exclusão.
    REGRA DE OURO: Só analisa linhas onde a coluna 'FURO/AMOSTRA' (num) é um número.
    Ignora linhas de continuação, rodapés internos ou linhas vazias.
    """
    if not filtros:
        return dados_originais

    dados_validos = []

    for furo in dados_originais:
        manter_furo = True
        
        for amostra in furo['amostras']:
            
            # --- TRAVA DE SEGURANÇA (A Lógica que você pediu) ---
            # Verifica se essa linha é uma "Linha Principal" (tem número na coluna A)
            # Se não tiver número (ex: vazia ou texto solto), IGNORA COMPLETAMENTE.
            # Isso impede que o "-" do TRB na linha de baixo cause exclusão falsa.
            id_amostra = extract_first_int(amostra.get('num'))
            if id_amostra is None:
                continue 

            # Se passou da trava, é uma linha de dados válida. Vamos filtrar.
            for filtro in filtros:
                coluna = filtro['coluna']
                op = filtro['operador']
                valor_usuario = filtro['valor']
                
                # 1. Parsing dos dados
                valor_dado = None
                
                if coluna == 'FURO/AMOSTRA':
                    valor_dado = id_amostra # Já extraímos lá em cima
                    valor_usuario = parse_float_br(valor_usuario)
                    
                elif coluna == 'ESTACA':
                    valor_dado = extract_first_int(amostra['estaca'])
                    valor_usuario = parse_float_br(valor_usuario)

                elif coluna == 'TRB':
                    raw_trb = amostra.get('trb', '')
                    valor_dado = str(raw_trb).strip().upper()
                    valor_usuario = str(valor_usuario).strip().upper()
                
                elif 'PROF.' in coluna:
                    tipo_prof = coluna.replace('PROF. ', '') 
                    valor_dado = parse_profundidade(amostra['prof'], tipo_prof)
                    valor_usuario = parse_float_br(valor_usuario)

                else:
                    mapa_simples = {
                        'L.L (%)': 'll', 'I.P (%)': 'ip', 'IG': 'ig', 
                        'h nat': 'hnat', 'COMP. h': 'comp_h', 'COMP. Ys': 'comp_ys',
                        'EXP (%)': 'exp', 'ISC (%)': 'isc', 'SIGMA': 'sigma'
                    }
                    chave = mapa_simples.get(coluna)
                    if chave:
                        valor_dado = parse_float_br(amostra.get(chave))
                    
                    valor_usuario = parse_float_br(valor_usuario)

                # Se o dado principal da linha válida estiver vazio, não compara
                if valor_dado in [None, "", " "]:
                    continue

                # 2. Comparação
                match = False
                
                if valor_usuario is None:
                    match = False
                else:
                    if coluna == 'TRB': 
                        if op == 'Igual': match = (valor_dado == valor_usuario)
                        elif op == 'Diferente': match = (valor_dado != valor_usuario)
                    else: # Lógica Numérica
                        if op == 'Maior': match = (valor_dado > valor_usuario)
                        elif op == 'Menor': match = (valor_dado < valor_usuario)
                        elif op == 'Maior ou igual': match = (valor_dado >= valor_usuario)
                        elif op == 'Menor ou igual': match = (valor_dado <= valor_usuario)
                        elif op == 'Igual': match = (valor_dado == valor_usuario)
                        elif op == 'Diferente': match = (valor_dado != valor_usuario)

                if match:
                    manter_furo = False
                    break # Sai dos filtros
            
            if not manter_furo: break # Sai das amostras

        if manter_furo:
            dados_validos.append(furo)

    return dados_validos