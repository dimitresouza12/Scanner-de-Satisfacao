import streamlit as st
import httpx
import pandas as pd
import plotly.express as px
from datetime import datetime, date

st.set_page_config(page_title="ReviewAI Pro", layout="wide")

# Estilização do Painel
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

MAPA_CORES = {"positivo": "#22c55e", "negativo": "#ef4444", "neutro": "#94a3b8"}

if 'logado' not in st.session_state:
    st.session_state['logado'] = False

def tela_login():
    st.title("🔐 Login - ReviewAI Pro")
    with st.form("login_form"):
        user = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar"):
            try:
                res = httpx.post("http://127.0.0.1:8000/login", json={"username": user, "password": password})
                if res.status_code == 200:
                    st.session_state['logado'] = True
                    st.rerun()
                else:
                    st.error("Credenciais incorretas.")
            except:
                st.error("Erro: Backend offline. Verifique o terminal do Uvicorn.")

if not st.session_state['logado']:
    tela_login()
    st.stop()

# --- DASHBOARD ---
st.sidebar.title("ReviewAI Dashboard")
if st.sidebar.button("Sair"):
    st.session_state['logado'] = False
    st.rerun()

tab_analise, tab_historico = st.tabs(["🔍 Nova Análise", "📜 Histórico & Filtros"])

with tab_analise:
    st.title("📊 Painel de Sentimentos")
    avaliacoes = st.text_area("Insira os textos para análise:", height=150)
    
    if st.button("Processar Dados", type="primary"):
        linhas = [l.strip() for l in avaliacoes.split("\n") if l.strip()]
        if linhas:
            with st.spinner("Analisando..."):
                try:
                    res = httpx.post("http://127.0.0.1:8000/analyze", json={"phrases": linhas})
                    data = res.json()
                    
                    # Score Card de Alta Visibilidade
                    st.markdown(f"""
                        <div style="background-color: #0f172a; padding: 25px; border-radius: 12px; border-left: 8px solid #3b82f6; margin-bottom: 30px;">
                            <h4 style="color: #94a3b8; margin: 0; font-size: 14px; text-transform: uppercase;">Score Geral de Satisfação</h4>
                            <span style="color: #ffffff; font-size: 48px; font-weight: 800;">{data['satisfaction_score']} / 100</span>
                        </div>
                    """, unsafe_allow_html=True)

                    c1, c2 = st.columns(2)
                    df = pd.DataFrame(data['sentiments'])
                    c1.plotly_chart(px.bar(df['sentiment'].value_counts().reset_index(), x='sentiment', y='count', color='sentiment', color_discrete_map=MAPA_CORES), use_container_width=True)
                    c2.plotly_chart(px.pie(df, names='sentiment', hole=0.5, color='sentiment', color_discrete_map=MAPA_CORES), use_container_width=True)
                except:
                    st.error("Conexão perdida com o motor de IA.")

with tab_historico:
    st.header("📜 Relatórios do MySQL")
    
    # Filtros de data
    col1, col2 = st.columns(2)
    d_inicio = col1.date_input("De:", date.today())
    d_fim = col2.date_input("Até:", date.today())

    if st.button("🔍 Sincronizar e Filtrar"):
        try:
            params = {"inicio": d_inicio.isoformat(), "fim": d_fim.isoformat()}
            res = httpx.get("http://127.0.0.1:8000/history", params=params)
            df_h = pd.DataFrame(res.json())
            
            if not df_h.empty:
                csv = df_h.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Baixar Planilha CSV", csv, "relatorio.csv", "text/csv")
                st.dataframe(df_h, use_container_width=True)
            else:
                st.warning("Sem dados para este período.")
        except:
            st.error("Erro ao acessar o banco de dados.")