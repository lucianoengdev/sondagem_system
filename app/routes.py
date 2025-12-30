import os
from flask import Blueprint, render_template, request, current_app, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from .utils.pdf import processar_furos
from .utils.file import salvar_dados_temporarios, carregar_dados_temporarios, salvar_filtros, carregar_filtros, salvar_dados_linear, carregar_dados_linear
from .utils.filters import aplicar_filtros
from .utils.graphs import preparar_dados_linear

bp = Blueprint('main', __name__)

# ROTA 1: Página Inicial (Apenas Upload)
@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return "Nenhum arquivo enviado", 400
        
        files = request.files.getlist('files[]')
        saved_paths = []
        
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                saved_paths.append(filepath)
        
        lista_dados = processar_furos(saved_paths)
        
        salvar_dados_temporarios(lista_dados)
        return redirect(url_for('main.subleito_imprimir'))

    return render_template('index.html')

# ROTA 2: Visualização Limpa (Imprimir)
@bp.route('/subleito/imprimir')
def subleito_imprimir():
    dados = carregar_dados_temporarios()
    return render_template('subleito_imprimir.html', dados=dados, active_page='imprimir')

# ROTA 3: Análise com Modal
@bp.route('/subleito/analise')
def subleito_analise():
    dados_brutos = carregar_dados_temporarios()
    filtros_ativos = carregar_filtros()
    
    dados_filtrados = aplicar_filtros(dados_brutos, filtros_ativos)
    
    return render_template('subleito_analise.html', 
                           dados=dados_filtrados, 
                           filtros=filtros_ativos, 
                           active_page='analise')

# ROTA 4: Subleito análise com filtro
@bp.route('/api/filtros', methods=['POST'])
def gerenciar_filtros():
    req_data = request.get_json()
    acao = req_data.get('acao') 

    filtros_atuais = carregar_filtros()
    
    if acao == 'adicionar':
        novo_filtro = req_data.get('filtro')
        if novo_filtro not in filtros_atuais:
            filtros_atuais.append(novo_filtro)
            
    elif acao == 'remover':
        indice = int(req_data.get('indice'))
        if 0 <= indice < len(filtros_atuais):
            filtros_atuais.pop(indice)
            
    salvar_filtros(filtros_atuais)
    
    return jsonify({'status': 'ok'})

# ROTA 5: SUBLEITO LINEAR
@bp.route('/api/gerar_linear', methods=['POST'])
def api_gerar_linear():
    """
    Pega os dados atuais + filtros atuais, processa a tabela Linear
    e SALVA num arquivo separado. Não retorna HTML, retorna JSON de sucesso.
    """
    dados_brutos = carregar_dados_temporarios()
    filtros_ativos = carregar_filtros()
    
    dados_limpos = aplicar_filtros(dados_brutos, filtros_ativos)
    
    dados_linear = preparar_dados_linear(dados_limpos)
    
    salvar_dados_linear(dados_linear)
    
    return jsonify({'status': 'ok'})

@bp.route('/subleito/linear')
def subleito_linear():
    dados_tabela = carregar_dados_linear()
    
    if dados_tabela is None:
        return render_template('subleito_linear.html', dados=[], erro="Gere o Linear primeiro!")
        
    return render_template('subleito_linear.html', 
                           dados=dados_tabela, 
                           active_page='linear')