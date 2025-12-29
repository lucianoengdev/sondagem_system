import pdfplumber
import os

def clean_text(text):
    """Limpa texto removendo quebras de linha extras"""
    if text:
        return str(text).replace('\n', ' ').strip()
    return ""

def processar_furos(file_paths):
    dados_consolidados = []
    
    for path in file_paths:
        nome_arquivo = os.path.basename(path)
        
        furo_data = {
            "arquivo": nome_arquivo,
            "amostras": [],
            "rodape": {
                "linha1": "",
                "linha2": "",
                "linha3": ""
            }
        }

        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    # extract_table retorna uma lista de listas
                    tabelas = page.extract_table()
                    
                    if not tabelas: continue

                    for row in tabelas:
                        # Limpa cada célula da linha
                        row_limpa = [clean_text(x) for x in row]
                        texto_completo = " ".join(row_limpa).upper()

                        # --- 1. CAPTURA DO RODAPÉ (LINHAS MESCLADAS) ---
                        if "CLAS. CAMPO" in texto_completo or "CLASSIF. LAB" in texto_completo:
                            furo_data["rodape"]["linha1"] = " | ".join([x for x in row_limpa if x])
                            continue
                        
                        if "PROJETO" in texto_completo or "TRECHO" in texto_completo:
                            furo_data["rodape"]["linha2"] = " | ".join([x for x in row_limpa if x])
                            continue

                        if "SUBTRECHO" in texto_completo or "ESTUDO" in texto_completo:
                            furo_data["rodape"]["linha3"] = " | ".join([x for x in row_limpa if x])
                            continue

                        # --- 2. FILTROS DE CABEÇALHO (LIXO) ---
                        if "PROFUNDIDADE" in texto_completo or "GRANULOMETRIA" in texto_completo or "FURO" in texto_completo:
                            continue
                        
                        # --- 3. CAPTURA DOS DADOS (AMOSTRAS) ---
                        # Verifica se a linha tem dados suficientes (pelo menos 20 colunas de uma tabela padrão)
                        if len(row_limpa) > 20:
                            # Se a primeira célula tem algo (Número) ou se há dados no meio
                            if any(c for c in row_limpa):
                                try:
                                    amostra = {
                                        "num": row_limpa[0],
                                        "estaca": row_limpa[1],
                                        "prof": row_limpa[2],
                                        "ll": row_limpa[3],
                                        "ip": row_limpa[4],
                                        # Granulometria (Índices 5 a 17 = 13 peneiras)
                                        "g_val": row_limpa[5:18], 
                                        
                                        "ig": row_limpa[18],
                                        "trb": row_limpa[19],
                                        "hnat": row_limpa[20],
                                        
                                        # --- CORREÇÃO AQUI: SEQUÊNCIA DIRETA SEM PULAR ÍNDICES ---
                                        # Antes eu pulava o 21. Agora pegamos direto.
                                        "comp_h": row_limpa[21] if len(row_limpa) > 21 else "",
                                        "comp_ys": row_limpa[22] if len(row_limpa) > 22 else "",
                                        "exp": row_limpa[23] if len(row_limpa) > 23 else "",
                                        "isc": row_limpa[24] if len(row_limpa) > 24 else "",
                                        # Nova coluna adicionada: Sigma (delta)
                                        "sigma": row_limpa[25] if len(row_limpa) > 25 else ""
                                    }
                                    furo_data["amostras"].append(amostra)
                                except Exception as index_error:
                                    print(f"Erro de índice na linha: {index_error}")
                                    continue

        except Exception as e:
            print(f"Erro ao processar arquivo {nome_arquivo}: {e}")

        # Só adiciona se tiver encontrado dados
        if furo_data["amostras"]:
            dados_consolidados.append(furo_data)

    return dados_consolidados