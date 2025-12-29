import os
from flask import Blueprint, render_template, request, current_app
from werkzeug.utils import secure_filename
from .utils_pdf import processar_furos

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    lista_dados = [] # Inicializa vazio
    
    if request.method == 'POST':
        # Verifica se tem arquivos
        if 'files[]' not in request.files:
            return "Nenhum arquivo enviado", 400
        
        files = request.files.getlist('files[]')
        saved_paths = []
        
        # Garante que a pasta existe
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        # Salva arquivos
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                saved_paths.append(filepath)
        
        # Processa e recebe a LISTA estruturada (não mais um DataFrame genérico)
        lista_dados = processar_furos(saved_paths)
        
        # Opcional: Limpar arquivos temporários
        # for f in saved_paths: os.remove(f)

    # Passamos 'dados' para o HTML montar a tabela bonita
    return render_template('index.html', dados=lista_dados)