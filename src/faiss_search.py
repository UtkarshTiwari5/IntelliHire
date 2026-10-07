# ============================================================
# IntelliHire V6 - FAISS Vector Search
# ============================================================

from typing import List, Dict, Any

import faiss
import numpy as np

from src.embeddings import generate_embeddings

# ============================================================
# BUILD FAISS INDEX
# ============================================================

def build_faiss_index(
    texts: List[str]
):
    """
    Build a FAISS index from text documents.
    """

    if not texts:
        return None, []

    embeddings = generate_embeddings(
        texts
    )

    vectors = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        vectors
    )

    return index, texts
# ============================================================
# FAISS SEARCH
# ============================================================

def faiss_search(
    query: str,
    index,
    texts: List[str],
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search the FAISS vector index.
    """

    if not query:
        return []

    if index is None:
        return []

    if not texts:
        return []

    if top_k <= 0:
        return []

    top_k = min(
        top_k,
        len(texts)
    )

    query_embedding = generate_embeddings(
        [query]
    )

    query_vector = np.array(
        query_embedding,
        dtype=np.float32
    )

    scores, indices = index.search(
        query_vector,
        top_k
    )

    results = []

    for score, position in zip(
        scores[0],
        indices[0]
    ):

        if position < 0:
            continue

        similarity = max(
            0.0,
            min(
                1.0,
                float(score)
            )
        )

        results.append(
            {
                "id": int(position),

                "text": texts[position],

                "similarity": round(
                    similarity,
                    4
                ),

                "score": round(
                    similarity * 100,
                    2
                )
            }
        )

    return results

# ============================================================
# FAISS DOCUMENT INDEX
# ============================================================

def build_document_faiss_index(
    documents: List[Dict[str, Any]]
):
    """
    Build FAISS index from documents containing text
    and optional metadata.
    """

    if not documents:
        return None, []

    valid_documents = []

    texts = []

    for document in documents:

        text = document.get(
            "text",
            ""
        )

        if not text:
            continue

        texts.append(text)

        valid_documents.append(
            document
        )

    if not texts:
        return None, []

    index, _ = build_faiss_index(
        texts
    )

    return index, valid_documents

# ============================================================
# FAISS DOCUMENT SEARCH
# ============================================================

def search_faiss_documents(
    query: str,
    index,
    documents: List[Dict[str, Any]],
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search FAISS document index and return metadata.
    """

    if not query:
        return []

    if index is None:
        return []

    if not documents:
        return []

    results = faiss_search(
        query,
        index,
        [
            document.get(
                "text",
                ""
            )
            for document in documents
        ],
        top_k
    )

    for result in results:

        document = documents[
            result["id"]
        ]

        result["metadata"] = document.get(
            "metadata",
            {}
        )

        result["document_id"] = document.get(
            "id",
            result["id"]
        )

    return results






