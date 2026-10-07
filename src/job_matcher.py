# ============================================================
# IntelliHire V3 - Job Matching Engine
# ============================================================

import re
from typing import Dict, List, Set


# ============================================================
# SKILL / TECHNOLOGY NORMALIZATION
# ============================================================

SKILL_ALIASES = {

    "python": [
        "python",
        "python3"
    ],

    "java": [
        "java"
    ],

    "javascript": [
        "javascript",
        "js"
    ],

    "typescript": [
        "typescript",
        "ts"
    ],

    "c++": [
        "c++",
        "cpp"
    ],

    "c": [
        "c language"
    ],

    "sql": [
        "sql"
    ],

    "mysql": [
        "mysql"
    ],

    "postgresql": [
        "postgresql",
        "postgres"
    ],

    "machine learning": [
        "machine learning",
        "ml",
        "machine-learning"
    ],

    "deep learning": [
        "deep learning",
        "dl"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "ai"
    ],

    "nlp": [
        "nlp",
        "natural language processing"
    ],

    "computer vision": [
        "computer vision",
        "opencv"
    ],

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy"
    ],

    "scikit-learn": [
        "scikit-learn",
        "sklearn",
        "scikit learn"
    ],

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch"
    ],

    "django": [
        "django"
    ],

    "flask": [
        "flask"
    ],

    "fastapi": [
        "fastapi"
    ],

    "react": [
        "react",
        "reactjs",
        "react.js"
    ],

    "node.js": [
        "node.js",
        "nodejs",
        "node js"
    ],

    "html": [
        "html",
        "html5"
    ],

    "css": [
        "css",
        "css3"
    ],

    "git": [
        "git"
    ],

    "github": [
        "github"
    ],

    "docker": [
        "docker"
    ],

    "kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure"
    ],

    "gcp": [
        "gcp",
        "google cloud",
        "google cloud platform"
    ],

    "rest api": [
        "rest api",
        "restful api",
        "rest"
    ],

    "streamlit": [
        "streamlit"
    ],

    "statistics": [
        "statistics",
        "statistical analysis"
    ],

    "data science": [
        "data science"
    ],

    "power bi": [
        "power bi"
    ],

    "tableau": [
        "tableau"
    ]
}


# ============================================================
# ROLE KEYWORDS
# ============================================================

ROLE_KEYWORDS = {

    "python developer": [
        "python",
        "django",
        "flask",
        "fastapi",
        "sql",
        "rest api"
    ],

    "backend developer": [
        "python",
        "java",
        "node.js",
        "sql",
        "rest api"
    ],

    "machine learning engineer": [
        "python",
        "machine learning",
        "numpy",
        "pandas",
        "scikit-learn",
        "tensorflow",
        "pytorch"
    ],

    "ml engineer": [
        "python",
        "machine learning",
        "numpy",
        "pandas",
        "scikit-learn",
        "tensorflow",
        "pytorch"
    ],

    "data scientist": [
        "python",
        "machine learning",
        "pandas",
        "numpy",
        "sql",
        "statistics",
        "scikit-learn"
    ],

    "ai engineer": [
        "python",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "nlp"
    ],

    "frontend developer": [
        "html",
        "css",
        "javascript",
        "react",
        "typescript"
    ],

    "full stack developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "sql"
    ]
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:

    if not text:
        return ""

    text = str(text).lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# EXTRACT SKILLS FROM TEXT
# ============================================================

def extract_skills_from_text(
    text: str
) -> Set[str]:

    text = normalize_text(text)

    detected_skills = set()

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            pattern = (
                r"(?<![a-zA-Z0-9])"
                + re.escape(alias.lower())
                + r"(?![a-zA-Z0-9])"
            )

            if re.search(
                pattern,
                text
            ):

                detected_skills.add(
                    canonical_skill
                )

                break

    return detected_skills


# ============================================================
# GET SKILLS FROM V2 RESULT
# ============================================================

