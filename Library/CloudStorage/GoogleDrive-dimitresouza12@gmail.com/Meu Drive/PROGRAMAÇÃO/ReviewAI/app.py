import mysql.connector
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pysentimiento import create_analyzer

app = FastAPI()

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "dimitresouza10",
    "database": "review_ai_db"
}

# Inicializa o Analisador de Sentimentos (BERT)
analyzer = create_analyzer(task="sentiment", lang="pt")

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.post("/login")
def login(user: dict):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", 
                   (user['username'], user['password']))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    if result:
        return {"status": "success"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@app.post("/analyze")
def analyze_phrases(request: dict):
    phrases = request.get("phrases", [])
    results = []
    
    # Contador corrigido para evitar erro de chave (KeyError)
    counts = {"positivo": 0, "negativo": 0, "neutro": 0}
    
    db = get_db_connection()
    cursor = db.cursor()

    for phrase in phrases:
        prediction = analyzer.predict(phrase)
        sentiment = prediction.output.lower()
        
        # Mapeamento para os labels em português
        label = "positivo" if "pos" in sentiment else "negativo" if "neg" in sentiment else "neutro"
        counts[label] += 1
        
        cursor.execute(
            "INSERT INTO historico (frase, sentimento, data_analise) VALUES (%s, %s, %s)",
            (phrase, label, datetime.now())
        )
        results.append({"phrase": phrase, "sentiment": label})

    db.commit()
    cursor.close()
    db.close()

    # Cálculo de Score (Média Ponderada)
    total = len(phrases)
    score = ((counts['positivo'] * 100) + (counts['neutro'] * 50)) / total if total > 0 else 0
    
    return {"sentiments": results, "satisfaction_score": round(score, 1)}

@app.get("/history")
def get_history(inicio: str = None, fim: str = None):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    query = "SELECT frase, sentimento, data_analise FROM historico"
    params = []
    
    if inicio and fim:
        query += " WHERE DATE(data_analise) BETWEEN %s AND %s"
        params = [inicio, fim]
    
    query += " ORDER BY data_analise DESC LIMIT 100"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows