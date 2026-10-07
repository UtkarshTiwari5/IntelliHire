# ============================================================
# IntelliHire V6 - Unified Pipeline Tests
# ============================================================

from src.v6_pipeline import (
    run_v6_match_pipeline
)


# ============================================================
# TEST 1 - COMPLETE PIPELINE
# ============================================================

def test_v6_pipeline():

    result = run_v6_match_pipeline(
        "Python developer with machine learning experience",
        "Python machine learning engineer",
        80
    )

    assert "keyword_score" in result

    assert "semantic_score" in result

    assert "hybrid_score" in result

    assert 0 <= result[
        "semantic_score"
    ] <= 100

    assert 0 <= result[
        "hybrid_score"
    ] <= 100


# ============================================================
# TEST 2 - EMPTY RESUME
# ============================================================

def test_empty_resume():

    result = run_v6_match_pipeline(
        "",
        "Python developer",
        70
    )

    assert result[
        "semantic_score"
    ] == 0.0

    assert result[
        "hybrid_score"
    ] == 70.0


# ============================================================
# TEST 3 - EMPTY JOB
# ============================================================

def test_empty_job():

    result = run_v6_match_pipeline(
        "Python developer",
        "",
        60
    )

    assert result[
        "semantic_score"
    ] == 0.0

    assert result[
        "hybrid_score"
    ] == 60.0


# ============================================================
# TEST 4 - NO KEYWORD SCORE
# ============================================================

def test_no_keyword_score():

    result = run_v6_match_pipeline(
        "Python developer",
        "Python software developer"
    )

    assert result[
        "keyword_score"
    ] == 0.0

    assert 0 <= result[
        "semantic_score"
    ] <= 100