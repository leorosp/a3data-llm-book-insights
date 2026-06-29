"""Interface Streamlit para consulta semantica das avaliacoes."""

from __future__ import annotations

import sys

import streamlit as st

# Permite importar o pacote local sem instalar o projeto como biblioteca.
sys.path.append("src")

from a3_book_insights.config import VECTORSTORE_DIR
from a3_book_insights.rag_chain import load_vectorstore


def converter_nota(valor: object) -> float | None:
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def passa_filtro_nota(nota: float | None, nota_min: float | None, nota_max: float | None) -> bool:
    if nota is None:
        return False
    if nota_min is not None and nota < nota_min:
        return False
    if nota_max is not None and nota > nota_max:
        return False
    return True


def resumir_texto(texto: str, limite: int = 700) -> str:
    texto_limpo = " ".join(texto.split())
    if len(texto_limpo) <= limite:
        return texto_limpo
    return f"{texto_limpo[:limite].rstrip()}..."


@st.cache_resource(show_spinner="Carregando base vetorial local...")
def carregar_base_vetorial():
    return load_vectorstore(VECTORSTORE_DIR)


def consultar(pergunta: str, nota_min: float | None, nota_max: float | None, top_k: int, fetch_k: int):
    vectorstore = carregar_base_vetorial()
    candidatos = vectorstore.similarity_search_with_score(pergunta, k=max(fetch_k, top_k))

    resultados = []
    for doc, distancia in candidatos:
        nota = converter_nota(doc.metadata.get("score"))
        if passa_filtro_nota(nota, nota_min, nota_max):
            resultados.append((doc, distancia, nota))
        if len(resultados) >= top_k:
            break

    return resultados


st.set_page_config(page_title="A3Data - Analise de Avaliacoes", layout="wide")

st.title("Analise Semantica de Avaliacoes de Livros")

with st.sidebar:
    st.header("Filtros")
    modo_nota = st.radio(
        "Recorte de notas",
        ["Todas", "Notas baixas", "Notas altas", "Intervalo"],
        horizontal=False,
    )

    nota_min: float | None = None
    nota_max: float | None = None

    if modo_nota == "Notas baixas":
        nota_max = st.slider("Nota maxima", min_value=1.0, max_value=5.0, value=2.0, step=0.5)
    elif modo_nota == "Notas altas":
        nota_min = st.slider("Nota minima", min_value=1.0, max_value=5.0, value=4.0, step=0.5)
    elif modo_nota == "Intervalo":
        intervalo = st.slider("Intervalo de notas", min_value=1.0, max_value=5.0, value=(2.0, 4.0), step=0.5)
        nota_min, nota_max = intervalo

    top_k = st.slider("Evidencias exibidas", min_value=1, max_value=10, value=5)
    fetch_k = st.slider("Candidatos analisados", min_value=10, max_value=200, value=100, step=10)

pergunta = st.text_input(
    "Pergunta de negocio",
    value="Identificar oportunidades de melhoria nas avaliacoes de livros",
)

col_consultar, col_status = st.columns([1, 3])
with col_consultar:
    consultar_agora = st.button("Consultar", type="primary", use_container_width=True)

with col_status:
    st.caption("Consulta local com embeddings sentence-transformers e base vetorial Chroma.")

if consultar_agora:
    if not pergunta.strip():
        st.warning("Informe uma pergunta de negocio para consultar a base.")
    else:
        with st.spinner("Buscando evidencias na base vetorial local..."):
            resultados = consultar(pergunta, nota_min, nota_max, top_k, fetch_k)

        if not resultados:
            st.info("Nenhuma evidencia encontrada com os filtros informados.")
        else:
            st.subheader("Evidencias Recuperadas")
            st.metric("Total exibido", len(resultados))

            for posicao, (doc, distancia, nota) in enumerate(resultados, start=1):
                metadata = doc.metadata
                titulo = metadata.get("title") or "Titulo nao informado"
                usuario = metadata.get("user_id") or "Usuario nao informado"

                with st.container(border=True):
                    col_titulo, col_nota, col_distancia = st.columns([4, 1, 1])
                    col_titulo.markdown(f"**{posicao}. {titulo}**")
                    col_nota.metric("Nota", f"{nota:g}" if nota is not None else "N/D")
                    col_distancia.metric("Distancia", f"{distancia:.2f}")

                    st.caption(f"Usuario: {usuario}")
                    st.write(resumir_texto(doc.page_content))
