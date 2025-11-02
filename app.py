import streamlit as st
import pandas as pd

# 📘 Título do app
st.title("📘 Desenhos P83")

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

# 🔄 Carregar dados automaticamente do GitHub
df = carregar_dados(URL_PLANILHA)

# 🔎 Entrada de texto para busca parcial
termo_input = st.text_input("Digite parte do nome do desenho (ex: 09A-394):")

# 📋 Mostrar sugestões e resultados em tempo real
if termo_input:
    resultados = buscar_desenho(df, termo_input)
    desenhos_encontrados = resultados['DESENHO'].unique()

    if len(desenhos_encontrados) > 0:
        st.markdown("**Sugestões encontradas:**")
        for desenho in desenhos_encontrados:
            st.markdown(f"🔹 **{desenho}**")

            # Mostrar revisões únicas para cada desenho
            revisoes = resultados[resultados['DESENHO'] == desenho]['REVISÃO'].drop_duplicates().tolist()
            st.markdown("Revisões disponíveis:")
            for rev in revisoes:
                st.markdown(f"- Revisão: `{rev}`")
            st.markdown("---")
    else:
        st.info("Nenhum desenho encontrado com esse trecho.")
