import streamlit as st
import random

# --- 1. O "CÉREBRO" DO SISTEMA (DADOS) ---
# Aqui criamos um "banco de dados" simples com opções de presentes
banco_de_presentes = {
    "esporte": [
        {"item": "Garrafa Térmica Inox", "preco": 45, "desc": "Ideal para hidratação no treino."},
        {"item": "Faixa Elástica de Resistência", "preco": 30, "desc": "Ótimo para treinar em casa."},
        {"item": "Luva de Academia", "preco": 55, "desc": "Proteção e conforto."},
        {"item": "Camiseta Dry Fit", "preco": 49, "desc": "Tecido leve para suar à vontade."}
    ],
    "geek": [
        {"item": "Funko Pop (Sortido)", "preco": 80, "desc": "Colecionável clássico."},
        {"item": "Caneca Temática Star Wars", "preco": 40, "desc": "Para o café do lado sombrio."},
        {"item": "Mousepad Gamer Grande", "preco": 60, "desc": "Melhora a precisão no jogo."},
        {"item": "Luminária Pixel", "preco": 45, "desc": "Decoração retrô."}
    ],
    "fashion": [
        {"item": "Óculos de Sol Estiloso", "preco": 50, "desc": "Proteção com estilo."},
        {"item": "Kit de Anéis Minimalistas", "preco": 35, "desc": "Acessório versátil."},
        {"item": "Carteira Slim", "preco": 45, "desc": "Prática e cabe no bolso."},
        {"item": "Lenço/Echarpe", "preco": 40, "desc": "Toque de elegância."}
    ],
    "minimalista": [
        {"item": "Vela Aromática", "preco": 35, "desc": "Deixa o ambiente aconchegante."},
        {"item": "Caderno de Anotações Preto", "preco": 25, "desc": "Simples e funcional."},
        {"item": "Vaso de Suculenta (Artificial)", "preco": 30, "desc": "Verde sem trabalho."},
        {"item": "Organizador de Mesa", "preco": 48, "desc": "Mantenha tudo no lugar."}
    ]
}

# --- 2. A FUNÇÃO DE LÓGICA ---
def sugerir_presente(vibe_escolhida, orcamento_maximo):
    # Pega a lista da vibe escolhida
    lista_da_vibe = banco_de_presentes.get(vibe_escolhida, [])
    
    # Filtra: Só deixa passar o que cabe no orçamento
    opcoes_validas = []
    for presente in lista_da_vibe:
        if presente["preco"] <= orcamento_maximo:
            opcoes_validas.append(presente)
    
    # Se não sobrar nada (dinheiro curto), retorna mensagem de erro
    if not opcoes_validas:
        return None
    
    # Escolhe um aleatório entre os que sobraram para parecer "inteligente"
    return random.choice(opcoes_validas)

# --- 3. A INTERFACE (STREAMLIT) ---
st.set_page_config(page_title="GiftGenie AI", page_icon="🎁")

st.title("🎁 GiftGenie AI")
st.subheader("O Assistente de Compras que _pensa_ antes de sugerir.")
st.divider()

# Colunas
col1, col2 = st.columns(2)
with col1:
    destinatario = st.selectbox("Quem vai receber?", ["Namorado(a)", "Mãe", "Pai", "Amigo"])
with col2:
    # Step=5 faz pular de 5 em 5 reais
    orcamento = st.number_input("Orçamento máximo (R$)", min_value=10, value=50, step=5)

vibe = st.selectbox("Qual a 'vibe' da pessoa?", ["esporte", "geek", "fashion", "minimalista"])

# Espaço visual
st.write("") 

# Botão de Ação
if st.button("ENCONTRAR PRESENTE PERFEITO 🚀", type="primary"):
    
    # Chama nossa função inteligente
    resultado = sugerir_presente(vibe, orcamento)
    
    st.divider()
    
    if resultado:
        st.success("✨ Presente Encontrado!")
        st.metric(label="Sugestão", value=resultado["item"], delta=f"R$ {resultado['preco']}")
        st.info(f"💡 Por que?: {resultado['desc']}")
    else:
        st.error(f"Poxa! Não encontrei nada da vibe '{vibe}' por menos de R$ {orcamento}. Tente aumentar um pouquinho!")

# Rodapé
st.markdown("---")
st.caption("🔒 Desenvolvido com Python e Lógica Estratégica.")