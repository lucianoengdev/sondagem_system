import pdfplumber
import os
import re

def processar_furos(file_paths):
    dados_consolidados = []
    
    for path in file_paths:
        nome_arquivo = os.path.basename(path)
        if not nome_arquivo.lower().startswith("furo"):
            continue

        dados_arquivo = {
            "arquivo": nome_arquivo,
            "linhas": []
        }

        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    # Extrai tabela SEM as linhas de grade para tentar pegar o texto puro alinhado
                    # ou usa a extração padrão mas filtramos o lixo
                    tabelas = page.extract_table()
                    
                    if not tabelas: continue

                    for row in tabelas:
                        # LÓGICA DE ENGENHARIA:
                        # Uma linha de dados válida geralmente começa com um número pequeno (Nº Amostra) 
                        # ou tem dados de granulometria (vários números em sequência).
                        # Vamos limpar vazios e None
                        row_limpa = [str(x).replace('\n', ' ').strip() if x else "" for x in row]
                        
                        # Filtro Básico: Ignorar cabeçalhos detectados como texto
                        texto_linha = "".join(row_limpa).lower()
                        if "profundidade" in texto_linha or "granulometria" in texto_linha or "passa" in texto_linha:
                            continue
                        
                        # Se a linha estiver quase vazia, ignora
                        if len("".join(row_limpa)) < 3:
                            continue

                        # Tenta mapear as colunas (Isso é uma aproximação baseada na imagem 3)
                        # O PDFPlumber às vezes retorna mais ou menos colunas dependendo da leitura.
                        # Aqui normalizamos para o dicionário que o HTML espera.
                        
                        # Se a linha tiver muitos dados, provavelmente é uma linha de amostra
                        if len(row_limpa) > 10:
                            dados_linha = {
                                "amostra": row_limpa[0] if len(row_limpa) > 0 else "",
                                "estaca": row_limpa[1] if len(row_limpa) > 1 else "",
                                "profundidade": row_limpa[2] if len(row_limpa) > 2 else "",
                                "ll": row_limpa[3] if len(row_limpa) > 3 else "",
                                "ip": row_limpa[4] if len(row_limpa) > 4 else "",
                                # Granulometria (ajuste os índices conforme a leitura real do seu PDF)
                                "g_2": row_limpa[5] if len(row_limpa) > 5 else "",
                                "g_1_12": row_limpa[6] if len(row_limpa) > 6 else "",
                                "g_1": row_limpa[7] if len(row_limpa) > 7 else "",
                                "g_34": row_limpa[8] if len(row_limpa) > 8 else "",
                                "g_38": row_limpa[9] if len(row_limpa) > 9 else "",
                                "g_4": row_limpa[10] if len(row_limpa) > 10 else "",
                                "g_10": row_limpa[11] if len(row_limpa) > 11 else "",
                                "g_16": row_limpa[12] if len(row_limpa) > 12 else "",
                                "g_30": row_limpa[13] if len(row_limpa) > 13 else "",
                                "g_40": row_limpa[14] if len(row_limpa) > 14 else "",
                                "g_50": row_limpa[15] if len(row_limpa) > 15 else "",
                                "g_100": row_limpa[16] if len(row_limpa) > 16 else "",
                                "g_200": row_limpa[17] if len(row_limpa) > 17 else "",
                                # Fim Granulometria
                                "ig": row_limpa[18] if len(row_limpa) > 18 else "",
                                "trb": row_limpa[19] if len(row_limpa) > 19 else "",
                                "h_nat": row_limpa[20] if len(row_limpa) > 20 else "",
                                "comp_h": row_limpa[22] if len(row_limpa) > 22 else "", # Pulando índice 21 as vezes vazio
                                "comp_ys": row_limpa[23] if len(row_limpa) > 23 else "",
                                "exp": row_limpa[24] if len(row_limpa) > 24 else "",
                                "isc": row_limpa[25] if len(row_limpa) > 25 else ""
                            }
                            dados_arquivo["linhas"].append(dados_linha)
        
        except Exception as e:
            print(f"Erro no arquivo {nome_arquivo}: {e}")
        
        if dados_arquivo["linhas"]:
            dados_consolidados.append(dados_arquivo)

    return dados_consolidados