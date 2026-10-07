# ============================================================
# IntelliHire V6 - Semantic Resume Job Matcher
# ============================================================

from typing import Dict, Any, List

from src.embeddings import (
    semantic_similarity,
    similarity_percentage
)


# ============================================================
# SEMANTIC SCORE
# ============================================================

def calculate_semantic_score(
    resume_text: str,
    job_description: str
) -> float:
    """
    Calculate semantic similarity between
    resume and job description.
    """

    if not resume_text:
        return 0.0

    if not job_description:
        return 0.0

    return similarity_percentage(
        resume_text,
        job_description
    )


# ============================================================
# HYBRID SCORE
# ============================================================

def calculate_hybrid_score(
    keyword_score: float,
    semantic_score: float,
    keyword_weight: float = 0.5,
    semantic_weight: float = 0.5
) -> float:
    """
    Combine keyword and semantic matching scores.
    """

    if keyword_weight < 0:
        keyword_weight = 0.0

    if semantic_weight < 0:
        semantic_weight = 0.0

    total_weight = (
        keyword_weight
        + semantic_weight
    )

    if total_weight == 0:
        return 0.0

    normalized_keyword_weight = (
        keyword_weight
        / total_weight
    )

    normalized_semantic_weight = (
        semantic_weight
        / total_weight
    )

    score = (
        keyword_score
        * normalized_keyword_weight
        +
        semantic_score
        * normalized_semantic_weight
    )

    return round(
        score,
        2
    )


# ============================================================
# SEMANTIC MATCH
# ============================================================

def semantic_match_resume_to_job(
    resume_text: str,
    job_description: str
) -> Dict[str, Any]:
    """
    Perform semantic resume-job matching.
    """

    semantic_score = calculate_semantic_score(
        resume_text,
        job_description
    )

    return {
        "semantic_score": semantic_score,

        "resume_text_available": bool(
            resume_text
        ),

        "job_description_available": bool(
            job_description
        )
    }


# ============================================================
# HYBRID RESUME JOB MATCH
# ============================================================

def hybrid_resume_job_match(
    resume_text: str,
    job_description: str,
    keyword_score: float
) -> Dict[str, Any]:
    """
    Combine V3 keyword matching with
    V6 semantic matching.
    """

    semantic_score = calculate_semantic_score(
        resume_text,
        job_description
    )

    hybrid_score = calculate_hybrid_score(
        keyword_score,
        semantic_score
    )

    return {
        "keyword_score": round(
            float(keyword_score),
            2
        ),

        "semantic_score": semantic_score,

        "hybrid_score": hybrid_score
    }


# ============================================================
# BATCH SEMANTIC JOB MATCHING
# ============================================================

def rank_jobs_by_semantic_similarity(
    resume_text: str,
    jobs: List[Dict[str, Any]],
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Rank multiple jobs according to semantic similarity.
    """

    if not resume_text:
        return []

    if not jobs:
        return []

    if top_k <= 0:
        return []

    results = []

    for index, job in enumerate(jobs):

        job_description = job.get(
            "description",
            ""
        )

        if not job_description:
            continue

        score = calculate_semantic_score(
            resume_text,
            job_description
        )

        results.append(
            {
                "rank": 0,

                "id": job.get(
                    "id",
                    index
                ),

                "job_title": job.get(
                    "job_title",
                    "Unknown Job"
                ),

                "description": job_description,

                "semantic_score": score
            }
        )

    results.sort(
        key=lambda item: item[
            "semantic_score"
        ],
        reverse=True
    )

    results = results[:top_k]

    for rank, result in enumerate(
        results,
        start=1
    ):

        result["rank"] = rank

    return results