def get_resume_skills(
    skill_analysis: Dict
) -> Set[str]:

    skills = set()

    if not skill_analysis:
        return skills

    # --------------------------------------------------------
    # Current V2 format
    # --------------------------------------------------------

    for item in skill_analysis.get(
        "known_skills",
        []
    ):

        if isinstance(item, dict):

            skill = item.get(
                "skill",
                ""
            )

        else:

            skill = str(item)

        if skill:
            skills.add(
                normalize_text(skill)
            )

    # --------------------------------------------------------
    # Test / older V2 format
    # --------------------------------------------------------

    for item in skill_analysis.get(
        "skills",
        []
    ):

        if isinstance(item, dict):

            skill = item.get(
                "skill",
                ""
            )

        else:

            skill = str(item)

        if skill:
            skills.add(
                normalize_text(skill)
            )

    # --------------------------------------------------------
    # Unknown candidates
    # --------------------------------------------------------

    for item in skill_analysis.get(
        "unknown_candidates",
        []
    ):

        if isinstance(item, dict):

            skill = item.get(
                "skill",
                ""
            )

        else:

            skill = str(item)

        if skill:
            skills.add(
                normalize_text(skill)
            )

    return skills


# ============================================================
# CANONICALIZE SKILL
# ============================================================

def canonicalize_skill(
    skill: str
) -> str:

    skill = normalize_text(skill)

    for canonical, aliases in SKILL_ALIASES.items():

        if skill == normalize_text(canonical):

            return canonical

        for alias in aliases:

            if skill == normalize_text(alias):

                return canonical

    return skill


# ============================================================
# DETECT ROLE REQUIREMENTS
# ============================================================

def detect_role_requirements(
    job_description: str
) -> Set[str]:

    text = normalize_text(
        job_description
    )

    required = set()

    for role, skills in ROLE_KEYWORDS.items():

        if role in text:

            required.update(
                skills
            )

    return required


# ============================================================
# EXTRACT JOB REQUIREMENTS
# ============================================================

def extract_job_requirements(
    job_description: str
) -> Set[str]:

    if not job_description:
        return set()

    text = normalize_text(
        job_description
    )

    requirements = set()

    # --------------------------------------------------------
    # Direct skill detection
    # --------------------------------------------------------

    requirements.update(
        extract_skills_from_text(
            text
        )
    )

    # --------------------------------------------------------
    # Role-based requirements
    # --------------------------------------------------------

    requirements.update(
        detect_role_requirements(
            text
        )
    )

    # --------------------------------------------------------
    # Generic direct signals
    # --------------------------------------------------------

    direct_signals = {

        "python": "python",
        "java": "java",
        "javascript": "javascript",
        "typescript": "typescript",
        "sql": "sql",
        "mysql": "mysql",
        "postgresql": "postgresql",
        "machine learning": "machine learning",
        "deep learning": "deep learning",
        "artificial intelligence": "artificial intelligence",
        "nlp": "nlp",
        "docker": "docker",
        "aws": "aws",
        "azure": "azure",
        "react": "react",
        "pandas": "pandas",
        "numpy": "numpy",
        "tensorflow": "tensorflow",
        "pytorch": "pytorch",
        "fastapi": "fastapi",
        "django": "django",
        "flask": "flask"
    }

    for signal, canonical in direct_signals.items():

        if re.search(
            r"(?<![a-zA-Z0-9])"
            + re.escape(signal)
            + r"(?![a-zA-Z0-9])",
            text
        ):

            requirements.add(
                canonical
            )

    # --------------------------------------------------------
    # Canonicalize
    # --------------------------------------------------------

    requirements = {
        canonicalize_skill(skill)
        for skill in requirements
        if skill
    }

    return requirements


# ============================================================
# MATCH SKILLS
# ============================================================

def match_skills(
    resume_skills: List[str],
    job_skills: List[str]
) -> Dict:

    resume_set = {
        canonicalize_skill(skill)
        for skill in resume_skills
        if skill
    }

    job_set = {
        canonicalize_skill(skill)
        for skill in job_skills
        if skill
    }

    matched_skills = sorted(
        resume_set.intersection(
            job_set
        )
    )

    missing_skills = sorted(
        job_set.difference(
            resume_set
        )
    )

    additional_skills = sorted(
        resume_set.difference(
            job_set
        )
    )

    if job_set:

        skill_coverage = round(
            (
                len(matched_skills)
                /
                len(job_set)
            ) * 100,
            2
        )

    else:

        skill_coverage = 0.0

    return {

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "additional_skills":
            additional_skills,

        "skill_coverage":
            skill_coverage
    }


