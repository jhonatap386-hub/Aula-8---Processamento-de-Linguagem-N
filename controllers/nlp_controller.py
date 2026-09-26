import spacy

# Carrega o modelo em português
nlp = spacy.load("pt_core_news_sm")

# Dicionário de Intenções baseado em Lematização
INTENCOES_LEMMAS = {
    "Bloqueio de Cartão": {
        "lemmas": {"bloquear", "cartão", "perda", "roubo", "furtar", "perder", "cancelar", "bloqueio"},
        "icone": "💳"
    },
    "Segunda Via de Boleto": {
        "lemmas": {"segundo", "via", "boleto", "fatura", "código", "barra", "reemitir", "pagamento", "vencido"},
        "icone": "📄"
    },
    "Aumento de Limite": {
        "lemmas": {"limite", "aumentar", "aumento", "crédito", "analisar", "ajustar"},
        "icone": "📈"
    },
    "Suporte a Atendente": {
        "lemmas": {"falar", "atendente", "humano", "pessoa", "suporte", "ajuda", "reclamação"},
        "icone": "🎧"
    }
}

def classificar_solicitacao(texto: str):
    """Processa o texto com spaCy e identifica a intenção primária."""
    doc = nlp(texto.lower())
    
    # Extrai lemmas ignorando pontuação e espaços
    lemmas_usuario = {token.lemma_.lower() for token in doc if not token.is_punct and not token.is_space}
    
    melhor_intencao = "Outros / Não Identificado"
    maior_pontuacao = 0

    for intencao, dados in INTENCOES_LEMMAS.items():
        # Intersecção entre os lemmas do texto e as palavras-chave do setor
        coincidencias = lemmas_usuario.intersection(dados["lemmas"])
        score = len(coincidencias)
        
        if score > maior_pontuacao:
            maior_pontuacao = score
            melhor_intencao = intencao

    return {
        "intencao": melhor_intencao,
        "score": maior_pontuacao,
        "lemmas_detectados": list(lemmas_usuario)
    }