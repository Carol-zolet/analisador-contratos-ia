# pages/📈_2_Dashboard.py

import streamlit as st
import pandas as pd
from database import buscar_todas_analises

st.set_page_config(layout="wide", page_title="Dashboard de Análises")

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
        max-width: 1400px;
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

    /* Markdown */
    .stMarkdown {
        font-family: 'Inter', sans-serif;
        color: #555555;
        line-height: 1.7;
    }

    /* Input de pesquisa */
    .stTextInput > div > div > input {
        background: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #ffd200;
        box-shadow: 0 0 0 3px rgba(255, 210, 0, 0.1);
    }

    /* Selectbox */
    .stSelectbox > div > div > div {
        background: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div > div:hover {
        border-color: #ffd200;
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

    /* DataFrames */
    [data-testid="stDataFrame"] {
        background: #ffffff;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        border: 2px solid #f0f0f0;
    }

    /* Cabeçalho da tabela */
    [data-testid="stDataFrame"] thead tr th {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: #ffd200 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        padding: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Células da tabela */
    [data-testid="stDataFrame"] tbody tr td {
        font-family: 'Inter', sans-serif;
        padding: 0.875rem;
        border-bottom: 1px solid #f0f0f0;
    }

    /* Hover nas linhas */
    [data-testid="stDataFrame"] tbody tr:hover {
        background-color: #fffbf0;
    }

    /* Alertas de info */
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        color: #0d47a1;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border: none;
        border-left: 4px solid #2196f3;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }

    /* Alertas de warning */
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
        color: #856404;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border: none;
        border-left: 4px solid #ffc107;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: #ffd200;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        padding: 1rem 1.5rem;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .streamlit-expanderContent {
        background: #ffffff;
        border: 2px solid #f0f0f0;
        border-top: none;
        border-radius: 0 0 12px 12px;
        padding: 2rem;
        font-family: 'Inter', sans-serif;
        line-height: 1.7;
    }

    /* Card de estatísticas */
    .stats-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        border-left: 4px solid #ffd200;
        margin: 1rem 0;
    }

    /* Responsividade */
    @media (max-width: 768px) {
        h1 { font-size: 2rem; }
        .main .block-container { padding: 1rem; }
        [data-testid="stDataFrame"] thead tr th { font-size: 0.875rem; }
    }

</style>
""", unsafe_allow_html=True)

st.title("📈 Dashboard de Análises Salvas")
st.markdown("Visualize, pesquise e acesse o histórico de todas as análises de contratos realizadas.")

# Botão para recarregar os dados do banco
if st.button("🔄 Recarregar Dados"):
    st.cache_data.clear() # Limpa o cache para buscar novos dados
    st.rerun()

# Usamos cache para não sobrecarregar o banco a cada interação na página
@st.cache_data
def carregar_dados():
    analises = buscar_todas_analises()
    # Converte os dados para um formato mais fácil de manipular (lista de dicionários)
    dados_formatados = [
        {
            "ID": a.id,
            "Arquivo": a.nome_arquivo,
            "Score de Risco": a.score_risco,
            "Data": a.data_analise.strftime("%d/%m/%Y %H:%M"),
            "Recomendação": a.resumo_riscos.get("resumo_riscos", {}).get("recomendacao_geral", "N/A"),
            "Análise IA": a.analise_completa_ia # Mantemos a análise completa para o detalhe
        }
        for a in analises
    ]
    return pd.DataFrame(dados_formatados)

df = carregar_dados()

if df.empty:
    st.warning("Nenhuma análise foi salva no banco de dados ainda. Analise um contrato na página 'Analisador' para começar.")
else:
    # --- Estatísticas rápidas ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric("Total de Análises", len(df))
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric("Score Médio de Risco", f"{df['Score de Risco'].mean():.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stats-card">', unsafe_allow_html=True)
        st.metric("Análise Mais Recente", df["Data"].iloc[0])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # --- Filtros e Interatividade ---
    st.subheader("🔍 Pesquisar Análises")
    filtro_arquivo = st.text_input("Digite o nome do arquivo:", placeholder="Exemplo: contrato_locacao.pdf")
    
    df_filtrado = df
    if filtro_arquivo:
        df_filtrado = df[df["Arquivo"].str.contains(filtro_arquivo, case=False, na=False)]

    # --- Exibição da Tabela ---
    st.markdown("### 📋 Tabela de Análises")
    st.dataframe(
        df_filtrado[["ID", "Arquivo", "Score de Risco", "Recomendação", "Data"]],
        hide_index=True,
        use_container_width=True
    )
    st.info(f"📊 Mostrando **{len(df_filtrado)}** de **{len(df)}** análises salvas.")

    # --- Visualização de Detalhes ---
    st.markdown("---")
    st.subheader("🔍 Ver Detalhes de uma Análise")
    
    # Cria uma lista de opções para o selectbox
    opcoes_analise = [f"ID {row.ID}: {row.Arquivo}" for index, row in df_filtrado.iterrows()]
    
    analise_selecionada = st.selectbox("Selecione uma análise para ver os detalhes completos:", options=opcoes_analise)

    if analise_selecionada:
        # Extrai o ID da opção selecionada
        id_selecionado = int(analise_selecionada.split(":")[0].replace("ID", "").strip())
        
        # Encontra a análise completa no DataFrame original
        dados_completos = df[df["ID"] == id_selecionado].iloc[0]

        with st.expander(f"📄 Análise Completa da IA para: **{dados_completos['Arquivo']}**", expanded=True):
            st.markdown(dados_completos["Análise IA"])