# 🎁 GiftGenie AI - Assistente de Compras Agêntico

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![LangGraph](https://img.shields.io/badge/AI-LangGraph-orange)
![Status](https://img.shields.io/badge/Status-Deployed-success)

> **O GiftGenie AI é um sistema de recomendação inteligente que utiliza uma arquitetura de agentes autônomos para encontrar o presente ideal e indicar as melhores lojas para compra.**

---

## 🚀 Sobre o Projeto

Diferente de filtros condicionais simples, este projeto implementa uma **Stateful Architecture** (Arquitetura de Estado) utilizando **LangGraph**. O sistema simula o raciocínio de um consultor de vendas através de um grafo direcionado, onde cada "nó" representa um agente especialista.

### 🧠 Arquitetura dos Agentes (Workflow)

O fluxo de decisão passa por 3 estágios autônomos:

1.  **🕵️ Agente Pesquisador:** Analisa a base de conhecimento para filtrar produtos baseados na "Vibe" (Perfil Comportamental).
2.  **💰 Agente Financeiro:** Aplica regras de negócio e restrições orçamentárias sobre os resultados.
3.  **🛒 Agente de Oportunidades:** Localiza parceiros comerciais (Lojas) confiáveis para a aquisição do produto selecionado.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Interface (UI):** Streamlit (com Custom CSS para Dark Mode Premium)
* **Orquestração de IA:** LangGraph (StateGraph Implementation)
* **Versionamento:** Git & GitHub

---

## 🎨 Funcionalidades

* **Interface Intuitiva:** Design moderno com feedback visual imediato.
* **Sistema de "Vibe":** Categorização por perfis (Geek, Esporte, Fashion, Minimalista).
* **Feedback Visual:** Cards interativos com detalhes do produto.
* **Integração com E-commerce:** Sugestão direta de links para compra (Amazon, Netshoes, etc).

---

## 📦 Como Rodar Localmente

Siga os passos abaixo para testar o projeto na sua máquina:

```bash
# 1. Clone o repositório
git clone [https://github.com/SEU-USUARIO/NOME-DO-REPO.git](https://github.com/SEU-USUARIO/NOME-DO-REPO.git)

# 2. Entre na pasta
cd NOME-DO-REPO

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
streamlit run app.py