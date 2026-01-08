import streamlit as st
import time
from backend_ia import app_ia  # Importa nossa IA criada no outro arquivo

# --- CONFIGURAÇÃO UX/UI (Design System) ---
st.set_page_config(
    page_title="GiftGenie AI",
    page_icon="🎁",
    layout="centered"
)

# CSS Customizado para forçar as cores de vendas (Laranja e Azul)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF6F00; /* Laranja Vendas */
        color: white;
        font-size: 18px;
        border-radius: 10px;
        border: none;
        padding: 10px 24px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #E65100;
        color: white;
    }
    .success-box {
        padding: 20px;
        background-color: #E8F5E9;
        border-left: 5px solid #2E7D32;
        border-radius: 5px;
    }
    h1 { color: #0E1117; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("🎁 GiftGenie AI")
st.markdown("### O Assistente de Compras que *pensa* antes de sugerir.")
st.markdown("---")

# --- ÁREA DO USUÁRIO (Input) ---
col1, col2 = st.columns(2)

with col1:
    perfil = st.selectbox(
        "Quem vai receber o presente?",
        ["Namorado(a)", "Mãe/Pai", "Amigo Geek", "Chefe", "Para mim mesmo"]
    )
    interesse = st.selectbox(
        "Qual a 'vibe' da pessoa?",
        ["tecnologia", "gastronomia", "leitura", "esporte", "moda"]
    )

with col2:
    orcamento = st.number_input("Qual seu orçamento máximo (R$)?", min_value=50, value=1000, step=50)

# --- BOTÃO DE AÇÃO (O Gatilho) ---
st.write("") # Espaçamento
if st.button("ENCONTRAR PRESENTE PERFEITO 🚀"):
    
    # UX: Feedback visual de carregamento
    with st.status("🤖 O Agente está trabalhando...", expanded=True) as status:
        st.write("🔍 Pesquisando tendências de mercado...")
        time.sleep(1)
        st.write("💰 Negociando melhores preços...")
        time.sleep(0.5)
        st.write("🧠 O Crítico de Vendas está revisando a qualidade...")
        
        # --- CHAMA A NOSSA IA (LangGraph) ---
        inputs = {
            "perfil_cliente": perfil,
            "orcamento": orcamento,
            "interesse": interesse,
            "sugestao_atual": {},
            "tentativas": 0,
            "status": "inicio"
        }
        
        # Executa o grafo
        resultado = app_ia.invoke(inputs)
        status.update(label="Presente Encontrado!", state="complete", expanded=False)

    # --- RESULTADO (A Conversão) ---
    produto_final = resultado['sugestao_atual']
    
    st.balloons() # Efeito visual de celebração (Dopamina)
    
    st.markdown(f"""
    <div class="success-box">
        <h3>🎯 Recomendação Final: {produto_final['nome']}</h3>
        <p>Baseado no perfil <b>{interesse}</b> e no orçamento de <b>R$ {orcamento}</b>.</p>
        <h2>R$ {produto_final['preco']},00</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Final
    st.write("")
    st.button(f"🛒 COMPRAR {produto_final['nome'].upper()} AGORA")

# --- RODAPÉ (Social Proof) ---
st.markdown("---")
st.caption("🔒 Desenvolvido com Python, LangGraph e UX Design Estratégico.")