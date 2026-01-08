import streamlit as st
import random
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
import time

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
    /* Botão Principal */
    div.stButton > button {
        width: 100%; background: linear-gradient(90deg, #F39C12 0%, #D35400 100%);
        color: white; border: none; padding: 15px 32px;
        font-size: 18px; border-radius: 12px; transition: all 0.3s ease;
        box-shadow: 0px 4px 15px rgba(243, 156, 18, 0.4);
    }
    div.stButton > button:hover {
        transform: translateY(-2px); box-shadow: 0px 6px 20px rgba(243, 156, 18, 0.6); color: white;
    }
    /* Card de Resultado */
    .result-card {
        background-color: #1E1E1E; border-left: 5px solid #F39C12;
        padding: 20px; border-radius: 10px; margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    /* Cards das Lojas (Novidade) */
    .store-card {
        background-color: #262730; border: 1px solid #333;
        border-radius: 8px; padding: 15px; text-align: center;
        transition: transform 0.2s; margin-bottom: 10px;
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

# Novo Banco de Lojas
banco_de_lojas = {
    "esporte": [
        {"nome": "Netshoes", "url": "https://www.netshoes.com.br", "desc": "Maior e-commerce esportivo"},
        {"nome": "Decathlon", "url": "https://www.decathlon.com.br", "desc": "Tudo para 65 esportes"},
        {"nome": "Centauro", "url": "https://www.centauro.com.br", "desc": "Rede tradicional de esportes"}
    ],
    "geek": [
        {"nome": "Nerdstore", "url": "https://nerdstore.com.br", "desc": "A maior loja nerd do Brasil"},
        {"nome": "Piticas", "url": "https://www.piticas.com.br", "desc": "Camisetas e colecionáveis"},
        {"nome": "Zona Criativa", "url": "https://www.zonacriativa.com.br", "desc": "Presentes divertidos"}
    ],
    "fashion": [
        {"nome": "Zattini", "url": "https://www.zattini.com.br", "desc": "Moda e lifestyle"},
        {"nome": "Dafiti", "url": "https://www.dafiti.com.br", "desc": "Marcas famosas e tendências"},
        {"nome": "Amaro", "url": "https://amaro.com", "desc": "Moda digital e estilosa"}
    ],
    "minimalista": [
        {"nome": "Tok&Stok", "url": "https://www.tokstok.com.br", "desc": "Design e decoração clean"},
        {"nome": "Camicado", "url": "https://www.camicado.com.br", "desc": "Casa e organização"},
        {"nome": "MinD", "url": "https://www.casamind.com.br", "desc": "Design original e presenteável"}
    ]
}

# --- ENGINE DE IA (LANGGRAPH) ---

# 1. Estado (Memória) Atualizada
class AgentState(TypedDict):
    vibe: str
    orcamento: float
    opcoes_encontradas: List[dict]
    decisao_final: dict
    lojas_recomendadas: List[dict] # Nova memória para guardar as lojas

# 2. Nós (Agentes)

def pesquisar_presentes(state: AgentState):
    """Agente 1: Busca produtos no banco de dados"""
    print("--- Agente Pesquisador Ativado ---")
    vibe = state['vibe']
    resultados = banco_de_presentes.get(vibe, [])
    return {"opcoes_encontradas": resultados}

def filtrar_por_orcamento(state: AgentState):
    """Agente 2: Filtra pelo preço"""
    print("--- Agente Financeiro Ativado ---")
    opcoes = state['opcoes_encontradas']
    orcamento = state['orcamento']
    validos = [p for p in opcoes if p['preco'] <= orcamento]
    escolha = random.choice(validos) if validos else None
    return {"decisao_final": escolha}

def recomendar_lojas(state: AgentState):
    """Agente 3 (NOVO): Encontra onde comprar"""
    print("--- Agente de Oportunidades Ativado ---")
    if state['decisao_final']:
        vibe = state['vibe']
        # Busca as lojas daquela vibe
        lojas = banco_de_lojas.get(vibe, [])
        return {"lojas_recomendadas": lojas}
    return {"lojas_recomendadas": []}

# 3. Construindo o Grafo
workflow = StateGraph(AgentState)

workflow.add_node("pesquisador", pesquisar_presentes)
workflow.add_node("financeiro", filtrar_por_orcamento)
workflow.add_node("loja_finder", recomendar_lojas) # Novo nó adicionado

workflow.set_entry_point("pesquisador")
workflow.add_edge("pesquisador", "financeiro")
workflow.add_edge("financeiro", "loja_finder") # Conecta o financeiro ao buscador de lojas
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
        # Rodando o grafo
        inputs = {"vibe": vibe, "orcamento": orcamento}
        resultado_estado = app_ia.invoke(inputs)
        
        presente = resultado_estado.get("decisao_final")
        lojas = resultado_estado.get("lojas_recomendadas")
    
    if presente:
        # Exibe o presente
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

        # Exibe as lojas (Nova Seção)
        st.markdown("<br><h4 style='text-align: center; color: #fff;'>🛒 Onde encontrar (Parceiros Indicados)</h4>", unsafe_allow_html=True)