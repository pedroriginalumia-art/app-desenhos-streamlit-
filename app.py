import streamlit as st
import pandas as pd

# 📥 Carregar os dados da planilha
@st.cache_data
def carregar_dados(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)
    return df

# 🧠 Função para buscar informações do desenho
def buscar_desenho(df, desenho):
    resultado = df[df['DESENHO'].astype(str).str.lower() == desenho.lower()]
    return resultado

# 🎯 Interface do usuário
st.title("🔍 Consulta de Desenhos")

# 📎 Upload da planilha
arquivo = st.file_uploader("Envie a planilha (.xlsx)", type=["xlsx"])

if arquivo:
    df = carregar_dados(arquivo)

    # 🔎 Caixa de pesquisa
    desenho_input = st.text_input("Digite o nome do desenho para buscar:")

    if desenho_input:
        resultado = buscar_desenho(df, desenho_input)

        if not resultado.empty:
            st.success(f"Encontrado {len(resultado)} registro(s) para o desenho '{desenho_input}'")
            st.dataframe(resultado[['MÓDULO', 'DESENHO', 'REVISÃO']])
        else:
            st.warning("Desenho não encontrado.")
