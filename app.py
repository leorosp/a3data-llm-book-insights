"""Interface Streamlit para analise executiva e consulta semantica."""

from __future__ import annotations

import sys

import pandas as pd
import streamlit as st

# Permite importar o pacote local sem instalar o projeto como biblioteca.
sys.path.append("src")

from a3_book_insights.business_metrics import (
    calcular_impacto_operacional,
    distribuicao_notas,
    formatar_moeda,
    gerar_metricas_base,
    principais_autores,
    principais_categorias,
)
from a3_book_insights.config import PROCESSED_REVIEWS_FILE, VECTORSTORE_DIR
from a3_book_insights.rag_chain import load_vectorstore
from a3_book_insights.retrieval import buscar_evidencias, limpar_valor_metadata, resumir_texto


@st.cache_resource(show_spinner="Carregando base vetorial local...")
def carregar_base_vetorial():
    return load_vectorstore(VECTORSTORE_DIR)


@st.cache_data(show_spinner=False)
def carregar_base_tratada() -> pd.DataFrame | None:
    if not PROCESSED_REVIEWS_FILE.exists():
        return None
    return pd.read_csv(PROCESSED_REVIEWS_FILE, low_memory=False)


def formatar_percentual(valor: float) -> str:
    return f"{valor:.1%}".replace(".", ",")


def formatar_numero(valor: int | float) -> str:
    if isinstance(valor, float):
        return f"{valor:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{valor:,}".replace(",", ".")


def tabela_top(valores: list[tuple[str, int]]) -> pd.DataFrame:
    return pd.DataFrame(valores, columns=["item", "quantidade"])


def consultar(pergunta: str, nota_min: float | None, nota_max: float | None, top_k: int, fetch_k: int):
    vectorstore = carregar_base_vetorial()
    return buscar_evidencias(
        vectorstore=vectorstore,
        pergunta=pergunta,
        nota_min=nota_min,
        nota_max=nota_max,
        top_k=top_k,
        fetch_k=fetch_k,
    )


st.set_page_config(page_title="A3Data - Analise de Avaliacoes", layout="wide")

st.title("Analise Semantica de Avaliacoes de Livros")
st.caption("POC para acelerar a exploracao de avaliacoes, recuperar evidencias e estimar impacto operacional.")

with st.sidebar:
    st.header("Parametros")
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

base_tratada = carregar_base_tratada()
impacto = calcular_impacto_operacional()

tab_executiva, tab_consulta = st.tabs(["Visao executiva", "Consulta semantica"])

with tab_executiva:
    st.subheader("Impacto operacional estimado")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Processo atual", f"{impacto['dias_processo_manual']:.0f} dias")
    col2.metric("Equipe envolvida", f"{impacto['analistas']:.0f} analistas")
    col3.metric("Custo atual por ciclo", formatar_moeda(impacto["custo_processo_manual"]))
    col4.metric(
        "Economia estimada",
        formatar_moeda(impacto["economia_por_ciclo"]),
        delta=f"{formatar_percentual(impacto['reducao_percentual'])} menor",
    )
    st.caption(
        "Estimativa baseada em 5 analistas, salario mensal de R$ 5.000,00 e 22 dias uteis por mes."
    )

    if base_tratada is None:
        st.info("Execute a preparacao dos dados para visualizar as metricas da base tratada.")
    else:
        metricas = gerar_metricas_base(base_tratada)

        st.subheader("Resumo da amostra analisada")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avaliacoes", formatar_numero(metricas["total_avaliacoes"]))
        col2.metric("Livros", formatar_numero(metricas["livros_unicos"]))
        col3.metric("Usuarios", formatar_numero(metricas["usuarios_unicos"]))
        col4.metric("Nota media", formatar_numero(metricas["nota_media"]))

        col1, col2, col3 = st.columns(3)
        col1.metric("Avaliacoes baixas", formatar_percentual(metricas["percentual_baixas"]))
        col2.metric("Avaliacoes altas", formatar_percentual(metricas["percentual_altas"]))
        col3.metric("Palavras por avaliacao", formatar_numero(metricas["palavras_medias_por_avaliacao"]))

        st.subheader("Distribuicao de notas")
        distribuicao = distribuicao_notas(base_tratada)
        if not distribuicao.empty:
            distribuicao_view = distribuicao.copy()
            distribuicao_view["percentual"] = distribuicao_view["percentual"].map(formatar_percentual)
            st.dataframe(distribuicao_view, use_container_width=True, hide_index=True)

        st.subheader("Autores e categorias mais frequentes")
        col_autores, col_categorias = st.columns(2)
        with col_autores:
            autores = tabela_top(principais_autores(base_tratada, top_n=8))
            st.dataframe(autores, use_container_width=True, hide_index=True)
        with col_categorias:
            categorias = tabela_top(principais_categorias(base_tratada, top_n=8))
            st.dataframe(categorias, use_container_width=True, hide_index=True)

        st.subheader("Metricas recomendadas para avaliacao")
        st.markdown(
            "- Cobertura: quantidade de evidencias recuperadas por pergunta.\n"
            "- Fidelidade: evidencias sustentam a resposta sem contradicao.\n"
            "- Utilidade: resposta ajuda a priorizar autores, categorias ou usuarios.\n"
            "- Acionabilidade: resultado sugere uma decisao ou proxima investigacao.\n"
            "- Tempo de analise: comparacao entre o fluxo manual e a POC."
        )

with tab_consulta:
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
        elif not (VECTORSTORE_DIR / "chroma.sqlite3").exists():
            st.warning("Execute a criacao da base vetorial antes de consultar as evidencias.")
        else:
            with st.spinner("Buscando evidencias na base vetorial local..."):
                resultados = consultar(pergunta, nota_min, nota_max, top_k, fetch_k)

            if not resultados:
                st.info("Nenhuma evidencia encontrada com os filtros informados.")
            else:
                st.subheader("Evidencias recuperadas")
                st.metric("Total exibido", len(resultados))

                for posicao, evidencia in enumerate(resultados, start=1):
                    doc = evidencia.documento
                    metadata = doc.metadata
                    titulo = limpar_valor_metadata(metadata.get("title"), padrao="Titulo nao informado")
                    usuario = limpar_valor_metadata(metadata.get("user_id"), padrao="Usuario nao informado")
                    nota = evidencia.nota

                    with st.container(border=True):
                        col_titulo, col_nota, col_distancia = st.columns([4, 1, 1])
                        col_titulo.markdown(f"**{posicao}. {titulo}**")
                        col_nota.metric("Nota", f"{nota:g}" if nota is not None else "N/D")
                        col_distancia.metric("Distancia", f"{evidencia.distancia:.2f}")

                        st.caption(f"Usuario: {usuario}")
                        st.write(resumir_texto(doc.page_content, limite=700))
