import streamlit as st
import random
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GiftGenie AI", page_icon="🎁", layout="centered")

# --- ESTILIZAÇÃO AVANÇADA (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; font-family: 'Helvetica Neue', sans-serif; }
    h1 {
        background: -webkit-linear-gradient(45deg, #F39C12, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important; font-size: 3rem !important;
        text-align: center; padding-bottom: 20px;
    }
    div.stButton > button {
        width: 100%; background: linear-gradient(90deg, #F39C12 0%, #D35400 100%);
        color: white; border: none; padding: 15px 32px;
        font-size: 18px; border-radius: 12px; transition: all 0.3s ease;
        box-shadow: 0px 4px 15px rgba(243, 156, 18, 0.4);
    }
    div.stButton > button:hover {
        transform: translateY(-2px); box-shadow: 0px 6px 20px rgba(243, 156, 18, 0.6); color: white;
    }
    .result-card {
        background-color: #1E1E1E; border-left: 5px solid #F39C12;
        padding: 20px; border-radius: 10px; margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .store-card {
        background-color: #262730; border: 1px solid #333;
        border-radius: 8px; padding: 15px; text-align: center;
        transition: transform 0.2s; margin-bottom: 10px;
        height: 100%;
    }
    .store-card:hover { transform: scale(1.03); border-color: #F39C12; }
    .store-link {
        text-decoration: none; color: white; font-weight: bold; font-size: 1.1rem;
    }
    .store-desc { font-size: 0.8rem; color: #aaa; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# --- DADOS (CONHECIMENTO DO SISTEMA) ---
banco_de_presentes = {
    "esporte": [
        {"item": "Garrafa Térmica Premium", "preco": 45, "desc": "Hidratação com tecnologia térmica."},
        {"item": "Kit Elásticos Extensores", "preco": 30, "desc": "Academia completa em casa."},
        {"item": "Luva de Treino Pro", "preco": 55, "desc": "Proteção para cargas altas."}
    ],
    "geek": [
        {"item": "Funko Pop (Edição Especial)", "preco": 80, "desc": "Item de colecionador raro."},
        {"item": "Caneca 3D Star Wars", "preco": 40, "desc": "Detalhes fieis da saga."},
        {"item": "Luminária Pixel LED", "preco": 45, "desc": "Decoração gamer retrô."}
    ],
    "fashion": [
        {"item": "Óculos Retro UV400", "preco": 50, "desc": "Estilo vintage com proteção."},
        {"item": "Pulseira Couro Minimalista", "preco": 35, "desc": "Acessório coringa."}
    ],
    "minimalista": [
        {"item": "Vela Aromática Bamboo", "preco": 35, "desc": "Relaxamento e aroma suave."},
        {"item": "Planner Executivo", "preco": 25, "desc": "Organização com elegância."}
    ]
}

# Banco de Lojas
banco_de_lojas = {
    "esporte": [
        {"nome": "Netshoes", "url": "https://www.netshoes.com.br", "desc": "Maior e-commerce esportivo"},
        {"nome": "Decathlon", "url": "https://www.decathlon.com.br", "desc": "Tudo para 65 esportes"},
        {"nome": "Centauro", "url": "https://www.centauro.com.br", "desc": "Rede tradicional de esportes"}
    ],
    "geek": [
        {"nome": "Nerdstore", "url": "https://nerdstore.com.br", "desc": "A maior loja nerd do Brasil"},
        {"nome": "Piticas", "url": "https://www.piticas.com.br", "desc": "Camisetas e colecionáveis"},
        {"nome": "Amazon Geek", "url": "https://www.amazon.com.br/geek", "desc": "Presentes rápidos"}
    ],
    "fashion": [
        {"nome": "Zattini", "url": "https://www.zattini.com.br", "desc": "Moda e lifestyle"},
        {"nome": "Dafiti", "url": "https://www.dafiti.com.br", "desc": "Marcas famosas"},
        {"nome": "Amaro", "url": "https://amaro.com", "desc": "Moda estilosa"}
    ],
    "minimalista": [
        {"nome": "Tok&Stok", "url": "https://www.tokstok.com.br", "desc": "Design clean"},
        {"nome": "Camicado", "url": "https://www.camicado.com.br", "desc": "Casa e organização"},
        {"nome": "MinD", "url": "https://www.casamind.com.br", "desc": "Design original"}
    ]
}

# --- ENGINE DE IA (LANGGRAPH) ---
class AgentState(TypedDict):
    vibe: str
    orcamento: float
    opcoes_encontradas: List[dict]
    decisao_final: dict
    lojas_recomendadas: List[dict]

def pesquisar_presentes(state: AgentState):
    vibe = state['vibe']
    resultados = banco_de_presentes.get(vibe, [])
    return {"opcoes_encontradas": resultados}

def filtrar_por_orcamento(state: AgentState):
    opcoes = state['opcoes_encontradas']
    orcamento = state['orcamento']
    validos = [p for p in opcoes if p['preco'] <= orcamento]
    escolha = random.choice(validos) if validos else None
    return {"decisao_final": escolha}

def recomendar_lojas(state: AgentState):
    if state['decisao_final']:
        vibe = state['vibe']
        lojas = banco_de_lojas.get(vibe, [])
        return {"lojas_recomendadas": lojas}
    return {"lojas_recomendadas": []}

workflow = StateGraph(AgentState)
workflow.add_node("pesquisador", pesquisar_presentes)
workflow.add_node("financeiro", filtrar_por_orcamento)
workflow.add_node("loja_finder", recomendar_lojas)

workflow.set_entry_point("pesquisador")
workflow.add_edge("pesquisador", "financeiro")
workflow.add_edge("financeiro", "loja_finder")
workflow.add_edge("loja_finder", END)

app_ia = workflow.compile()

# --- INTERFACE VISUAL ---
st.markdown("<h1>GiftGenie AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa;'>Powered by <b>LangGraph</b> Agentes</p>", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        destinatario = st.selectbox("🎯 Destinatário", ["Namorado(a)", "Mãe", "Pai", "Amigo"])
    with col2:
        orcamento = st.number_input("💰 Orçamento (R$)", min_value=10, value=50, step=5)
    vibe = st.selectbox("✨ Vibe Principal", ["esporte", "geek", "fashion", "minimalista"])

st.write("") 

if st.button("ATIVAR AGENTES DE BUSCA 🚀"):
    
    with st.spinner("Iniciando workflow de agentes..."):
        inputs = {"vibe": vibe, "orcamento": orcamento}
        resultado_estado = app_ia.invoke(inputs)
        
        presente = resultado_estado.get("decisao_final")
        # Correção aqui: Adicionei um valor padrão ([]) para evitar erro se vier vazio
        lojas = resultado_estado.get("lojas_recomendadas", [])
    
    if presente:
        st.markdown(f"""
        <div class="result-card">
            <h3 style="color: #F39C12; margin:0;">✨ Sugestão Encontrada!</h3>
            <h2 style="color: white; margin: 10px 0;">{presente['item']}</h2>
            <p style="color: #ddd;">"{presente['desc']}"</p>
            <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                <span style="color: #aaa;">Preço Médio:</span>
                <span style="color: #2ecc71; font-weight: bold;">R$ {presente['preco']},00</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if lojas:
            st.markdown("<br><h4 style='text-align: center; color: #F39C12;'>🛒 Onde encontrar (Parceiros Indicados)</h4>", unsafe_allow_html=True)
            cols = st.columns(3)
            for i, loja in enumerate(lojas):
                if i < 3: # Garante que não estoure o layout
                    with cols[i]:
                        st.markdown(f"""
                        <a href="{loja['url']}" target="_blank" style="text-decoration: none;">
                            <div class="store-card">
                                <div class="store-link">{loja['nome']} ↗</div>
                                <div class="store-desc">{loja['desc']}</div>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
        else:
            st.warning("Nenhuma loja parceira encontrada para esta categoria.")
                
    else:
        st.error(f"⚠️ Os agentes não encontraram produtos da vibe '{vibe}' abaixo de R$ {orcamento}.")

# Rodapé
st.markdown("<br><br><p style='text-align: center; color: #444; font-size: 0.8rem;'>Arquitetura: LangGraph StateMachine • Frontend: Streamlit</p>", unsafe_allow_html=True)