# pages/📄_1_Analisador.py

import streamlit as st
import tempfile
import os

# Importa a lógica dos outros arquivos
from extractor import extrair_texto_local, extrair_clausulas_chave
from ai_analyzer import analisar_contrato_com_ia, AI_ENABLED
from database import salvar_analise, criar_tabelas

# Inicializa as tabelas do banco de dados
criar_tabelas()
print("Database tables initialized successfully.")

# --- CSS PERSONALIZADO (TEMA 26 FIT - VERSÃO PREMIUM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Oculta elementos padrão do Streamlit */
    #MainMenu, footer, header { visibility: hidden; }

    /* Fundo geral */
    .main {
        background: linear-gradient(180deg, #fafafa 0%, #ffffff 100%);
    }

    /* Container principal */
    .main .block-container { 
        padding-top: 2rem; 
        padding-bottom: 4rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1200px;
    }

    /* Título principal */
    h1 {
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    /* Subtítulos */
    h2, h3 {
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        margin-top: 2rem;
    }

    /* Card de upload */
    .stFileUploader {
        background: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        border: 2px dashed #ffd200;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #ffed4e;
        box-shadow: 0 15px 50px rgba(255, 210, 0, 0.15);
    }

    /* Métricas personalizadas */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #555555;
        font-family: 'Inter', sans-serif;
    }

    /* Cards de métrica */
    [data-testid="metric-container"] {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.06);
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }

    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 45px rgba(0,0,0,0.1);
        border-color: #ffd200;
    }

    /* Spinner personalizado */
    .stSpinner > div {
        border-top-color: #ffd200 !important;
    }

    /* Alertas de sucesso */
    .stSuccess {
        background: linear-gradient(135deg, #ffd200 0%, #ffed4e 100%);
        color: #1a1a1a;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border: none;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }

    /* Alertas de erro */
    .stError {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: #ffffff;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border: none;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }

    /* Markdown personalizado */
    .stMarkdown {
        font-family: 'Inter', sans-serif;
        color: #555555;
        line-height: 1.7;
    }

    /* Box de análise IA */
    .ia-analysis-box {
        background: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        border-left: 4px solid #ffd200;
        margin-top: 2rem;
    }

    /* Box de diagnóstico */
    .diagnostic-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 15px 50px rgba(0,0,0,0.15);
    }

    .diagnostic-box h2, .diagnostic-box h3 {
        color: #ffd200;
    }

    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #ffd200 0%, #ffed4e 100%);
        color: #1a1a1a;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(255, 210, 0, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(255, 210, 0, 0.4);
    }

    /* Responsividade */
    @media (max-width: 768px) {
        h1 { font-size: 2rem; }
        .main .block-container { padding: 1rem; }
    }

</style>
""", unsafe_allow_html=True)

st.title("📄 Análise de Contrato | 26fit")
st.markdown("Faça o upload de um contrato para receber uma **análise crítica internamente**.")

uploaded_file = st.file_uploader(
    "Selecione o arquivo PDF do contrato",
    type="pdf",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        caminho_do_arquivo = tmp_file.name

    with st.spinner("Lendo o documento..."):
        texto_contrato, erro = extrair_texto_local(caminho_do_arquivo)
    os.remove(caminho_do_arquivo)

    if erro:
        st.error(erro)
    elif texto_contrato:
        st.success(f"Contrato '{uploaded_file.name}' lido com sucesso. Iniciando análises...")

        # 1. Análise de Regras
        analise_regras = extrair_clausulas_chave(texto_contrato)
        resumo = analise_regras["resumo_riscos"]
        
        st.markdown('<div class="diagnostic-box">', unsafe_allow_html=True)
        st.subheader("📊 Diagnóstico Rápido do Contrato")
        st.markdown(f"**Recomendação Geral: {resumo['recomendacao_geral']}**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Pontuação de Risco", f"{resumo['score_risco']}")
        col2.metric("Alertas Críticos", resumo['total_criticos'])
        col3.metric("Alertas Graves", resumo['total_graves']) 

        # 2. Análise com IA - Somente se AI_ENABLED for True
        if AI_ENABLED:
            st.markdown('<div class="ia-analysis-box">', unsafe_allow_html=True)
            st.subheader("🧠 Análise sugestiva do Advogado Virtual")
            with st.spinner("Aguarde, nosso advogado virtual está revisando o contrato..."):
                analise_ia_texto = analisar_contrato_com_ia(texto_contrato)
            st.markdown(analise_ia_texto)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 3. SALVAR NO BANCO DE DADOS
        with st.spinner("Salvando resultados..."):
            try:
                # Chama a função para salvar no banco
                salvar_analise(
                    nome_arquivo=uploaded_file.name,
                    score=resumo['score_risco'],
                    resumo=analise_regras, # Salva o dicionário completo
                    analise_ia=analise_ia_texto if AI_ENABLED else "Análise de IA desativada"
                )
                st.success("Análise salva com sucesso no banco de dados!")
            except Exception as e:
                st.error(f"Ocorreu um erro ao salvar a análise: {e}")