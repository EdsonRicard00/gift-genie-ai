import random
import time
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

# --- 1. DEFINIÇÃO DO ESTADO (A Memória do Agente) ---
class VendasState(TypedDict):
    perfil_cliente: str
    orcamento: float
    interesse: str
    sugestao_atual: dict
    tentativas: int
    status: str  # 'pesquisando', 'refinando', 'concluido'

# --- 2. OS NÓS (As Ações do Vendedor) ---

def agente_pesquisador(state: VendasState):
    """
    Simula um especialista buscando produtos no banco de dados.
    """
    print(f"--- [Backend] Pesquisando produtos para: {state['interesse']} ---")
    time.sleep(1) # Simula o "thinking" da IA (importante para UX)
    
    # Simulação de Inteligência (Aqui entraria o GPT-4 ou Busca Web)
    produtos_simulados = [
        {"nome": "Smartwatch Pro", "preco": 800, "vibe": "tecnologia"},
        {"nome": "Kit Café Gourmet", "preco": 150, "vibe": "gastronomia"},
        {"nome": "Kindle Paperwhite", "preco": 499, "vibe": "leitura"},
        {"nome": "Tênis de Corrida Ultra", "preco": 600, "vibe": "esporte"}
    ]
    
    # Lógica simples de filtro baseada no interesse
    escolha = next((p for p in produtos_simulados if state['interesse'] in p['vibe']), produtos_simulados[0])
    
    return {
        "sugestao_atual": escolha,
        "tentativas": state['tentativas'] + 1,
        "status": "analisando"
    }

def agente_critico_de_vendas(state: VendasState):
    """
    O 'Gerente' que verifica se o produto bate com o orçamento.
    O LangGraph brilha aqui: ele toma a decisão de aprovar ou reprovar.
    """
    produto = state['sugestao_atual']
    orcamento = state['orcamento']
    
    print(f"--- [Backend] Verificando: {produto['nome']} custa {produto['preco']} (Budget: {orcamento}) ---")
    
    # Regra de Negócio (Lógica de Decisão)
    if produto['preco'] <= orcamento:
        return {"status": "aprovado"}
    else:
        # Se for muito caro, mandamos voltar e achar algo mais barato
        return {"status": "rejeitado"}

# --- 3. MONTAGEM DO GRAFO (O Fluxo de Trabalho) ---

def decisao_de_roteamento(state: VendasState):
    """A função que controla as setas do gráfico"""
    if state['status'] == "aprovado":
        return "fim"
    elif state['tentativas'] > 3:
        # Fail-safe para não ficar em loop infinito
        return "fim_alternativo" 
    else:
        return "pesquisar_novamente"

workflow = StateGraph(VendasState)

workflow.add_node("pesquisador", agente_pesquisador)
workflow.add_node("critico", agente_critico_de_vendas)

workflow.set_entry_point("pesquisador")

workflow.add_edge("pesquisador", "critico")

workflow.add_conditional_edges(
    "critico",
    decisao_de_roteamento,
    {
        "fim": END,
        "fim_alternativo": END,
        "pesquisar_novamente": "pesquisador" # O Loop Mágico
    }
)

app_ia = workflow.compile()
