import streamlit as st
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GiftGenie AI", page_icon="🎁", layout="centered")

# --- ESTILIZAÇÃO AVANÇADA (CSS) ---
st.markdown("""
<style>
    /* 1. Fundo Geral e Fontes */
    .stApp {
        background-color: #0E1117;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 2. Título com Gradiente (Efeito Dourado/Laranja) */
    h1 {
        background: -webkit-linear-gradient(45deg, #F39C12, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        font-size: 3rem !important;
        text-align: center;
        padding-bottom: 20px;
    }
    
    /* 3. Subtítulo centralizado */
    .css-10trblm {
        text-align: center;
        color: #B0B0B0;
    }
    
    /* 4. Estilo dos Cards (Caixas dos Inputs) */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid #333;
    }

    /* 5. Botão Laranja "Neon" */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #F39C12 0%, #D35400 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 18px;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 15px rgba(243, 156, 18, 0.4);
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #D35400 0%, #F39C12 100%);
        transform: translateY(-2px);
        box-shadow: 0px 6px 20px rgba(243, 156, 18, 0.6);
        color: white;
    }

    /* 6. Card de Resultado */
    .result-card {
        background-color: #262730;
        border-left: 5px solid #F39C12;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- DADOS (LÓGICA) ---
banco_de_presentes = {
    "esporte": [
        {"item": "Garrafa Térmica Premium", "preco": 45, "desc": "Design ergonômico e mantém a temperatura por 12h."},
        {"item": "Kit Faixas de Resistência", "preco": 30, "desc": "Treino completo em qualquer lugar."},
        {"item": "Luva de Academia Pro", "preco": 55, "desc": "Aderência e proteção reforçada."},
        {"item": "Camiseta Tech Dry", "preco": 49, "desc": "Tecnologia anti-suor e secagem rápida."}
    ],
    "geek": [
        {"item": "Funko Pop (Edição Limitada)", "preco": 80, "desc": "Item essencial para colecionadores."},
        {"item": "Caneca Star Wars 3D", "preco": 40, "desc": "Detalhes realistas da saga."},
        {"item": "Mousepad Gamer Speed", "preco": 60, "desc": "Superfície otimizada para precisão."},
        {"item": "Luminária Pixel Art", "preco": 45, "desc": "Iluminação ambiente retrô."}
    ],
    "fashion": [
        {"item": "Óculos de Sol UV400", "preco": 50, "desc": "Design moderno com proteção total."},
        {"item": "Mix de Anéis Prata", "preco": 35, "desc": "Acabamento refinado e minimalista."},
        {"item": "Carteira Slim Couro", "preco": 45, "desc": "Discreta, elegante e funcional."},
        {"item": "Lenço de Seda Sintética", "preco": 40, "desc": "Toque suave para elevar o look."}
    ],
    "minimalista": [
        {"item": "Vela Aromática Bamboo", "preco": 35, "desc": "Fragrância suave e relaxante."},
        {"item": "Moleskine Capa Dura", "preco": 25, "desc": "Para ideias brilhantes."},
        {"item": "Vaso Geométrico + Suculenta", "preco": 30, "desc": "Decoração viva sem manutenção."},
        {"item": "Organizador de Mesa Acrílico", "preco": 48, "desc": "Clean e funcional."}
    ]
}

def sugerir_presente(vibe_escolhida, orcamento_maximo):
    lista_da_vibe = banco_de_presentes.get(vibe_escolhida, [])
    opcoes_validas = [p for p in lista_da_vibe if p["preco"] <= orcamento_maximo]
    return random.choice(opcoes_validas) if opcoes_validas else None

# --- INTERFACE VISUAL ---

st.markdown("<h1>GiftGenie AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa; font-size: 1.1rem; margin-bottom: 30px;'>O Consultor de Compras Inteligente.</p>", unsafe_allow_html=True)

# Container principal (Cria uma "caixa" visual ao redor dos inputs)
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        destinatario = st.selectbox("🎯 Quem vai receber?", ["Namorado(a)", "Mãe", "Pai", "Amigo", "Chefe"])
    
    with col2:
        orcamento = st.number_input("💰 Orçamento Máximo (R$)", min_value=10, value=50, step=5)
    
    vibe = st.selectbox("✨ Qual a 'vibe' da pessoa?", ["esporte", "geek", "fashion", "minimalista"])

st.write("") # Espaçamento
st.write("") 

if st.button("ENCONTRAR PRESENTE PERFEITO 🚀"):
    
    with st.spinner("Analisando perfil e tendências..."):
        import time
        time.sleep(1.2) # Pequeno delay para dar a sensação de "processamento" da IA
        resultado = sugerir_presente(vibe, orcamento)
    
    if resultado:
        # Exibição do Resultado Customizada
        st.markdown(f"""
        <div class="result-card">
            <h3 style="color: #F39C12; margin:0;">✨ Sugestão Encontrada!</h3>
            <h2 style="color: white; margin: 10px 0;">{resultado['item']}</h2>
            <p style="color: #ddd; font-style: italic;">"{resultado['desc']}"</p>
            <hr style="border-color: #444;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #aaa;">Valor estimado:</span>
                <span style="color: #2ecc71; font-weight: bold; font-size: 1.2rem;">R$ {resultado['preco']},00</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"⚠️ Nenhuma opção encontrada por menos de R$ {orcamento} na categoria '{vibe}'. Tente aumentar o orçamento!")

# Rodapé minimalista
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #444; font-size: 0.8rem;'>🔒 Powered by Python & Streamlit • Design Estratégico</p>", unsafe_allow_html=True)