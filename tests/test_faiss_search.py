# ============================================================
# IntelliHire V6 - FAISS Vector Search Tests
# ============================================================

from src.faiss_search import (
    build_faiss_index,
    faiss_search,
    build_document_faiss_index,
    search_faiss_documents
)


# ============================================================
# TEST 1 - BUILD FAISS INDEX
# ============================================================

def test_build_faiss_index():

    texts = [
        "Python developer",
        "Machine Learning Engineer",
        "Data Scientist"
    ]

    index, stored_texts = build_faiss_index(
        texts
    )

    assert index is not None

    assert len(stored_texts) == 3

    assert index.ntotal == 3


# ============================================================
# TEST 2 - EMPTY FAISS INDEX
# ============================================================

def test_empty_faiss_index():

    index, stored_texts = build_faiss_index(
        []
    )

    assert index is None

    assert stored_texts == []


# ============================================================
# TEST 3 - FAISS SEARCH
# ============================================================

def test_faiss_search():

    texts = [
        "Python software developer",
        "Machine Learning Engineer",
        "Frontend React developer"
    ]

    index, stored_texts = build_faiss_index(
        texts
    )

    results = faiss_search(
        "Python developer",
        index,
        stored_texts,
        top_k=2
    )

    assert isinstance(
        results,
        list
    )

    assert len(results) == 2


# ============================================================
# TEST 4 - FAISS TOP RESULT
# ============================================================

def test_faiss_top_result():

    texts = [
        "Python software developer",
        "Machine Learning Engineer",
        "Frontend React developer"
    ]

    index, stored_texts = build_faiss_index(
        texts
    )

    results = faiss_search(
        "Python developer",
        index,
        stored_texts,
        top_k=1
    )

    assert len(results) == 1

    assert results[0]["text"] == (
        "Python software developer"
    )


# ============================================================
# TEST 5 - FAISS SCORE
# ============================================================

def test_faiss_score():

    texts = [
        "Python developer",
        "Data Scientist"
    ]

    index, stored_texts = build_faiss_index(
        texts
    )

    results = faiss_search(
        "Python",
        index,
        stored_texts,
        top_k=1
    )

    assert "score" in results[0]

    assert (
        0.0
        <= results[0]["score"]
        <= 100.0
    )


# ============================================================
# TEST 6 - FAISS SIMILARITY
# ============================================================

def test_faiss_similarity():

    texts = [
        "Python developer",
        "Machine Learning Engineer"
    ]

    index, stored_texts = build_faiss_index(
        texts
    )

    results = faiss_search(
        "Python programming",
        index,
        stored_texts,
        top_k=2
    )

    assert "similarity" in results[0]

    assert (
        0.0
        <= results[0]["similarity"]
        <= 1.0
    )


# ============================================================
# TEST 7 - TOP K
# ============================================================

def test_faiss_top_k():

    texts = [
        "Python",
        "Machine Learning",
        "Docker",
        "AWS",
        "React"
    ]

    index, stored_texts = build_faiss_index(
        texts
    )

    results = faiss_search(
        "technology",
        index,
        stored_texts,
        top_k=3
    )

    assert len(results) == 3


# ============================================================
# TEST 8 - TOP K GREATER THAN INDEX
# ============================================================

def test_faiss_top_k_greater_than_index():

    texts = [
        "Python",
        "Docker"
    ]

    index, stored_texts = build_faiss_index(
        texts
    )

    results = faiss_search(
        "Python",
        index,
        stored_texts,
        top_k=10
    )

    assert len(results) == 2


# ============================================================
# TEST 9 - EMPTY QUERY
# ============================================================

def test_faiss_empty_query():

    texts = [
        "Python developer"
    ]

    index, stored_texts = build_faiss_index(
        texts
    )

    results = faiss_search(
        "",
        index,
        stored_texts
    )

    assert results == []


# ============================================================
# TEST 10 - EMPTY TEXTS
# ============================================================

def test_faiss_empty_texts():

    results = faiss_search(
        "Python",
        None,
        []
    )

    assert results == []


# ============================================================
# TEST 11 - INVALID TOP K
# ============================================================

def test_faiss_invalid_top_k():

    texts = [
        "Python developer"
    ]

    index, stored_texts = build_faiss_index(
        texts
    )

    results = faiss_search(
        "Python",
        index,
        stored_texts,
        top_k=0
    )

    assert results == []


# ============================================================
# TEST 12 - BUILD DOCUMENT INDEX
# ============================================================

def test_build_document_faiss_index():

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

    index, stored_documents = (
        build_document_faiss_index(
            documents
        )
    )

    assert index is not None

    assert index.ntotal == 2

    assert len(
        stored_documents
    ) == 2


# ============================================================
# TEST 13 - DOCUMENT SEARCH
# ============================================================

def test_search_faiss_documents():

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

    index, stored_documents = (
        build_document_faiss_index(
            documents
        )
    )

    results = search_faiss_documents(
        "Python developer",
        index,
        stored_documents,
        top_k=1
    )

    assert len(results) == 1

    assert results[0]["document_id"] == (
        "job_1"
    )


# ============================================================
# TEST 14 - DOCUMENT METADATA
# ============================================================

def test_faiss_document_metadata():

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

    index, stored_documents = (
        build_document_faiss_index(
            documents
        )
    )

    results = search_faiss_documents(
        "Python",
        index,
        stored_documents,
        top_k=1
    )

    assert results[0]["metadata"][
        "category"
    ] == "Backend"

    assert results[0]["metadata"][
        "level"
    ] == "Junior"


# ============================================================
# TEST 15 - EMPTY DOCUMENTS
# ============================================================

def test_empty_document_index():

    index, documents = (
        build_document_faiss_index(
            []
        )
    )

    assert index is None

    assert documents == []


# ============================================================
# TEST 16 - EMPTY DOCUMENT SEARCH
# ============================================================

def test_empty_document_search():

    results = search_faiss_documents(
        "Python",
        None,
        []
    )

    assert results == []