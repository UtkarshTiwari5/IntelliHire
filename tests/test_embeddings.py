# ============================================================
# IntelliHire V6 - Embeddings Tests
# ============================================================

from src.embeddings import (
    normalize_text,
    generate_embedding,
    generate_embeddings,
    calculate_similarity,
    semantic_similarity,
    similarity_percentage
)


# ============================================================
# TEST 1 - TEXT NORMALIZATION
# ============================================================

def test_normalize_text():

    assert normalize_text(
        "  Python   Machine Learning  "
    ) == "Python Machine Learning"


# ============================================================
# TEST 2 - EMPTY TEXT
# ============================================================

def test_normalize_empty_text():

    assert normalize_text("") == ""

    assert normalize_text(None) == ""


# ============================================================
# TEST 3 - NORMALIZE NON STRING
# ============================================================

def test_normalize_non_string():

    assert normalize_text(123) == "123"


# ============================================================
# TEST 4 - GENERATE EMBEDDING
# ============================================================

def test_generate_embedding():

    embedding = generate_embedding(
        "Python developer"
    )

    assert isinstance(
        embedding,
        list
    )

    assert len(embedding) > 0


# ============================================================
# TEST 5 - EMPTY EMBEDDING
# ============================================================

def test_empty_embedding():

    assert generate_embedding(
        ""
    ) == []

    assert generate_embedding(
        None
    ) == []


# ============================================================
# TEST 6 - EMBEDDING DIMENSION
# ============================================================

def test_embedding_dimension():

    embedding = generate_embedding(
        "Machine Learning"
    )

    assert len(embedding) == 384


# ============================================================
# TEST 7 - BATCH EMBEDDINGS
# ============================================================

def test_generate_embeddings():

    embeddings = generate_embeddings(
        [
            "Python",
            "Machine Learning",
            "Docker"
        ]
    )

    assert isinstance(
        embeddings,
        list
    )

    assert len(embeddings) == 3

    assert all(
        isinstance(
            embedding,
            list
        )
        for embedding in embeddings
    )


# ============================================================
# TEST 8 - EMPTY BATCH
# ============================================================

def test_empty_batch_embeddings():

    assert generate_embeddings(
        []
    ) == []


# ============================================================
# TEST 9 - SIMILARITY
# ============================================================

def test_calculate_similarity():

    embedding = generate_embedding(
        "Python programming"
    )

    similarity = calculate_similarity(
        embedding,
        embedding
    )

    assert similarity > 0.99


# ============================================================
# TEST 10 - DIFFERENT EMBEDDINGS
# ============================================================

def test_different_embeddings():

    embedding_a = generate_embedding(
        "Python programming"
    )

    embedding_b = generate_embedding(
        "Cooking food"
    )

    similarity = calculate_similarity(
        embedding_a,
        embedding_b
    )

    assert 0.0 <= similarity <= 1.0


# ============================================================
# TEST 11 - EMPTY SIMILARITY
# ============================================================

def test_empty_similarity():

    assert calculate_similarity(
        [],
        []
    ) == 0.0


# ============================================================
# TEST 12 - SEMANTIC SIMILARITY
# ============================================================

def test_semantic_similarity():

    similarity = semantic_similarity(
        "Machine Learning",
        "ML"
    )

    assert 0.0 <= similarity <= 1.0


# ============================================================
# TEST 13 - SIMILAR TEXT
# ============================================================

def test_similar_text():

    similarity = semantic_similarity(
        "Python developer",
        "Python software developer"
    )

    assert similarity > 0.5


# ============================================================
# TEST 14 - EMPTY SEMANTIC TEXT
# ============================================================

def test_empty_semantic_similarity():

    assert semantic_similarity(
        "",
        "Python"
    ) == 0.0

    assert semantic_similarity(
        "Python",
        ""
    ) == 0.0


# ============================================================
# TEST 15 - SIMILARITY PERCENTAGE
# ============================================================

def test_similarity_percentage():

    percentage = similarity_percentage(
        "Python developer",
        "Python software developer"
    )

    assert 0.0 <= percentage <= 100.0


# ============================================================
# TEST 16 - EMPTY SIMILARITY PERCENTAGE
# ============================================================

def test_empty_similarity_percentage():

    assert similarity_percentage(
        "",
        "Python"
    ) == 0.0