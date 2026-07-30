from langchain_core.documents import Document


def split_documents(documents, lines_per_chunk=20, overlap=5):
    """
    Split log documents by log lines instead of characters.
    """

    chunks = []

    for document in documents:

        lines = document.page_content.splitlines()

        step = lines_per_chunk - overlap

        for i in range(0, len(lines), step):

            chunk_lines = lines[i:i + lines_per_chunk]

            if not chunk_lines:
                continue

            chunk_text = "\n".join(chunk_lines)

            chunks.append(
                Document(
                    page_content=chunk_text,
                    metadata=document.metadata
                )
            )

    return chunks