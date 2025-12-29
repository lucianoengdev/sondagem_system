import os
from flask import Blueprint, render_template, request, current_app, redirect, url_for
from werkzeug.utils import secure_filename
from .utils_pdf import processar_furos
from .utils_file import salvar_dados_temporarios, carregar_dados_temporarios

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
        
        # Processa os dados
        lista_dados = processar_furos(saved_paths)
        
        # SALVA OS DADOS PARA NAVEGAÇÃO e Redireciona para Imprimir
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
    dados = carregar_dados_temporarios()
    return render_template('subleito_analise.html', dados=dados, active_page='analise')