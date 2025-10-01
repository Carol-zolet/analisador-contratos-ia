# extractor.py

import fitz  # PyMuPDF
import re

def extrair_texto_local(caminho_pdf):
    """Extrai texto de um arquivo PDF, marcando o início de cada página."""
    try:
        doc = fitz.open(caminho_pdf)
        texto_completo = [f"--- PÁGINA {pagina.number + 1} ---\n{pagina.get_text('text')}\n\n" for pagina in doc]
        doc.close()
        return "".join(texto_completo), None
    except Exception as e:
        return None, f"Erro ao ler o PDF: {e}"

def extrair_clausulas_chave(texto: str) -> dict:
    """Análise jurídica baseada em regras para proteção máxima do locatário comercial."""
    alertas_criticos, alertas_graves, alertas_moderados, pontos_positivos, dados_essenciais = [], [], [], [], []
    
    padroes_dados = {
        "Valor do Aluguel": r"(?:valor|aluguel|aluguer).*?R\$\s*([\d\.,]+)",
        "Prazo do Contrato": r"(?:prazo|período|vigência).*?(\d+)\s*(?:meses|anos)",
        "Índice de Reajuste": r"(?:reajust|corrigi).*?(?:IGP-M|IPCA|INPC|[\w\-]+)",
        "Dia de Vencimento": r"(?:vencimento|pagamento).*?dia\s*(\d+)",
        "Multa por Rescisão": r"(?:multa|penalidade).*?(?:rescis|quebra).*?(\d+)\s*(?:%|meses)",
        "Caução/Depósito": r"(?:caução|depósito|garantia).*?R\$\s*([\d\.,]+)",
    }
    for tipo_dado, padrao in padroes_dados.items():
        match = re.search(padrao, texto, re.IGNORECASE)
        if match:
            if hasattr(match, 'lastindex') and match.lastindex is not None and match.lastindex >= 1:
                valor_extraido = match.group(1).strip()
            else:
                valor_extraido = match.group(0).strip()
            dados_essenciais.append({"tipo": tipo_dado, "valor": valor_extraido})

    todos_padroes_risco = {
        "Fundo de Comércio": {"padroes": [r"(?:renuncia|não\s+terá\s+direito).*?(?:fundo\s+de\s+comércio|ponto\s+comercial)", r"(?:sem\s+direito).*?(?:indenização).*?(?:ponto\s+comercial)"], "nivel": "CRÍTICO", "impacto": "Você perde o direito ao fundo de comércio/ponto, que pode valer milhares de reais após anos de negócio."},
        "Benfeitorias sem Indenização": {"padroes": [r"(?:renuncia|abdica).*?(?:indenização|reembolso).*?(?:benfeitorias|melhorias)", r"sem.*?(?:direito|indenização).*?benfeitorias"], "nivel": "CRÍTICO", "impacto": "Qualquer melhoria feita no imóvel (mesmo necessária para o negócio) não será reembolsada."},
        "Alvará Negado Sem Rescisão": {"padroes": [r"não\s+constituirá\s+motivo\s+para.*?rescisão", r"sem\s+direito\s+a\s+rescisão.*?alvará"], "nivel": "CRÍTICO", "impacto": "Mesmo que seja impossível obter alvará para seu negócio, você continua obrigado a pagar o aluguel."},
        "Garantia Excessiva": {"padroes": [r"(?:fiador|fiança).*?(?:renuncia).*?(?:bem\s+de\s+família|lei\s+8\.009)", r"(?:fiador).*?(?:principal\s+pagador).*?(?:renuncia)"], "nivel": "CRÍTICO", "impacto": "O fiador pode perder sua casa em caso de inadimplência, o que dificulta encontrar garantidores."},
        "Carência com Contrapartida Onerosa": {"padroes": [r"(?:carência|isento).*?(?:mediante|condicionada).*?(?:reforma|adequação|obra)", r"(?:concedida).*?(?:carência).*?(?:para que|a fim de).*?(?:realiz|efetu).*?(?:obra|reforma)"], "nivel": "GRAVE", "impacto": "A carência oferecida exige contrapartidas de reformas que podem custar mais que o valor dos aluguéis isentos."},
        "Multa por Atraso Excessiva": {"padroes": [r"(?:multa|penalidade).*?(?:atraso|inadimpl).*?(\d+)\s*%", r"(?:mora|atraso).*?(\d+)\s*(?:por\s+cento|%)"], "nivel": "MODERADO", "impacto": "Multa por atraso superior a 10% é considerada abusiva."},
        "Juros Abusivos": {"padroes": [r"juros.*?(\d+)\s*%.*?(?:mês|mensal|ao\s+mês)", r"correção.*?juros.*?(\d+)\s*%"], "nivel": "MODERADO", "impacto": "Juros acima de 1% ao mês podem ser considerados abusivos."},
    }

    for categoria, config in todos_padroes_risco.items():
        for padrao in config["padroes"]:
            for match in re.finditer(padrao, texto, re.IGNORECASE | re.MULTILINE):
                contexto_ampliado = texto[max(0, match.start() - 100):min(len(texto), match.end() + 100)]
                alerta = {"categoria": categoria, "detalhe": config["impacto"], "contexto": f"...{contexto_ampliado.strip()}..."}
                
                if config["nivel"] == "CRÍTICO" and not any(a['categoria'] == alerta['categoria'] for a in alertas_criticos):
                    alertas_criticos.append(alerta)
                elif config["nivel"] == "GRAVE" and not any(a['categoria'] == alerta['categoria'] for a in alertas_graves):
                    alertas_graves.append(alerta)
                elif config["nivel"] == "MODERADO" and not any(a['categoria'] == alerta['categoria'] for a in alertas_moderados):
                    alertas_moderados.append(alerta)
    
    padroes_positivos = {
        "Prazo de Carência": r"(?:carência|isenção).*?(?:primeiros|inicial).*?(?:meses|período)",
        "Direito de Preferência": r"(?:locatário|inquilino).*?(?:direito|preferência).*?(?:compra|aquisição)",
    }
    for tipo_positivo, padrao in padroes_positivos.items():
        if re.search(padrao, texto, re.IGNORECASE):
            pontos_positivos.append(tipo_positivo)

    score = min(100, (len(alertas_criticos) * 15) + (len(alertas_graves) * 8) + (len(alertas_moderados) * 3))
    
    if score >= 30: recomendacao_geral = "❌ NÃO ASSINAR"
    elif score >= 15: recomendacao_geral = "⚠️ NEGOCIAR OBRIGATÓRIO"
    elif score > 0: recomendacao_geral = "⚡ REVISAR COM CUIDADO"
    else: recomendacao_geral = "✅ APARENTEMENTE SEGURO"

    return {
        "dados_essenciais": dados_essenciais, "alertas_criticos": alertas_criticos,
        "alertas_graves": alertas_graves, "alertas_moderados": alertas_moderados,
        "pontos_positivos": pontos_positivos,
        "resumo_riscos": {
            "score_risco": score, "total_criticos": len(alertas_criticos),
            "total_graves": len(alertas_graves), "total_moderados": len(alertas_moderados),
            "recomendacao_geral": recomendacao_geral
        }
    }