# ============================================================
# CALCULATE MATCH SCORE
# ============================================================

def calculate_match_score(
    skill_coverage: float,
    experience_score: float
) -> float:

    skill_coverage = float(
        skill_coverage
    )

    experience_score = float(
        experience_score
    )

    score = (
        (skill_coverage * 0.75)
        +
        (experience_score * 0.25)
    )

    return round(
        score,
        2
    )


# ============================================================
# EXPERIENCE SCORE
# ============================================================

def calculate_experience_score(
    job_description: str
) -> float:

    text = normalize_text(
        job_description
    )

    experience_keywords = [

        "experience",
        "years",
        "developer",
        "engineer",
        "intern",
        "senior",
        "junior",
        "lead"
    ]

    matches = sum(
        1
        for keyword in experience_keywords
        if keyword in text
    )

    return min(
        100.0,
        matches * 15.0
    )


# ============================================================
# ROLE SIGNAL
# ============================================================

def calculate_role_signal(
    job_description: str
) -> float:

    text = normalize_text(
        job_description
    )

    for role in ROLE_KEYWORDS:

        if role in text:

            return 100.0

    generic_roles = [

        "developer",
        "engineer",
        "scientist",
        "analyst",
        "programmer",
        "software"
    ]

    if any(
        role in text
        for role in generic_roles
    ):

        return 60.0

    return 0.0


# ============================================================
# MAIN RESUME ↔ JOB MATCHING
# ============================================================

def match_resume_to_job(
    resume_text: str,
    skill_analysis: Dict,
    job_description: str
) -> Dict:

    # ========================================================
    # RESUME SKILLS
    # ========================================================

    resume_skills = get_resume_skills(
        skill_analysis
    )

    # Also scan raw resume text
    raw_resume_skills = extract_skills_from_text(
        resume_text
    )

    resume_skills.update(
        raw_resume_skills
    )

    resume_skills = {

        canonicalize_skill(skill)

        for skill in resume_skills

        if skill
    }

    # ========================================================
    # JOB SKILLS
    # ========================================================

    job_skills = extract_job_requirements(
        job_description
    )

    # ========================================================
    # MATCH
    # ========================================================

    skill_result = match_skills(
        list(resume_skills),
        list(job_skills)
    )

    matched_skills = skill_result[
        "matched_skills"
    ]

    missing_skills = skill_result[
        "missing_skills"
    ]

    additional_skills = skill_result[
        "additional_skills"
    ]

    skill_coverage = skill_result[
        "skill_coverage"
    ]

    # ========================================================
    # EXPERIENCE
    # ========================================================

    experience_score = calculate_experience_score(
        job_description
    )

    # ========================================================
    # ROLE
    # ========================================================

    role_signal = calculate_role_signal(
        job_description
    )

    # ========================================================
    # OVERALL SCORE
    # ========================================================

    overall_match_score = (

        (skill_coverage * 0.60)

        +

        (experience_score * 0.15)

        +

        (role_signal * 0.25)
    )

    overall_match_score = round(
        min(
            100.0,
            max(
                0.0,
                overall_match_score
            )
        ),
        2
    )

    # ========================================================
    # UNKNOWN SKILL EVIDENCE
    # ========================================================

    unknown_evidence = []

    for item in skill_analysis.get(
        "unknown_candidates",
        []
    ):

        if isinstance(item, dict):

            skill = item.get(
                "skill",
                ""
            )

        else:

            skill = str(item)

        if not skill:
            continue

        normalized_skill = normalize_text(
            skill
        )

        present_in_job = (
            normalized_skill
            in normalize_text(
                job_description
            )
        )

        unknown_evidence.append({

            "skill": skill,

            "present_in_job":
                present_in_job
        })

    # ========================================================
    # RESULT
    # ========================================================

    return {

        "overall_match_score":
            overall_match_score,

        "skill_coverage":
            skill_coverage,

        "experience_score":
            round(
                experience_score,
                2
            ),

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "additional_skills":
            additional_skills,

        "unknown_skill_evidence":
            unknown_evidence,

        "resume_skills":
            sorted(resume_skills),

        "job_skills":
            sorted(job_skills),

        "role_signal":
            role_signal,

        "analysis_type":
            "Rule-based V3 Job Matching"
    }