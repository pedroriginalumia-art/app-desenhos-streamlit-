import streamlit as st
import pandas as pd
from PIL import Image

# 📁 Carregar a logo da Petrobras
logo = Image.open("petrobras-seeklogo.png")  # Certifique-se de que o arquivo está na mesma pasta do script

# 🔷 Cabeçalho com logo e título alinhados verticalmente
col1, col2 = st.columns([1, 6])
with col1:
    st.image(logo, width=60)
with col2:
    st.markdown("<h1 style='margin-top:14px;'>Desenhos P83</h1>", unsafe_allow_html=True)

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
        st.markdown("### 🔍 Desenhos Encontrados:")
        for desenho in desenhos_encontrados:
            st.subheader(f"📄 {desenho}")

            # Filtrar revisões únicas e ordenar corretamente
            revisoes = resultados[resultados['DESENHO'] == desenho]['REVISÃO'].drop_duplicates().tolist()
            revisoes_ordenadas = ordenar_revisoes(revisoes)

            # ✅ Última revisão é a última da lista ordenada
            ultima_revisao = revisoes_ordenadas[-1] if revisoes_ordenadas else None

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

            # 🟨 Comentário explicativo abaixo da última revisão, na coluna correta
            if ultima_revisao:
                for i, rev in enumerate(revisoes_ordenadas):
                    if rev == ultima_revisao:
                        cols[i].markdown(
                            f"<div style='margin-top:6px;color:#ffd966;font-weight:bold;'>⬆ Esta é a última revisão disponível</div>",
                            unsafe_allow_html=True
                        )

            st.markdown("---")
    else:
        st.info("Nenhum desenho encontrado com esse trecho.")
