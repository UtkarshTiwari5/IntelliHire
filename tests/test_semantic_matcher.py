# ============================================================
# IntelliHire V6 - Semantic Matcher Tests
# ============================================================

from src.semantic_matcher import (
    calculate_semantic_score,
    calculate_hybrid_score,
    semantic_match_resume_to_job,
    hybrid_resume_job_match,
    rank_jobs_by_semantic_similarity
)


# ============================================================
# TEST 1 - SEMANTIC SCORE
# ============================================================

def test_calculate_semantic_score():

    score = calculate_semantic_score(
        "Python software developer",
        "Python developer"
    )

    assert 0.0 <= score <= 100.0


# ============================================================
# TEST 2 - EMPTY RESUME
# ============================================================

def test_empty_resume():

    assert calculate_semantic_score(
        "",
        "Python developer"
    ) == 0.0


# ============================================================
# TEST 3 - EMPTY JOB
# ============================================================

def test_empty_job():

    assert calculate_semantic_score(
        "Python developer",
        ""
    ) == 0.0


# ============================================================
# TEST 4 - HYBRID SCORE
# ============================================================

def test_hybrid_score():

    score = calculate_hybrid_score(
        80,
        60
    )

    assert score == 70.0


# ============================================================
# TEST 5 - KEYWORD ONLY
# ============================================================

def test_keyword_only():

    score = calculate_hybrid_score(
        80,
        60,
        keyword_weight=1,
        semantic_weight=0
    )

    assert score == 80.0


# ============================================================
# TEST 6 - SEMANTIC ONLY
# ============================================================

def test_semantic_only():

    score = calculate_hybrid_score(
        80,
        60,
        keyword_weight=0,
        semantic_weight=1
    )

    assert score == 60.0


# ============================================================
# TEST 7 - ZERO WEIGHTS
# ============================================================

def test_zero_weights():

    assert calculate_hybrid_score(
        80,
        60,
        0,
        0
    ) == 0.0


# ============================================================
# TEST 8 - SEMANTIC MATCH RESULT
# ============================================================

def test_semantic_match_resume_to_job():

    result = semantic_match_resume_to_job(
        "Python developer",
        "Python software developer"
    )

    assert "semantic_score" in result

    assert (
        0.0
        <= result["semantic_score"]
        <= 100.0
    )

    assert (
        result["resume_text_available"]
        is True
    )

    assert (
        result["job_description_available"]
        is True
    )


# ============================================================
# TEST 9 - HYBRID MATCH
# ============================================================

def test_hybrid_resume_job_match():

    result = hybrid_resume_job_match(
        "Python developer",
        "Python software developer",
        80
    )

    assert "keyword_score" in result

    assert "semantic_score" in result

    assert "hybrid_score" in result

    assert (
        0.0
        <= result["hybrid_score"]
        <= 100.0
    )


# ============================================================
# TEST 10 - EMPTY HYBRID MATCH
# ============================================================

def test_empty_hybrid_match():

    result = hybrid_resume_job_match(
        "",
        "",
        50
    )

    assert result["semantic_score"] == 0.0


# ============================================================
# TEST 11 - RANK JOBS
# ============================================================

def test_rank_jobs():

    jobs = [

        {
            "id": "job_1",

            "job_title": "Python Developer",

            "description":
                "Python software development"
        },

        {
            "id": "job_2",

            "job_title": "Frontend Developer",

            "description":
                "React frontend development"
        },

        {
            "id": "job_3",

            "job_title": "ML Engineer",

            "description":
                "Machine learning and Python"
        }

    ]

    results = rank_jobs_by_semantic_similarity(
        "Python developer",
        jobs,
        top_k=2
    )

    assert len(results) == 2

    assert results[0]["rank"] == 1

    assert results[1]["rank"] == 2


# ============================================================
# TEST 12 - RANK ORDER
# ============================================================

def test_rank_order():

    jobs = [

        {
            "job_title": "Python Developer",

            "description":
                "Python software developer"
        },

        {
            "job_title": "Unrelated Role",

            "description":
                "Cooking and restaurant management"
        }

    ]

    results = rank_jobs_by_semantic_similarity(
        "Python developer",
        jobs,
        top_k=2
    )

    assert results[0]["job_title"] == (
        "Python Developer"
    )


# ============================================================
# TEST 13 - EMPTY JOB LIST
# ============================================================

def test_empty_job_list():

    assert rank_jobs_by_semantic_similarity(
        "Python",
        [],
        5
    ) == []


# ============================================================
# TEST 14 - EMPTY RESUME
# ============================================================

def test_empty_resume_ranking():

    jobs = [

        {
            "job_title": "Python Developer",

            "description": "Python development"
        }

    ]

    assert rank_jobs_by_semantic_similarity(
        "",
        jobs,
        5
    ) == []


# ============================================================
# TEST 15 - INVALID TOP K
# ============================================================

def test_invalid_top_k():

    jobs = [

        {
            "job_title": "Python Developer",

            "description": "Python development"
        }

    ]

    assert rank_jobs_by_semantic_similarity(
        "Python",
        jobs,
        0
    ) == []


# ============================================================
# TEST 16 - MISSING DESCRIPTION
# ============================================================

def test_missing_description():

    jobs = [

        {
            "job_title": "Python Developer"
        },

        {
            "job_title": "Data Scientist",

            "description":
                "Data science and machine learning"
        }

    ]

    results = rank_jobs_by_semantic_similarity(
        "Python",
        jobs,
        5
    )

    assert len(results) == 1

    assert results[0]["job_title"] == (
        "Data Scientist"
    )