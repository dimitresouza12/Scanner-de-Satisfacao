# 📊 Scanner de Satisfação: Análise de Sentimentos com IA

Este é um projeto **Full Stack** desenvolvido para processar feedbacks de clientes utilizando **Inteligência Artificial (BERT)**, com persistência de dados em **MySQL** e uma interface interativa em **Streamlit**.

O projeto nasceu da necessidade de transformar dados brutos de texto em métricas de satisfação precisas para tomadas de decisão em negócios.

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia | Função |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Interface do usuário e visualização de dados. |
| **Backend** | FastAPI (Python) | Motor da API e processamento lógico. |
| **IA** | Pysentimiento (BERT) | Modelo de NLP para análise de sentimentos em português. |
| **Banco de Dados** | MySQL | Armazenamento de usuários e histórico de análises. |

---

## 🧮 Lógica de Engenharia: Score de Satisfação

Diferente de sistemas que apenas contam palavras, o **ReviewAI Pro** aplica uma média ponderada para calcular o **Score Geral de Satisfação**, garantindo que feedbacks neutros tenham o peso correto na saúde do negócio:

**Score** = \frac{(\text{Positivos} \times 100) + (\text{Neutros} \times 50)}{\text{Total de Avaliações}}$$

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o Python e o MySQL instalados.

### 2. Configuração do Banco de Dados
Execute o script contido em `database.sql` no seu gerenciador MySQL para criar as tabelas necessárias.

### 3. Instalação de Dependências
```bash
pip install -r requirements.txt

4. Inicialização
Abra dois terminais independentes no VS Code e execute os comandos abaixo:

Terminal do Backend:

Bash
uvicorn app:app --reload

Terminal do Frontend:
Bash
streamlit run interface.py

📜 Funcionalidades do Sistema
Autenticação de Usuário: Sistema de login com validação direta no MySQL.

Análise em Tempo Real: Processamento de textos utilizando o modelo BERT para classificar sentimentos (Positivo, Negativo e Neutro).

Dashboard de BI: Visualização de gráficos de distribuição e o Score Geral de Satisfação em cards de alto contraste.

Relatórios Históricos: Aba dedicada para consulta de análises passadas com filtros por período de data.

Exportação de Dados: Funcionalidade para baixar o histórico filtrado em formato CSV para análise no Excel ou Numbers.

👤 Autor
Dimitre Souza

Software Engineering Student (2º Semestre).

LinkedIn: [https://www.linkedin.com/in/dimitre-souza/]

Email: dimitresouza12@gmail.com.