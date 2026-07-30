from src.loader import load_logs

docs = load_logs("uploads/server.log")

print(docs)

print(docs[0].page_content[:300])