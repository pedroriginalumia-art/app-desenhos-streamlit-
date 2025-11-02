import streamlit as st
import pandas as pd

# 📥 URL direta da planilha no GitHub
URL_PLANILHA = "https://raw.githubusercontent.com/pedroriginalumia-art/app-desenhos-streamlit-/main/DESENHOS%20P83%20REV.xlsx"

# 📥 Carregar os dados da planilha
@st.cache_data
def carregar_dados(url):
    df = pd.read_excel(url)
    return df

# 🔍 Função para buscar por parte do nome do desenho
def buscar_desenho(df, termo):
    filtro = df['DESENHO'].astype(str).str.contains(termo, case=False, na=False)
    return df[filtro]

# 🎯 Interface do usuário
st.title("🔍 Consulta de Desenhos com Sugestões")

# 🔄 Carregar dados automaticamente do GitHub
df = carregar_dados(URL_PLANILHA)

# 🔎 Entrada de texto para busca parcial
termo_input = st.text_input("Digite parte do nome do desenho (ex: 09A-394):")

# 📋 Sugestões automáticas com base no termo
if termo_input:
    sugestoes = df[df['DESENHO'].astype(str).str.contains(termo_input, case=False, na=False)]['DESENHO'].unique()
    sugestao_selecionada = st.selectbox("Selecione o desenho sugerido:", sugestoes)

    # 🔍 Mostrar resultados
    resultado = buscar_desenho(df, sugestao_selecionada)

    if not resultado.empty:
        st.success(f"Encontrado {len(resultado)} registro(s) para o desenho '{sugestao_selecionada}'")
        st.dataframe(resultado[['MÓDULO', 'DESENHO', 'REVISÃO']])
    else:
        st.warning("Desenho não encontrado.")
