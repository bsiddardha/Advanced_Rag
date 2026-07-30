from pathlib import Path

from langchain_core.documents import Document


def load_logs(file_path: str):
    path = Path(file_path)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    return [
        Document(
            page_content=text,
            metadata={
                "source": path.name
            }
        )
    ]

# # The text will be created into an object 
# Document(
#     page_content="""
# INFO Server Started
# INFO Connected to Database
# ERROR Database Timeout
# WARNING Retrying...
# """,
#     metadata={
#         "source": "server.log"
#     }
# )

#Exmaple for thsi 