
def validate_collection(collection, expected_metadata: dict) -> None:
    metadata = collection.metadata or {}
  
    for field in expected_metadata:
        if metadata.get(field, "<missing>") != expected_metadata[field]:
            raise ValueError(
                            f"{field}: expected {expected_metadata[field]!r}, "
                            f"stored {metadata.get(field, '<missing>')!r}"
                        )

def search_chroma(query: str, model, collection, top_k=3):
    if len(query.strip()) < 1:
            raise ValueError("Query must not be blank")
    if top_k < 1:
        raise ValueError("top_k must be at least 1")
    
    q_embeddings = model.encode(['Represent this sentence for searching relevant passages: '
                                + query])
    hits = collection.query(
            query_embeddings=q_embeddings,
            n_results=top_k)
    return [{"rank": i + 1,
                "chunk_id": hits['ids'][0][i],
                "score": float(1 - hits['distances'][0][i]),
                "text": hits['documents'][0][i],
                "metadata": {
                    "paper_id": hits['metadatas'][0][i]['paper_id'],
                    "source_sha256": hits['metadatas'][0][i]['source_sha256'],
                    "page": hits['metadatas'][0][i]['page'],
                    "start_word": hits['metadatas'][0][i]['start_word'],
                    "end_word": hits['metadatas'][0][i]['end_word']
                }} 
            for i in range(len(hits["ids"][0]))]
        