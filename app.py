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
    /* NOVO TÍTULO LILÁS REVOLUCIONÁRIO */
    h1 {
        /* Gradiente futurista de Roxo Neon para Magenta */
        background: linear-gradient(to right, #9D50BB, #FF00FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3.5rem !important; /* Aumentei um pouco para mais impacto */
        text-align: center;
        padding-bottom: 10px;
        letter-spacing: 2px; /* Espaçamento mais moderno */
        text-shadow: 0px 0px 15px rgba(157, 80, 187, 0.5); /* Efeito de brilho neon */
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

# --- DADOS (O ESTOQUE DO E-COMMERCE) ---
banco_de_presentes = {
    "esporte": [
        {"item": "Garrafa Térmica Premium", "preco": 45, "desc": "Hidratação com tecnologia térmica dupla camada."},
        {"item": "Kit Elásticos Extensores", "preco": 30, "desc": "Academia completa que cabe na mochila."},
        {"item": "Luva de Treino Pro", "preco": 55, "desc": "Proteção para cargas altas e calos."},
        {"item": "Smartband Simples", "preco": 90, "desc": "Monitoramento de passos e sono básico."},
        {"item": "Corda de Pular Rolamentada", "preco": 40, "desc": "Alta velocidade para queimar calorias."}
    ],
    "geek": [
        {"item": "Funko Pop (Edição Especial)", "preco": 80, "desc": "Item de colecionador que valoriza com o tempo."},
        {"item": "Caneca 3D Star Wars", "preco": 40, "desc": "Detalhes fieis da saga para o café da manhã."},
        {"item": "Luminária Pixel LED", "preco": 45, "desc": "Iluminação ambiente estilo 8-bits."},
        {"item": "Camiseta Algodão Egípcio Nerd", "preco": 60, "desc": "Conforto premium com estampa de cultura pop."},
        {"item": "Mousepad Gamer Extra Grande", "preco": 70, "desc": "Cobre a mesa toda, melhora a precisão."}
    ],
    "fashion": [
        {"item": "Óculos Retro UV400", "preco": 50, "desc": "Estilo vintage com proteção solar real."},
        {"item": "Pulseira Couro Minimalista", "preco": 35, "desc": "Acessório coringa para qualquer look."},
        {"item": "Bag Transversal Street", "preco": 85, "desc": "Praticidade e estilo urbano."},
        {"item": "Boné Dad Hat", "preco": 45, "desc": "Tendência casual e despojada."},
        {"item": "Kit Meias Estampadas", "preco": 30, "desc": "Um toque de cor e personalidade discreta."}
    ],
    "minimalista": [
        {"item": "Vela Aromática Bamboo", "preco": 35, "desc": "Relaxamento e aroma suave para o ambiente."},
        {"item": "Planner Executivo Sem Pauta", "preco": 25, "desc": "Liberdade total para organizar ideias."},
        {"item": "Vaso de Cimento Geométrico", "preco": 40, "desc": "Design industrial para plantas pequenas."},
        {"item": "Organizador de Cabos", "preco": 20, "desc": "Fim da bagunça na mesa de trabalho."}
    ],
    "tech_home_office": [ # NOVA CATEGORIA
        {"item": "Suporte Notebook Ergonômico", "preco": 50, "desc": "Corrige a postura e resfria o computador."},
        {"item": "Ring Light de Mesa", "preco": 45, "desc": "Iluminação profissional para videochamadas."},
        {"item": "Hub USB 4 Portas", "preco": 35, "desc": "Mais conexões para quem tem muitos gadgets."},
        {"item": "Apoio de Pulso em Gel", "preco": 25, "desc": "Conforto para longas horas digitando."}
    ],
    "coffee_lover": [ # NOVA CATEGORIA
        {"item": "Prensa Francesa 350ml", "preco": 60, "desc": "O método clássico para um café encorpado."},
        {"item": "Copo Térmico Coffee To Go", "preco": 40, "desc": "Seu café quente até chegar no trabalho."},
        {"item": "Moedor de Grãos Manual", "preco": 90, "desc": "O cheiro de café moído na hora é impagável."},
        {"item": "Kit Mini Xícaras Parede Dupla", "preco": 55, "desc": "Design moderno que não queima a mão."}
    ],
    "pet_lover": [ # NOVA CATEGORIA
        {"item": "Brinquedo Interativo Kong", "preco": 45, "desc": "Mantém o pet entretido por horas."},
        {"item": "Bandana Personalizada", "preco": 20, "desc": "Estilo imediato para o passeio."},
        {"item": "Comedouro Lento", "preco": 35, "desc": "Saúde digestiva e diversão para o animal."},
        {"item": "Escova Tira Pelos", "preco": 30, "desc": "Casa limpa e pet massageado."}
    ]
}

# --- ATUALIZAÇÃO DAS LOJAS (PARCEIROS) ---
banco_de_lojas = {
    "esporte": [
        {"nome": "Netshoes", "url": "https://www.netshoes.com.br", "desc": "Líder em artigos esportivos"},
        {"nome": "Decathlon", "url": "https://www.decathlon.com.br", "desc": "A maior variedade técnica"},
        {"nome": "Nike Outlet", "url": "https://www.nike.com.br", "desc": "Qualidade indiscutível"}
    ],
    "geek": [
        {"nome": "Amazon Geek", "url": "https://www.amazon.com.br/geek", "desc": "Entrega mais rápida do Brasil"},
        {"nome": "Nerdstore", "url": "https://nerdstore.com.br", "desc": "De fã para fã"},
        {"nome": "Piticas", "url": "https://www.piticas.com.br", "desc": "Vestuário oficial"}
    ],
    "fashion": [
        {"nome": "Dafiti", "url": "https://www.dafiti.com.br", "desc": "Moda inteligente"},
        {"nome": "Amaro", "url": "https://amaro.com", "desc": "Tendências digitais"},
        {"nome": "Renner", "url": "https://www.lojasrenner.com.br", "desc": "Estilo para todos"}
    ],
    "minimalista": [
        {"nome": "Tok&Stok", "url": "https://www.tokstok.com.br", "desc": "Design assinado"},
        {"nome": "MinD", "url": "https://www.casamind.com.br", "desc": "Decoração com propósito"},
        {"nome": "Camicado", "url": "https://www.camicado.com.br", "desc": "Casa completa"}
    ],
    "tech_home_office": [
        {"nome": "Kabum!", "url": "https://www.kabum.com.br", "desc": "Hardware e periféricos"},
        {"nome": "Amazon Eletrônicos", "url": "https://amazon.com.br", "desc": "Tecnologia acessível"},
        {"nome": "Kalunga", "url": "https://www.kalunga.com.br", "desc": "Tudo para escritório"}
    ],
    "coffee_lover": [
        {"nome": "Coffee Mais", "url": "https://coffeemais.com", "desc": "Cafés especiais"},
        {"nome": "Amazon Cozinha", "url": "https://amazon.com.br", "desc": "Utensílios baristas"},
        {"nome": "Starbucks At Home", "url": "https://www.starbucksathome.com", "desc": "A experiência da cafeteria"}
    ],
    "pet_lover": [
        {"nome": "Petz", "url": "https://www.petz.com.br", "desc": "O shopping do seu pet"},
        {"nome": "Cobasi", "url": "https://www.cobasi.com.br", "desc": "Essencial para a vida"},
        {"nome": "Petlove", "url": "https://www.petlove.com.br", "desc": "Assinaturas e mimos"}
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
# --- INTERFACE VISUAL ---
# Título Principal com o novo estilo Lilás definido no CSS acima
st.markdown("<h1>GiftGenie AI</h1>", unsafe_allow_html=True)

# --- NOVO BLOCO DE TEXTO EMOCIONAL (REVOLUCIONÁRIO) ---
st.markdown("""
<p style='text-align: center; color: #C0C0C0; font-size: 1.1rem; line-height: 1.6; font-style: italic; max-width: 800px; margin: -15px auto 30px auto;'>
    "Sabe aquela ansiedade de navegar por horas e terminar com a dúvida: 'será que a pessoa vai gostar?'? A dificuldade de traduzir afeto em um presente físico é real e cansativa. O GiftGenie AI nasceu exatamente para resolver esse bloqueio criativo. A ideia não é apenas sugerir produtos, mas usar a tecnologia para entender perfis e conectar você às lojas certas, transformando a indecisão em um gesto certeiro."
</p>
""", unsafe_allow_html=True)
# -------------------------------------------------------

st.markdown("<p style='text-align: center; color: #aaa;'>Powered by <b>LangGraph</b> Agentes</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaa;'>Powered by <b>LangGraph</b> Agentes</p>", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        destinatario = st.selectbox("🎯 Destinatário", ["Namorado(a)", "Mãe", "Pai", "Amigo"])
    with col2:
        orcamento = st.number_input("💰 Orçamento (R$)", min_value=10, value=50, step=5)
    vibe = st.selectbox(
        "✨ Vibe Principal", 
        ["esporte", "geek", "fashion", "minimalista", "tech_home_office", "coffee_lover", "pet_lover"]
    )

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

# --- RODAPÉ COM ASSINATURA E CONTATOS ---
st.markdown("""
<br><br>
<div style='text-align: center; color: #666; font-size: 0.8rem;'>
<p style='margin-bottom: 15px;'>Desenvolvido por <b>Edson Ricardo</b> 🚀</p>
<div style="display: flex; justify-content: center; gap: 15px; margin-bottom: 20px;">
<a href="https://www.linkedin.com/in/edson-ricardo-495294220?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app" target="_blank" style="background-color: #0e76a8; color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-weight: bold; transition: all 0.3s;">LinkedIn 🔗</a>
<a href="https://wa.me/5511987302923?text=Ol%C3%A1!%20Vi%20seu%20projeto%20GiftGenie%20e%20gostaria%20de%20conversar." target="_blank" style="background-color: #25D366; color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-weight: bold; transition: all 0.3s;">WhatsApp 💬</a>
</div>
<span style='color: #444;'>Arquitetura: LangGraph StateMachine • Frontend: Streamlit</span>
</div>
""", unsafe_allow_html=True)