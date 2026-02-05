#!/usr/bin/env python3
"""
Script de setup do ReviewAI.
Instala dependências e baixa o modelo spaCy pt_core_news_sm.
"""

import subprocess
import sys


def run(cmd: list[str], description: str) -> bool:
    print(f"\n>>> {description}")
    print(" ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Erro ao executar: {' '.join(cmd)}", file=sys.stderr)
        return False
    return True


def main():
    print("ReviewAI - Setup")
    if not run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        "Instalando dependências (pip install -r requirements.txt)",
    ):
        sys.exit(1)
    if not run(
        [sys.executable, "-m", "spacy", "download", "pt_core_news_sm"],
        "Baixando modelo spaCy pt_core_news_sm",
    ):
        sys.exit(1)
    print("\nSetup concluído. Inicie o backend com: uvicorn app:app --reload")
    print("E a interface com: streamlit run interface.py")


if __name__ == "__main__":
    main()
