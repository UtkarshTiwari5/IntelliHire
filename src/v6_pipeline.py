# ============================================================
# IntelliHire V6 - Unified Semantic Pipeline
# ============================================================

from typing import Dict, Any

from src.semantic_matcher import (
    hybrid_resume_job_match
)


# ============================================================
# V6 MATCH PIPELINE
# ============================================================

def run_v6_match_pipeline(
    resume_text: str,
    job_description: str,
    keyword_score: float = 0.0
) -> Dict[str, Any]:
    """
    Combine V3 keyword matching with V6
    semantic matching.
    """

    if not resume_text:
        return {
            "keyword_score": round(
                float(keyword_score),
                2
            ),
            "semantic_score": 0.0,
            "hybrid_score": round(
                float(keyword_score),
                2
            )
        }

    if not job_description:
        return {
            "keyword_score": round(
                float(keyword_score),
                2
            ),
            "semantic_score": 0.0,
            "hybrid_score": round(
                float(keyword_score),
                2
            )
        }

    result = hybrid_resume_job_match(
        resume_text,
        job_description,
        keyword_score
    )

    return {
        "keyword_score": result[
            "keyword_score"
        ],

        "semantic_score": result[
            "semantic_score"
        ],

        "hybrid_score": result[
            "hybrid_score"
        ]
    }