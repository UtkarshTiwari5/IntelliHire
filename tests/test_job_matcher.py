
from src.job_matcher import (
    extract_job_requirements,
    match_skills,
    calculate_match_score,
    match_resume_to_job
)


def test_extract_job_requirements():

    job = """
    We need a Python developer with
    Machine Learning, Docker and PostgreSQL.
    """

    result = extract_job_requirements(job)

    assert "python" in result
    assert "machine learning" in result
    assert "docker" in result
    assert "postgresql" in result


def test_skill_matching():

    resume_skills = [
        "python",
        "machine learning",
        "docker"
    ]

    job_skills = [
        "python",
        "machine learning",
        "docker",
        "aws"
    ]

    result = match_skills(
        resume_skills,
        job_skills
    )

    assert "python" in result[
        "matched_skills"
    ]

    assert "aws" in result[
        "missing_skills"
    ]

    assert result[
        "skill_coverage"
    ] == 75.0


def test_match_score():

    score = calculate_match_score(
        80,
        80
    )

    assert score == 80.0


def test_complete_job_matching():

    resume_text = """
    Python developer with Machine Learning
    experience. Built projects using Docker.
    """

    skill_analysis = {
        "skills": [
            {
                "skill": "python",
                "known_skill": True,
                "confidence": 0.95
            },
            {
                "skill": "machine learning",
                "known_skill": True,
                "confidence": 0.95
            },
            {
                "skill": "docker",
                "known_skill": True,
                "confidence": 0.95
            }
        ],
        "unknown_candidates": []
    }

    job = """
    Python Machine Learning Docker AWS developer
    """

    result = match_resume_to_job(
        resume_text,
        skill_analysis,
        job
    )

    assert (
        result["overall_match_score"] > 0
    )

    assert "aws" in result[
        "missing_skills"
    ]