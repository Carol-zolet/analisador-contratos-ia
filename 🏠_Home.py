import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Analisador 26fit",
    page_icon="https://www.26fit.com.br/imagens/logo.png"
)

# --- CSS PERSONALIZADO (TEMA 26 FIT - VERSÃO PREMIUM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Oculta elementos padrão do Streamlit */
    #MainMenu, footer, header { visibility: hidden; }

    /* Fundo geral com gradiente sutil */
    .main {
        background: linear-gradient(180deg, #fafafa 0%, #ffffff 100%);
    }

    /* Estilo do container principal */
    .main .block-container { 
        padding-top: 2rem; 
        padding-bottom: 4rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1200px;
    }

    /* SEÇÃO DE BOAS-VINDAS (HERO SECTION) */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border-radius: 24px;
        position: relative;
        overflow: hidden;
        margin-bottom: 4rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 50%, rgba(255, 210, 0, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(255, 210, 0, 0.08) 0%, transparent 50%);
        pointer-events: none;
    }
    .hero-section .subheader {
        color: #ffd200;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    .hero-section h1 {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 4rem;
        line-height: 1.15;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 20px rgba(0,0,0,0.3);
    }
    .hero-section p {
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.7;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }

    /* CARTÕES DE FUNCIONALIDADES */
    .features-container {
        display: flex;
        gap: 2.5rem;
        margin-top: 3rem;
        flex-wrap: wrap;
    }
    .feature-card {
        background: #ffffff;
        padding: 3rem 2.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        border: 2px solid transparent;
        flex: 1;
        min-width: 280px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ffd200 0%, #ffed4e 100%);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.12);
        border-color: #ffd200;
    }
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    .feature-card .icon {
        font-size: 4rem;
        line-height: 1;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 4px 12px rgba(255, 210, 0, 0.3));
    }
    .feature-card h3 {
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.6rem;
        margin-bottom: 1rem;
    }
    .feature-card p {
        color: #555555;
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        line-height: 1.7;
        font-weight: 400;
    }

    /* CHAMADA PARA AÇÃO (CALL TO ACTION) */
    .cta-box {
        background: linear-gradient(135deg, #ffd200 0%, #ffed4e 100%);
        color: #1a1a1a;
        padding: 3.5rem 3rem;
        border-radius: 24px;
        text-align: center;
        margin-top: 5rem;
        box-shadow: 0 15px 50px rgba(255, 210, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    .cta-box::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        animation: pulse 8s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    .cta-box h2 {
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }
    .cta-box p {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        position: relative;
        z-index: 1;
        color: #2a2a2a;
    }

    /* Responsividade */
    @media (max-width: 768px) {
        .hero-section h1 { font-size: 2.5rem; }
        .features-container { flex-direction: column; }
        .feature-card { min-width: 100%; }
    }

</style>
""", unsafe_allow_html=True)

# --- LAYOUT DA PÁGINA ---

# 1. SEÇÃO DE BOAS-VINDAS (HERO)
st.markdown("""
<div class="hero-section">
    <div class="subheader">Ferramenta Interna 26 FIT</div>
    <h1>Analisador Jurídico de Contratos</h1>
    <p>
        O assistente de IA para acelerar a revisão de contratos de locação, 
        identificando riscos e pontos de atenção com foco na proteção da nossa marca.
    </p>
</div>
""", unsafe_allow_html=True)

# 2. CARTÕES DE FUNCIONALIDADES
st.markdown('<div class="features-container">', unsafe_allow_html=True)

st.markdown("""
<div class="feature-card">
    <div class="icon">⚙️</div>
    <h3>Diagnóstico por Regras</h3>
    <p>Um motor de regras varre o documento em busca de mais de 15 tipos de cláusulas de risco pré-definidas, gerando um score de perigo instantâneo.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="feature-card">
    <div class="icon">🧠</div>
    <h3>Análise Profunda com IA</h3>
    <p>O Google Gemini realiza uma análise jurídica completa, interpretando o contexto, identificando ambiguidades e sugerindo alterações nas cláusulas.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 3. CHAMADA PARA AÇÃO (CALL TO ACTION)
st.markdown("""
<div class="cta-box">
    <h2>Pronto para Começar?</h2>
    <p>Navegue para a página "Analisador" na barra lateral para fazer o upload do seu primeiro contrato.</p>
</div>
""", unsafe_allow_html=True)