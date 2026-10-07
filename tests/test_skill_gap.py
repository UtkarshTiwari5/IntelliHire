# ============================================================
# IntelliHire V5 - Skill Gap + Career Roadmap Tests
# ============================================================

from src.skill_gap import (
    normalize_skill,
    extract_resume_skills,
    extract_required_skills,
    calculate_skill_gap,
    get_skill_priority,
    build_skill_gap_details,
    build_learning_roadmap,
    generate_career_roadmap,
    generate_roadmap_from_job
)


# ============================================================
# TEST 1 - SKILL NORMALIZATION
# ============================================================

def test_normalize_skill():

    assert normalize_skill("Python3") == "python"
    assert normalize_skill("ML") == "machine learning"
    assert normalize_skill("sklearn") == "scikit-learn"
    assert normalize_skill("postgres") == "postgresql"
    assert normalize_skill("nodejs") == "node.js"
    assert normalize_skill("REST") == "rest api"
    assert normalize_skill("K8s") == "kubernetes"


# ============================================================
# TEST 2 - EMPTY SKILL
# ============================================================

def test_normalize_empty_skill():

    assert normalize_skill("") == ""
    assert normalize_skill(None) == ""


# ============================================================
# TEST 3 - EXTRACT RESUME SKILLS
# ============================================================

def test_extract_resume_skills():

    skill_analysis = {
        "known_skills": [
            {"skill": "Python"},
            {"skill": "Machine Learning"},
            {"skill": "Docker"}
        ]
    }

    skills = extract_resume_skills(
        skill_analysis
    )

    assert "python" in skills
    assert "machine learning" in skills
    assert "docker" in skills


# ============================================================
# TEST 4 - EXTRACT UNKNOWN CANDIDATES
# ============================================================

def test_extract_unknown_candidates():

    skill_analysis = {
        "unknown_candidates": [
            {"skill": "FastAPI"},
            {"skill": "Kubernetes"}
        ]
    }

    skills = extract_resume_skills(
        skill_analysis
    )

    assert "fastapi" in skills
    assert "kubernetes" in skills


# ============================================================
# TEST 5 - COMPATIBILITY WITH SKILLS KEY
# ============================================================

def test_extract_skills_compatibility():

    skill_analysis = {
        "skills": [
            {"skill": "Python"},
            {"skill": "SQL"}
        ]
    }

    skills = extract_resume_skills(
        skill_analysis
    )

    assert "python" in skills
    assert "sql" in skills


# ============================================================
# TEST 6 - EMPTY RESUME ANALYSIS
# ============================================================

def test_empty_resume_analysis():

    skills = extract_resume_skills(
        {}
    )

    assert skills == set()


# ============================================================
# TEST 7 - EXTRACT REQUIRED JOB SKILLS
# ============================================================

def test_extract_required_skills():

    required = extract_required_skills(
        [
            "Python",
            "ML",
            "Docker",
            "Postgres"
        ]
    )

    assert "python" in required
    assert "machine learning" in required
    assert "docker" in required
    assert "postgresql" in required


# ============================================================
# TEST 8 - EMPTY REQUIRED SKILLS
# ============================================================

def test_empty_required_skills():

    required = extract_required_skills(
        []
    )

    assert required == set()


# ============================================================
# TEST 9 - CALCULATE SKILL GAP
# ============================================================

def test_calculate_skill_gap():

    resume_skills = {
        "python",
        "machine learning",
        "docker"
    }

    required_skills = {
        "python",
        "machine learning",
        "docker",
        "aws",
        "kubernetes"
    }

    result = calculate_skill_gap(
        resume_skills,
        required_skills
    )

    assert result["matched_skills"] == [
        "docker",
        "machine learning",
        "python"
    ]

    assert result["missing_skills"] == [
        "aws",
        "kubernetes"
    ]

    assert result["readiness_score"] == 60.0


# ============================================================
# TEST 10 - COMPLETE SKILL MATCH
# ============================================================

def test_complete_skill_match():

    resume_skills = {
        "python",
        "sql",
        "docker"
    }

    required_skills = {
        "python",
        "sql",
        "docker"
    }

    result = calculate_skill_gap(
        resume_skills,
        required_skills
    )

    assert result["missing_skills"] == []

    assert result["readiness_score"] == 100.0


# ============================================================
# TEST 11 - NO SKILL MATCH
# ============================================================

def test_no_skill_match():

    resume_skills = {
        "html",
        "css"
    }

    required_skills = {
        "python",
        "sql",
        "docker"
    }

    result = calculate_skill_gap(
        resume_skills,
        required_skills
    )

    assert result["matched_skills"] == []

    assert result["missing_skills"] == [
        "docker",
        "python",
        "sql"
    ]

    assert result["readiness_score"] == 0.0


# ============================================================
# TEST 12 - EMPTY REQUIRED SKILLS
# ============================================================

