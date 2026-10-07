# ============================================================
# IntelliHire V6 - Vector Search Engine
# ============================================================

from typing import List, Dict, Any

import numpy as np

from src.embeddings import (
    generate_embedding,
    calculate_similarity
)

# ============================================================
# CREATE VECTOR INDEX
# ============================================================

def create_vector_index(
    texts: List[str]
) -> List[Dict[str, Any]]:
    """
    Convert a collection of texts into searchable vectors.
    """

    if not texts:
        return []

    index = []

    for item_id, text in enumerate(texts):

        embedding = generate_embedding(
            text
        )

        index.append(
            {
                "id": item_id,
                "text": text,
                "embedding": embedding
            }
        )

    return index

# ============================================================
# VECTOR SEARCH
# ============================================================

def vector_search(
    query: str,
    vector_index: List[Dict[str, Any]],
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search the vector index using semantic similarity.
    """

    if not query:
        return []

    if not vector_index:
        return []

    if top_k <= 0:
        return []

    query_embedding = generate_embedding(
        query
    )

    results = []

    for item in vector_index:

        similarity = calculate_similarity(
            query_embedding,
            item.get(
                "embedding",
                []
            )
        )

        results.append(
            {
                "id": item.get(
                    "id"
                ),

                "text": item.get(
                    "text",
                    ""
                ),

                "similarity": similarity,

                "score": round(
                    similarity * 100,
                    2
                )
            }
        )

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return results[:top_k]

# ============================================================
# METADATA VECTOR INDEX
# ============================================================

def create_metadata_vector_index(
    documents: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Create vector index from documents containing
    text and optional metadata.
    """

    if not documents:
        return []

    index = []

    for item_id, document in enumerate(
        documents
    ):

        text = document.get(
            "text",
            ""
        )

        if not text:
            continue

        embedding = generate_embedding(
            text
        )

        index.append(
            {
                "id": document.get(
                    "id",
                    item_id
                ),

                "text": text,

                "embedding": embedding,

                "metadata": document.get(
                    "metadata",
                    {}
                )
            }
        )

    return index

# ============================================================
# METADATA VECTOR SEARCH
# ============================================================

def search_documents(
    query: str,
    vector_index: List[Dict[str, Any]],
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search documents and preserve their metadata.
    """

    if not query:
        return []

    if not vector_index:
        return []

    if top_k <= 0:
        return []

    query_embedding = generate_embedding(
        query
    )

    results = []

    for item in vector_index:

        similarity = calculate_similarity(
            query_embedding,
            item.get(
                "embedding",
                []
            )
        )

        results.append(
            {
                "id": item.get(
                    "id"
                ),

                "text": item.get(
                    "text",
                    ""
                ),

                "similarity": similarity,

                "score": round(
                    similarity * 100,
                    2
                ),

                "metadata": item.get(
                    "metadata",
                    {}
                )
            }
        )

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return results[:top_k]















