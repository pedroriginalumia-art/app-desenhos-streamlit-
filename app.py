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

# 📋 Mostrar sugestões abaixo da caixa de pesquisa
if termo_input:
    sugestoes = df[df['DESENHO'].astype(str).str.contains(termo_input, case=False, na=False)]['DESENHO'].unique()

    if len(sugestoes) > 0:
        st.markdown("**Sugestões encontradas:**")
        for sugestao in sugestoes:
            if st.button(sugestao):
                resultado = buscar_desenho(df, sugestao)

                if not resultado.empty:
                    st.success(f"Encontrado {len(resultado)} registro(s) para o desenho '{sugestao}'")

                    # Extrair revisões únicas
                    revisoes = resultado['REVISÃO'].drop_duplicates().tolist()

                    # Exibir como lista simples
                    st.markdown("**Revisões disponíveis:**")
                    for rev in revisoes:
                        st.markdown(f"- Revisão: `{rev}`")
                else:
                    st.warning("Desenho não encontrado.")
                break
    else:
        st.info("Nenhuma sugestão encontrada.")


