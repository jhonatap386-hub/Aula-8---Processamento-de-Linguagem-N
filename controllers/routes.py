from flask import Blueprint, render_template, request, redirect, url_for

# Imports relativos do próprio pacote/projeto
from .nlp_controller import classificar_solicitacao
from models.intent_model import salvar_solicitacao, obter_metricas_pandas

routes_bp = Blueprint('routes', __name__)
# ... restante do arquivo


from flask import Blueprint, render_template, request, redirect, url_for
from controllers.nlp_controller import classificar_solicitacao
from models.intent_model import salvar_solicitacao, obter_metricas_pandas

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/', methods=['GET'])
def index():
    metricas, total = obter_metricas_pandas()
    return render_template('index.html', metricas=metricas, total=total, resultado=None)

@routes_bp.route('/classificar', methods=['POST'])
def classificar():
    texto_cliente = request.form.get('texto_solicitacao', '')
    
    if texto_cliente.strip():
        # Processa a intenção via spaCy
        resultado_nlp = classificar_solicitacao(texto_cliente)
        
        # Persiste o log no SQLite3
        salvar_solicitacao(texto_cliente, resultado_nlp['intencao'])
        
        # Recupera estatísticas atualizadas via Pandas
        metricas, total = obter_metricas_pandas()
        
        return render_template(
            'index.html', 
            metricas=metricas, 
            total=total, 
            resultado=resultado_nlp, 
            texto_enviado=texto_cliente
        )
    
    return redirect(url_for('routes.index'))