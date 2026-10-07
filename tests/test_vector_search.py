# ============================================================
# IntelliHire V6 - Vector Search Tests
# ============================================================

from src.vector_search import (
    create_vector_index,
    vector_search,
    create_metadata_vector_index,
    search_documents
)


# ============================================================
# TEST 1 - CREATE VECTOR INDEX
# ============================================================

def test_create_vector_index():

    texts = [
        "Python developer",
        "Machine Learning Engineer",
        "Data Scientist"
    ]

    index = create_vector_index(
        texts
    )

    assert isinstance(
        index,
        list
    )

    assert len(index) == 3

    assert index[0]["id"] == 0

    assert index[0]["text"] == (
        "Python developer"
    )

    assert len(
        index[0]["embedding"]
    ) == 384


# ============================================================
# TEST 2 - EMPTY VECTOR INDEX
# ============================================================

def test_empty_vector_index():

    assert create_vector_index(
        []
    ) == []


# ============================================================
# TEST 3 - VECTOR SEARCH
# ============================================================

def test_vector_search():

    index = create_vector_index(
        [
            "Python software developer",
            "Machine Learning Engineer",
            "Frontend React developer"
        ]
    )

    results = vector_search(
        "Python developer",
        index,
        top_k=2
    )

    assert isinstance(
        results,
        list
    )

    assert len(results) == 2

    assert results[0]["text"] == (
        "Python software developer"
    )


# ============================================================
# TEST 4 - SEARCH RESULT SCORE
# ============================================================

def test_vector_search_score():

    index = create_vector_index(
        [
            "Python developer",
            "Data Scientist"
        ]
    )

    results = vector_search(
        "Python",
        index,
        top_k=1
    )

    assert "score" in results[0]

    assert 0.0 <= results[0]["score"] <= 100.0


# ============================================================
# TEST 5 - SEARCH RESULT SIMILARITY
# ============================================================

def test_vector_search_similarity():

    index = create_vector_index(
        [
            "Python developer",
            "Machine Learning Engineer"
        ]
    )

    results = vector_search(
        "Python programming",
        index,
        top_k=2
    )

    assert "similarity" in results[0]

    assert (
        0.0
        <= results[0]["similarity"]
        <= 1.0
    )


# ============================================================
# TEST 6 - TOP K
# ============================================================

def test_vector_search_top_k():

    index = create_vector_index(
        [
            "Python",
            "Machine Learning",
            "Docker",
            "AWS",
            "React"
        ]
    )

    results = vector_search(
        "technology",
        index,
        top_k=3
    )

    assert len(results) == 3


# ============================================================
# TEST 7 - TOP K GREATER THAN INDEX
# ============================================================

def test_top_k_greater_than_index():

    index = create_vector_index(
        [
            "Python",
            "Docker"
        ]
    )

    results = vector_search(
        "Python",
        index,
        top_k=10
    )

    assert len(results) == 2


# ============================================================
# TEST 8 - EMPTY QUERY
# ============================================================

def test_empty_query():

    index = create_vector_index(
        [
            "Python developer"
        ]
    )

    assert vector_search(
        "",
        index
    ) == []


# ============================================================
# TEST 9 - EMPTY SEARCH INDEX
# ============================================================

def test_empty_search_index():

    assert vector_search(
        "Python",
        []
    ) == []


# ============================================================
# TEST 10 - INVALID TOP K
# ============================================================

def test_invalid_top_k():

    index = create_vector_index(
        [
            "Python developer"
        ]
    )

    assert vector_search(
        "Python",
        index,
        top_k=0
    ) == []


# ============================================================
# TEST 11 - CREATE METADATA INDEX
# ============================================================

def test_create_metadata_vector_index():

    documents = [

        {
            "id": "job_1",

            "text": "Python Developer",

            "metadata": {
                "category": "Backend"
            }
        },

        {
            "id": "job_2",

            "text": "Machine Learning Engineer",

            "metadata": {
                "category": "AI"
            }
        }

    ]

    index = create_metadata_vector_index(
        documents
    )

    assert len(index) == 2

    assert index[0]["id"] == "job_1"

    assert index[0]["metadata"][
        "category"
    ] == "Backend"


# ============================================================
# TEST 12 - EMPTY METADATA INDEX
# ============================================================

def test_empty_metadata_index():

    assert create_metadata_vector_index(
        []
    ) == []


# ============================================================
# TEST 13 - SEARCH DOCUMENTS
# ============================================================

def test_search_documents():

    documents = [

        {
            "id": "job_1",

            "text": "Python Backend Developer",

            "metadata": {
                "category": "Backend"
            }
        },

        {
            "id": "job_2",

            "text": "Machine Learning Engineer",

            "metadata": {
                "category": "AI"
            }
        }

    ]

    index = create_metadata_vector_index(
        documents
    )

    results = search_documents(
        "Python developer",
        index,
        top_k=1
    )

    assert len(results) == 1

    assert results[0]["id"] == "job_1"


# ============================================================
# TEST 14 - DOCUMENT METADATA
# ============================================================

def test_document_metadata():

    documents = [

        {
            "id": "job_1",

            "text": "Python Developer",

            "metadata": {
                "category": "Backend",
                "level": "Junior"
            }
        }

    ]

    index = create_metadata_vector_index(
        documents
    )

    results = search_documents(
        "Python",
        index,
        top_k=1
    )

    assert results[0]["metadata"][
        "category"
    ] == "Backend"

    assert results[0]["metadata"][
        "level"
    ] == "Junior"


# ============================================================
# TEST 15 - EMPTY DOCUMENT QUERY
# ============================================================

def test_empty_document_query():

    index = create_metadata_vector_index(
        [
            {
                "id": "job_1",
                "text": "Python",
                "metadata": {}
            }
        ]
    )

    assert search_documents(
        "",
        index
    ) == []


# ============================================================
# TEST 16 - EMPTY DOCUMENT INDEX
# ============================================================

def test_empty_document_index():

    assert search_documents(
        "Python",
        []
    ) == []

    