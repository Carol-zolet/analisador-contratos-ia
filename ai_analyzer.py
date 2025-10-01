# ai_analyzer.py

import os

# Suprime avisos do Google Cloud antes de qualquer import do genai
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

import streamlit as st
import google.generativeai as genai

# Add a constant to indicate if AI analysis is enabled
AI_ENABLED = True

PROMPT_IA = """
Você é um advogado especialista em contratos de locação comercial. Analise o contrato abaixo protegendo o LOCATÁRIO.

**TEXTO DO CONTRATO:**
{texto}

**ESTRUTURA DA ANÁLISE (SEJA CONCISO E DIRETO):**

## 📊 RESUMO EXECUTIVO
- Avaliação geral do contrato em 2-3 linhas
- **Nível de risco:** CRÍTICO / ALTO / MÉDIO / BAIXO
- **Recomendação principal:** [ação objetiva]

## ✅ PONTOS POSITIVOS (máx. 5 itens)
Liste apenas os principais benefícios ao locatário, com página.

## ⚠️ RISCOS CRÍTICOS (máx. 5 itens)
Para cada risco:
- **[NÍVEL]** Título do Risco (Página X)
  - **Impacto:** [breve explicação em 1-2 linhas]
  - **Solução:** [ação específica em 1 linha]

Priorize: despejo, multas abusivas, perda de investimentos, fundo de comércio.

## 🔍 PONTOS DE ATENÇÃO (máx. 3 itens)
Ambiguidades ou cláusulas que precisam esclarecimento.

## 📋 DOCUMENTOS FALTANTES (máx. 5 itens)
Liste apenas os essenciais.

## ⚖️ CONFORMIDADE LEGAL
Identifique até 3 violações principais da Lei 8.245/91.

## 🎯 AÇÕES RECOMENDADAS
Liste 3-5 ações prioritárias antes da assinatura.

**IMPORTANTE:** 
- Seja direto e objetivo
- Use **negrito** em palavras-chave importantes
- Use bullet points curtos
- Evite repetições
- Foque no que realmente importa
- Máximo de 800 palavras no total
"""

def configurar_api_gemini():
    """Verifica e configura a API do Gemini, pronta para deploy."""
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("Chave da API do Gemini não configurada. Por favor, configure-a nas variáveis de ambiente ou em .streamlit/secrets.toml")
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Erro ao configurar a API do Gemini: {e}")
        return False

@st.cache_data
def analisar_contrato_com_ia(texto: str) -> str:
    """Envia o texto para a IA Gemini e retorna a análise (com cache)."""
    if not configurar_api_gemini():
        return "❌ **Erro:** A chave da API do Gemini não foi configurada corretamente."
    try:
        # Using a valid model name from your test results
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        resposta = model.generate_content(PROMPT_IA.format(texto=texto))
        return resposta.text
    except Exception as e:
        return f"❌ **Erro na análise com Gemini:** {e}"