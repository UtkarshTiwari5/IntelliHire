# ============================================================
# IntelliHire V6 - NLP + Embeddings + Vector Search
# ============================================================

from typing import List, Union

import numpy as np

from sentence_transformers import SentenceTransformer


# ============================================================
# EMBEDDING MODEL
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"


_model = None


def get_embedding_model():
    """
    Load the embedding model lazily.

    The model is loaded only when required.
    """

    global _model

    if _model is None:

        _model = SentenceTransformer(
            MODEL_NAME
        )

    return _model

    # ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(
    text: Union[str, None]
) -> str:
    """
    Normalize input text before embedding.
    """

    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    text = text.strip()

    return " ".join(
        text.split()
    )

    # ============================================================
# GENERATE EMBEDDING
# ============================================================

def generate_embedding(
    text: Union[str, None]
) -> List[float]:
    """
    Generate an embedding vector for text.
    """

    text = normalize_text(
        text
    )

    if not text:

        return []

    model = get_embedding_model()

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding.astype(
        np.float32
    ).tolist()

    # ============================================================
# BATCH EMBEDDINGS
# ============================================================

def generate_embeddings(
    texts: List[str]
) -> List[List[float]]:
    """
    Generate embeddings for multiple texts.
    """

    if not texts:

        return []

    normalized_texts = [

        normalize_text(text)

        for text in texts
    ]

    model = get_embedding_model()

    embeddings = model.encode(
        normalized_texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings.astype(
        np.float32
    ).tolist()

# ============================================================
# COSINE SIMILARITY
# ============================================================

def calculate_similarity(
    embedding_a: List[float],
    embedding_b: List[float]
) -> float:
    """
    Calculate cosine similarity between two embeddings.
    """

    if not embedding_a or not embedding_b:

        return 0.0

    vector_a = np.array(
        embedding_a,
        dtype=np.float32
    )

    vector_b = np.array(
        embedding_b,
        dtype=np.float32
    )

    norm_a = np.linalg.norm(
        vector_a
    )

    norm_b = np.linalg.norm(
        vector_b
    )

    if norm_a == 0 or norm_b == 0:

        return 0.0

    similarity = np.dot(
        vector_a,
        vector_b
    ) / (
        norm_a * norm_b
    )

    return round(
        float(similarity),
        4
    )

# ============================================================
# SEMANTIC TEXT SIMILARITY
# ============================================================

def semantic_similarity(
    text_a: Union[str, None],
    text_b: Union[str, None]
) -> float:
    """
    Calculate semantic similarity between two texts.
    """

    if not normalize_text(text_a):

        return 0.0

    if not normalize_text(text_b):

        return 0.0

    embedding_a = generate_embedding(
        text_a
    )

    embedding_b = generate_embedding(
        text_b
    )

    return calculate_similarity(
        embedding_a,
        embedding_b
    )

# ============================================================
# SIMILARITY PERCENTAGE
# ============================================================

def similarity_percentage(
    text_a: Union[str, None],
    text_b: Union[str, None]
) -> float:
    """
    Convert semantic similarity into percentage.
    """

    similarity = semantic_similarity(
        text_a,
        text_b
    )

    percentage = similarity * 100

    return round(
        percentage,
        2
    )









