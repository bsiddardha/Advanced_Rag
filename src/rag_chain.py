from src.llm import get_llm
from src.prompt import prompt
from src.hybrid_retriever import hybrid_search
from src.reranker import rerank


def ask_question(vector_store, bm25_retriever, question):
    """
    Retrieve relevant log chunks using Hybrid Search (FAISS + BM25)
    and generate an answer using the LLM.
    """

    # Retrieve documents
    docs = hybrid_search(
    vector_store,
    bm25_retriever,
    question
    )

    docs = rerank(question, docs)

    # Build context for the LLM
    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # Initialize the LLM
    llm = get_llm()

    # Create the chain
    chain = prompt | llm

    # Generate the response
    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return response.content, docs