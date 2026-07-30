from langchain_community.embeddings import FastEmbedEmbeddings


def get_embedding_model():
    return FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )