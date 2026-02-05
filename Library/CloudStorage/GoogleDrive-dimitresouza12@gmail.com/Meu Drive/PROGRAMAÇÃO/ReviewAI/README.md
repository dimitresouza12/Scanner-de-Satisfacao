# ReviewAI – Análise de Sentimentos (SaaS)

API e interface para analisar avaliações de clientes em **português**: sentimento por frase (BERT), palavras-chave (substantivos e adjetivos via spaCy) e score de satisfação 0–100.

## Requisitos

- Python 3.10+

## Instalação

Dependências principais: **pysentimiento** (sentimento em PT), **spacy** (palavras-chave), **plotly**, **httpx**.

```bash
cd ReviewAI
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Modelo spaCy (obrigatório para palavras-chave)

Após o `pip install`, baixe o modelo de português:

```bash
python -m spacy download pt_core_news_sm
```

**Ou** use o script de setup (instala tudo e baixa o modelo):

```bash
python setup.py
# ou (Linux/macOS)
./setup.sh
```

## Executar

**1. Backend (terminal 1):**

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**2. Interface Streamlit (terminal 2):**

```bash
streamlit run interface.py
```

- API: **http://localhost:8000** | Docs: **http://localhost:8000/docs**
- Interface: **http://localhost:8501**

## Endpoint `POST /analyze`

**Corpo (JSON):**

```json
{
  "phrases": [
    "Comida perfeita, atendimento excelente!",
    "Demorou muito para chegar.",
    "Produto ok, preço justo."
  ]
}
```

**Resposta:**

```json
{
  "sentiments": [
    { "phrase": "Comida perfeita...", "sentiment": "positivo" },
    { "phrase": "Demorou muito...", "sentiment": "negativo" },
    { "phrase": "Produto ok...", "sentiment": "neutro" }
  ],
  "top_keywords": ["comida", "atendimento", "produto", "preço"],
  "satisfaction_score": 58.3
}
```

- **sentiments**: sentimento de cada frase (`positivo`, `negativo`, `neutro`) via **pysentimiento** (BERT em português).
- **top_keywords**: até 5 palavras-chave (substantivos e adjetivos) extraídas com **spaCy** `pt_core_news_sm`.
- **satisfaction_score**: média de satisfação de 0 a 100 com base nas probabilidades do modelo.

## Stack

- **Sentimento:** pysentimiento (modelo BERT pré-treinado para português).
- **Palavras-chave:** spaCy com `pt_core_news_sm` (apenas NOUN, PROPN, ADJ).
- **Backend:** FastAPI.
- **Frontend:** Streamlit, Plotly, httpx.

## Health check

- `GET /health` → `{"status": "ok"}`
