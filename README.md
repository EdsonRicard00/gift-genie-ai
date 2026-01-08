# 🎁 GiftGenie AI - Agente de Vendas Autônomo

> **Uma aplicação Full-Stack de Inteligência Artificial que utiliza fluxos agênticos cíclicos (LangGraph) e Psicologia das Cores para otimizar a experiência de compra.**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![LangGraph](https://img.shields.io/badge/AI-LangGraph-orange)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![Status](https://img.shields.io/badge/Status-MVP-green)

---

## 🧠 Sobre o Projeto

O **GiftGenie AI** não é apenas um sistema de recomendação. É uma implementação de **Engenharia de Agentes (Agentic Engineering)**.

Diferente de chatbots lineares tradicionais, este sistema utiliza um **Grafo de Estados (State Graph)** para simular o processo cognitivo de um consultor de vendas humano. O sistema possui capacidade de "autocrítica": ele pesquisa, avalia se a sugestão atende aos requisitos de orçamento/perfil e, se necessário, **rejeita a própria sugestão e refaz a busca** autonomamente antes de apresentar ao usuário.

### 🎯 Diferenciais Técnicos & UX
* **Arquitetura Cíclica (Looping):** Uso de `LangGraph` para criar fluxos de decisão condicionais (Pesquisar -> Criticar -> Decidir -> Repetir/Entregar).
* **Separação de Responsabilidades:** Arquitetura desacoplada com Lógica de Negócios (`backend_ia.py`) separada da Interface (`app.py`).
* **UX Design Estratégico:** Interface desenhada com *Color Psychology* para conversão:
    * 🟠 **Laranja (#FF6F00):** Call-to-Action (CTA) para gerar urgência e entusiasmo.
    * 🔵 **Navy Blue (#0E1117):** Transmite autoridade e confiança técnica.
    * ⚪ **White-space:** Redução de carga cognitiva para foco na decisão.

---

## 🛠️ Arquitetura do Sistema

O sistema opera com dois agentes autônomos trabalhando em conjunto:

1.  **Agente Pesquisador:** Varre a base de dados (simulada ou via API) buscando produtos baseados em tags de interesse ("vibe").
2.  **Agente Crítico de Vendas:** Atua como um "guardrail", verificando restrições orçamentárias rígidas. Se o produto ultrapassa o budget, ele aciona o gatilho de *retry* no grafo.

```mermaid
graph LR
    A[Início] --> B(Agente Pesquisador);
    B --> C{Agente Crítico};
    C -- Aprovado --> D[Entrega ao Cliente];
    C -- Reprovado (Preço Alto) --> B;