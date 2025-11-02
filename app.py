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

# 🔠 Função para ordenar revisões: 0 primeiro, depois letras
def ordenar_revisoes(revisoes):
    numericas = [r for r in revisoes if str(r).isdigit()]
    letras = [r for r in revisoes if str(r).isalpha()]
    return sorted(numericas, key=int) + sorted(letras)

# 🔄 Carregar dados automaticamente do GitHub
df = carregar_dados(URL_PLANILHA)

# 🔎 Entrada de texto para busca parcial
termo_input = st.text_input("Digite parte do nome do desenho (ex: 09A-394):")

# 📋 Mostrar sugestões e resultados em tempo real
if termo_input:
    resultados = buscar_desenho(df, termo_input)
    desenhos_encontrados = resultados['DESENHO'].unique()

    if len(desenhos_encontrados) > 0:
        st.markdown("### 🔍 Sugestões encontradas:")
        for desenho in desenhos_encontrados:
            st.subheader(f"📄 {desenho}")

            # Filtrar revisões únicas e ordenar corretamente
            revisoes = resultados[resultados['DESENHO'] == desenho]['REVISÃO'].drop_duplicates().tolist()
            revisoes_ordenadas = ordenar_revisoes(revisoes)

            # Última letra como revisão mais recente
            letras = [r for r in revisoes_ordenadas if str(r).isalpha()]
            ultima_revisao = letras[-1] if letras else None

            st.markdown("**Revisões disponíveis:**")
            cols = st.columns(len(revisoes_ordenadas))
            for i, rev in enumerate(revisoes_ordenadas):
                destaque = (
                    "background-color:#ffd966;color:#000000;" if rev == ultima_revisao
                    else "background-color:#e0e0e0;color:#000000;"
                )
                cols[i].markdown(
                    f"<div style='{destaque}padding:6px;border-radius:6px;text-align:center;font-weight:bold;'>{rev}</div>",
                    unsafe_allow_html=True
                )
            st.markdown("---")
    else:
        st.info("Nenhum desenho encontrado com esse trecho.")
