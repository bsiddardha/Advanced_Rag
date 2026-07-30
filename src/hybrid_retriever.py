from src.retriever import get_retriever


def hybrid_search(vector_store, bm25_retriever, question):
    """
    Combine FAISS and BM25 results and remove duplicates.
    """

    faiss_docs = get_retriever(vector_store).invoke(question)
    bm25_docs = bm25_retriever.invoke(question)

    combined = []
    seen = set()

    for doc in faiss_docs + bm25_docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            combined.append(doc)

    return combined