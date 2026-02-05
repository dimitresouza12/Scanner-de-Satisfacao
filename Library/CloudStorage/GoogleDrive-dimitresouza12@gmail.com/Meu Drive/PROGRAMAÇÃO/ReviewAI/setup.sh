#!/bin/bash
# Setup ReviewAI: venv, dependências e modelo spaCy

set -e
cd "$(dirname "$0")"

echo "ReviewAI - Setup"

if [ ! -d "venv" ]; then
  echo "Criando venv..."
  python3 -m venv venv
fi

echo "Ativando venv e instalando dependências..."
source venv/bin/activate
pip install -r requirements.txt

echo "Baixando modelo spaCy pt_core_news_sm..."
python -m spacy download pt_core_news_sm

echo ""
echo "Setup concluído."
echo "  Backend:  uvicorn app:app --reload --host 127.0.0.1 --port 8000"
echo "  Interface: streamlit run interface.py"