def test_empty_required_skill_gap():

    result = calculate_skill_gap(
        {"python"},
        set()
    )

    assert result["matched_skills"] == []

    assert result["missing_skills"] == []

    assert result["readiness_score"] == 0.0


# ============================================================
# TEST 13 - HIGH PRIORITY
# ============================================================

def test_high_priority_skill():

    assert get_skill_priority(
        "AWS"
    ) == "High"

    assert get_skill_priority(
        "Machine Learning"
    ) == "High"

    assert get_skill_priority(
        "Python"
    ) == "High"


# ============================================================
# TEST 14 - MEDIUM PRIORITY
# ============================================================

def test_medium_priority_skill():

    assert get_skill_priority(
        "Pandas"
    ) == "Medium"

    assert get_skill_priority(
        "NumPy"
    ) == "Medium"

    assert get_skill_priority(
        "Git"
    ) == "Medium"


# ============================================================
# TEST 15 - LOW PRIORITY
# ============================================================

def test_low_priority_skill():

    assert get_skill_priority(
        "SomeNewTechnology"
    ) == "Low"


# ============================================================
# TEST 16 - BUILD SKILL GAP DETAILS
# ============================================================

def test_build_skill_gap_details():

    missing_skills = [
        "aws",
        "docker",
        "kubernetes"
    ]

    details = build_skill_gap_details(
        missing_skills
    )

    assert len(details) == 3

    assert details[0]["skill"] == "aws"

    assert details[0]["priority"] == "High"

    assert "topics" in details[0]

    assert "projects" in details[0]


# ============================================================
# TEST 17 - ROADMAP BUILDING
# ============================================================

def test_build_learning_roadmap():

    details = [
        {
            "skill": "aws",
            "priority": "High",
            "sequence": 7,
            "topics": [
                "AWS fundamentals"
            ],
            "projects": [
                "Deploy ML API on AWS"
            ]
        },
        {
            "skill": "docker",
            "priority": "High",
            "sequence": 6,
            "topics": [
                "Docker fundamentals"
            ],
            "projects": [
                "Containerized ML application"
            ]
        }
    ]

    roadmap = build_learning_roadmap(
        details
    )

    assert len(roadmap) == 2

    assert roadmap[0]["phase"] == 1

    assert roadmap[0]["skill"] == "aws"

    assert roadmap[1]["phase"] == 2


# ============================================================
# TEST 18 - COMPLETE CAREER ROADMAP
# ============================================================

def test_generate_career_roadmap():

    skill_analysis = {
        "known_skills": [
            {"skill": "Python"},
            {"skill": "Machine Learning"},
            {"skill": "Docker"}
        ]
    }

    result = generate_career_roadmap(
        skill_analysis,
        "ML Engineer",
        [
            "Python",
            "Machine Learning",
            "Docker",
            "AWS",
            "Kubernetes"
        ]
    )

    assert result["target_job"] == "ML Engineer"

    assert "python" in result["current_skills"]

    assert "aws" in result["missing_skills"]

    assert "kubernetes" in result["missing_skills"]

    assert result["job_readiness_score"] == 60.0

    assert len(
        result["learning_roadmap"]
    ) == 2


# ============================================================
# TEST 19 - ROADMAP FROM V4 JOB
# ============================================================

def test_generate_roadmap_from_job():

    skill_analysis = {
        "known_skills": [
            {"skill": "Python"},
            {"skill": "SQL"}
        ]
    }

    job = {
        "job_title": "Data Scientist",
        "required_skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Statistics"
        ]
    }

    result = generate_roadmap_from_job(
        skill_analysis,
        job
    )

    assert result["target_job"] == (
        "Data Scientist"
    )

    assert "python" in result["matched_skills"]

    assert "sql" in result["matched_skills"]

    assert "machine learning" in (
        result["missing_skills"]
    )

    assert "statistics" in (
        result["missing_skills"]
    )

    assert result["job_readiness_score"] == 50.0


# ============================================================
# TEST 20 - EMPTY V4 JOB
# ============================================================

def test_empty_job():

    skill_analysis = {
        "known_skills": [
            {"skill": "Python"}
        ]
    }

    result = generate_roadmap_from_job(
        skill_analysis,
        {}
    )

    assert result["target_job"] is None

    assert result["current_skills"] == []

    assert result["required_skills"] == []

    assert result["missing_skills"] == []

    assert result["job_readiness_score"] == 0.0


# ============================================================
# TEST 21 - UNKNOWN SKILL ROADMAP
# ============================================================

def test_unknown_skill_roadmap():

    details = build_skill_gap_details(
        ["quantum computing"]
    )

    assert len(details) == 1

    assert details[0]["skill"] == (
        "quantum computing"
    )

    assert details[0]["priority"] == "Low"

    assert len(
        details[0]["topics"]
    ) > 0

    assert len(
        details[0]["projects"]
    ) > 0