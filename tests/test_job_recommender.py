# ============================================================
# IntelliHire V4 - Job Recommendation Tests
# ============================================================

from src.job_recommender import (
    recommend_jobs,
    recommend_jobs_from_skills,
    calculate_job_match,
    get_best_job,
    get_recommendation_summary
)


# ============================================================
# TEST 1
# ============================================================

def test_calculate_job_match():

    resume_skills = {
        "python",
        "machine learning",
        "docker"
    }

    required_skills = [
        "python",
        "machine learning",
        "docker",
        "aws"
    ]

    result = calculate_job_match(
        resume_skills,
        required_skills
    )

    assert result["score"] == 75.0

    assert "python" in result[
        "matched_skills"
    ]

    assert "aws" in result[
        "missing_skills"
    ]


# ============================================================
# TEST 2
# ============================================================

def test_recommend_jobs():

    skill_analysis = {

        "known_skills": [

            {
                "skill": "python"
            },

            {
                "skill": "machine learning"
            },

            {
                "skill": "pandas"
            },

            {
                "skill": "numpy"
            },

            {
                "skill": "docker"
            }
        ],

        "unknown_candidates": []
    }

    result = recommend_jobs(
        skill_analysis,
        top_n=5
    )

    assert len(result) == 5

    assert "job_title" in result[0]

    assert "match_score" in result[0]

    assert "matched_skills" in result[0]

    assert "missing_skills" in result[0]


# ============================================================
# TEST 3
# ============================================================

def test_ml_engineer_recommendation():

    skill_analysis = {

        "known_skills": [

            {
                "skill": "python"
            },

            {
                "skill": "machine learning"
            },

            {
                "skill": "pandas"
            },

            {
                "skill": "numpy"
            },

            {
                "skill": "scikit-learn"
            }
        ],

        "unknown_candidates": []
    }

    result = recommend_jobs(
        skill_analysis,
        top_n=5
    )

    job_names = [
        item["job_title"]
        for item in result
    ]

    assert (
        "Machine Learning Engineer"
        in job_names
    )


# ============================================================
# TEST 4
# ============================================================

def test_recommend_jobs_from_skills():

    skills = [
        "python",
        "machine learning",
        "pandas",
        "numpy"
    ]

    result = recommend_jobs_from_skills(
        skills,
        top_n=3
    )

    assert len(result) == 3

    assert result[0]["match_score"] >= 0


# ============================================================
# TEST 5
# ============================================================

def test_best_job():

    skill_analysis = {

        "known_skills": [

            {
                "skill": "python"
            },

            {
                "skill": "machine learning"
            },

            {
                "skill": "numpy"
            },

            {
                "skill": "pandas"
            },

            {
                "skill": "scikit-learn"
            },

            {
                "skill": "tensorflow"
            },

            {
                "skill": "pytorch"
            }
        ]
    }

    result = get_best_job(
        skill_analysis
    )

    assert result != {}

    assert "job_title" in result

    assert "match_score" in result


# ============================================================
# TEST 6
# ============================================================

def test_recommendation_summary():

    skill_analysis = {

        "known_skills": [

            {
                "skill": "python"
            },

            {
                "skill": "django"
            },

            {
                "skill": "flask"
            },

            {
                "skill": "sql"
            }
        ]
    }

    result = get_recommendation_summary(
        skill_analysis,
        top_n=5
    )

    assert (
        result["total_recommendations"]
        == 5
    )

    assert (
        result["best_match"]
        is not None
    )

    assert (
        len(result["recommendations"])
        == 5
    )