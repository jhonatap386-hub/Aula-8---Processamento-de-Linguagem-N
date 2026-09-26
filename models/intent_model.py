import sqlite3
import pandas as pd
import os

DB_PATH = 'banco_solicitacoes.db'

def init_db():
    """Inicializa a tabela de logs no SQLite3."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto_original TEXT NOT NULL,
            intencao TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def salvar_solicitacao(texto: str, intencao: str):
    """Salva uma nova classificação no banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO solicitacoes (texto_original, intencao) VALUES (?, ?)',
        (texto, intencao)
    )
    conn.commit()
    conn.close()

def obter_metricas_pandas():
    """Utiliza o Pandas para processar estatísticas do histórico."""
    if not os.path.exists(DB_PATH):
        return [], 0

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT intencao, criado_em FROM solicitacoes", conn)
    conn.close()

    if df.empty:
        return [], 0

    total_atendimentos = len(df)
    # Agrupamento e contagem via Pandas
    resumo = df['intencao'].value_counts().reset_index()
    resumo.columns = ['intencao', 'total']
    
    return resumo.to_dict(orient='records'), total_atendimentos