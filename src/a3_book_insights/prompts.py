from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Voce e um especialista de ciencia de dados que apoia uma editora na analise "
            "de avaliacoes de livros. Responda com insights orientados ao negocio. Use "
            "apenas o contexto fornecido. Se as evidencias forem fracas, indique o que "
            "esta faltando. Seja conciso.",
        ),
        (
            "human",
            "Pergunta: {input}\n\nContexto:\n{context}\n\n"
            "Retorne: resposta executiva, resumo das evidencias e proxima acao sugerida.",
        ),
    ]
)
