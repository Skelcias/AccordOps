from accordops.db import *
from accordops.embedder import *
from accordops.rag import *
from pathlib import Path

# chunks = chunker(Path("documents/policies/expense_policy.md"))

# with get_connection() as conn:
#     for chunk in chunks:
#         category = chunk["category"]
#         embed = embed_text(chunk["content"])
#         add_document_chunk(
#             conn,
#             source="expense_policy.md",
#             embedding=embed,
#             content=chunk["content"],
#             category=category,
#         )


query = "Est-ce que les boissons alcoolisées sont remboursées au restaurant ? "
embedding = embed_text(query)

with get_connection() as conn:
    chunks = search_similar_chunks(conn, embedding)


for chunk in chunks:
    print(chunk[2])
