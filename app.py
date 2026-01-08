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
        font-weight: 700 !important;
        font-size: 3rem !important;
        text-align: center;
        padding-bottom: 20px;
    }
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #F39C12 0%, #D35400 100%);
        color: white; border: none; padding: 15px 32px;
        font-size: 18px; border-radius: 12px; transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px); box-shadow: 0px 6px 20px rgba(243, 156, 18, 0.6); color: white;
    }
    .result-card {
        background-color: #1E1E1E; border-left: 5px solid #F39C12;
        padding: 20px; border-radius: 10px; margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- DADOS (O CONHECIMENTO DO AGENTE) ---
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

# --- ENGINE DE IA (LANGGRAPH) ---
# Aqui começa a mágica que diferencia seu projeto de um script comum.

# 1. Definindo o Estado (A memória do robô durante o processo)
class AgentState(TypedDict):
    vibe: str
    orcamento: float
    opcoes_encontradas: List[dict]
    decisao_final: dict

# 2. Nó 1: Agente de Pesquisa (Simula a busca no banco de dados)
def pesquisar_presentes(state: AgentState):
    # O agente "olha" para o estado (vibe) e busca dados
    vibe = state['vibe']
    # Simulação de busca inteligente
    resultados = banco_de_presentes.get(vibe, [])
    return {"opcoes_encontradas": resultados}

# 3. Nó 2: Agente Financeiro (Filtra pelo orçamento)
def filtrar_por_orcamento(state: AgentState):
    opcoes = state['opcoes_encontradas']
    orcamento = state['orcamento']
    # Lógica de filtragem
    validos = [p for p in opcoes if p['preco'] <= orcamento]
    # Se tiver opções, escolhe a melhor (random mockado), senão retorna vazio
    escolha = random.choice(validos) if validos else None
    return {"decisao_final": escolha}

# 4. Construindo o Grafo (O Fluxo de Trabalho)
workflow = StateGraph(AgentState)

# Adicionando os nós
workflow.add_node("pesquisador", pesquisar_presentes)
workflow.add_node("financeiro", filtrar_por_orcamento)

# Definindo as conexões (Arestas)
workflow.set_entry_point("pesquisador") # Começa aqui
workflow.add_edge("pesquisador", "financeiro") # Depois vai pra cá
workflow.add_edge("financeiro", END) # Fim

# Compilando o cérebro
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
        # Executando o LangGraph
        inputs = {"vibe": vibe, "orcamento": orcamento}
        resultado_estado = app_ia.invoke(inputs)
        
        presente = resultado_estado.get("decisao_final")
    
    if presente:
        st.markdown(f"""
        <div class="result-card">
            <h3 style="color: #F39C12; margin:0;">✨ Sugestão Encontrada!</h3>
            <h2 style="color: white; margin: 10px 0;">{presente['item']}</h2>
            <p style="color: #ddd;">"{presente['desc']}"</p>
            <hr style="border-color: #444;">
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #aaa;">Preço:</span>
                <span style="color: #2ecc71; font-weight: bold;">R$ {presente['preco']},00</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"⚠️ Os agentes não encontraram produtos da vibe '{vibe}' abaixo de R$ {orcamento}.")

# Rodapé
st.markdown("<br><br><p style='text-align: center; color: #444; font-size: 0.8rem;'>Arquitetura: LangGraph StateMachine • Frontend: Streamlit</p>", unsafe_allow_html=True)