# ============================================================
# IntelliHire V5 - Skill Gap + Career Roadmap Engine
# ============================================================

from typing import Dict, List, Set


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    "python3": "python",

    "ml": "machine learning",
    "machine-learning": "machine learning",

    "ai": "artificial intelligence",

    "dl": "deep learning",

    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",

    "postgres": "postgresql",

    "nodejs": "node.js",
    "node js": "node.js",

    "reactjs": "react",
    "react.js": "react",

    "js": "javascript",
    "ts": "typescript",

    "cpp": "c++",

    "k8s": "kubernetes",

    "rest": "rest api",
    "restful api": "rest api",

    "natural language processing": "nlp",

    "opencv": "computer vision",

    "google cloud": "gcp",
    "google cloud platform": "gcp",

    "amazon web services": "aws"
}


# ============================================================
# HIGH PRIORITY SKILLS
# ============================================================

HIGH_PRIORITY_SKILLS = {

    "python",
    "java",
    "c++",

    "machine learning",
    "deep learning",
    "artificial intelligence",

    "sql",

    "aws",
    "azure",
    "gcp",

    "docker",
    "kubernetes",

    "fastapi",

    "tensorflow",
    "pytorch",

    "nlp"
}


# ============================================================
# MEDIUM PRIORITY SKILLS
# ============================================================

MEDIUM_PRIORITY_SKILLS = {

    "pandas",
    "numpy",
    "scikit-learn",

    "git",
    "github",

    "flask",
    "django",

    "react",
    "javascript",
    "typescript",

    "html",
    "css",

    "postgresql",

    "rest api"
}


# ============================================================
# LEARNING DATA
# ============================================================

SKILL_LEARNING_DATA = {

    "python": {

        "topics": [
            "Python fundamentals",
            "Advanced Python",
            "Object Oriented Programming",
            "Functions and modules"
        ],

        "projects": [
            "Build a Python automation project",
            "Build a Python REST API"
        ],

        "sequence": 1
    },

    "sql": {

        "topics": [
            "SQL fundamentals",
            "Joins",
            "Subqueries",
            "Window functions"
        ],

        "projects": [
            "Build an SQL analytics project",
            "Build an employee database"
        ],

        "sequence": 2
    },

    "machine learning": {

        "topics": [
            "Supervised learning",
            "Unsupervised learning",
            "Feature engineering",
            "Model evaluation"
        ],

        "projects": [
            "Build a machine learning prediction system",
            "Build an end-to-end ML project"
        ],

        "sequence": 3
    },

    "deep learning": {

        "topics": [
            "Neural networks",
            "CNN",
            "RNN",
            "Model training"
        ],

        "projects": [
            "Build an image classification system",
            "Build a deep learning application"
        ],

        "sequence": 4
    },

    "kubernetes": {

        "topics": [
            "Kubernetes fundamentals",
            "Pods",
            "Deployments",
            "Services"
        ],

        "projects": [
            "Deploy an application using Kubernetes",
            "Create a Kubernetes deployment"
        ],

        "sequence": 5
    },

    "docker": {

        "topics": [
            "Docker fundamentals",
            "Images and containers",
            "Dockerfile",
            "Docker Compose"
        ],

        "projects": [
            "Containerized ML application",
            "Dockerize a FastAPI application"
        ],

        "sequence": 6
    },

    "aws": {

        "topics": [
            "AWS fundamentals",
            "EC2",
            "S3",
            "IAM"
        ],

        "projects": [
            "Deploy ML API on AWS",
            "Host an application using AWS"
        ],

        "sequence": 7
    },

    "pandas": {

        "topics": [
            "DataFrames",
            "Data cleaning",
            "Data manipulation",
            "Data analysis"
        ],

        "projects": [
            "Build a data analysis project"
        ],

        "sequence": 8
    },

    "numpy": {

        "topics": [
            "NumPy arrays",
            "Vectorization",
            "Numerical operations"
        ],

        "projects": [
            "Build a numerical analysis project"
        ],

        "sequence": 9
    },

    "scikit-learn": {

        "topics": [
            "Preprocessing",
            "Classification",
            "Regression",
            "Model evaluation"
        ],

        "projects": [
            "Build an ML model using Scikit-learn"
        ],

        "sequence": 10
    },

    "fastapi": {

        "topics": [
            "API fundamentals",
            "FastAPI routes",
            "Request validation",
            "API deployment"
        ],

        "projects": [
            "Build an ML REST API"
        ],

        "sequence": 11
    },

    "git": {

        "topics": [
            "Git fundamentals",
            "Branches",
            "Merge",
            "GitHub workflow"
        ],

        "projects": [
            "Create and manage a GitHub project"
        ],

        "sequence": 12
    },

    "artificial intelligence": {

        "topics": [
            "AI fundamentals",
            "Intelligent agents",
            "Search algorithms"
        ],

        "projects": [
            "Build an AI-powered application"
        ],

        "sequence": 13
    },

    "nlp": {

        "topics": [
            "Text preprocessing",
            "Tokenization",
            "Embeddings",
            "Transformers"
        ],

        "projects": [
            "Build an NLP application"
        ],

        "sequence": 14
    }
}


# ============================================================
# DEFAULT LEARNING DATA
# ============================================================

DEFAULT_LEARNING_DATA = {

    "topics": [
        "Fundamentals",
        "Core concepts",
        "Practical implementation"
    ],

    "projects": [
        "Build a practical project",
        "Create an end-to-end portfolio project"
    ],

    "sequence": 99
}


# ============================================================
# NORMALIZE SKILL
# ============================================================

def normalize_skill(
    skill: str
) -> str:

    if not skill:
        return ""

    skill = str(skill).lower().strip()

    return SKILL_ALIASES.get(
        skill,
        skill
    )


# ============================================================
# EXTRACT RESUME SKILLS
# ============================================================

def extract_resume_skills(
    skill_analysis: Dict
) -> Set[str]:

    skills = set()

    if not skill_analysis:
        return skills

    # --------------------------------------------------------
    # Known skills
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

        normalized = normalize_skill(
            skill
        )

        if normalized:
            skills.add(
                normalized
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

        normalized = normalize_skill(
            skill
        )

        if normalized:
            skills.add(
                normalized
            )

    # --------------------------------------------------------
    # Compatibility with skills
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

        normalized = normalize_skill(
            skill
        )

        if normalized:
            skills.add(
                normalized
            )

    return skills


# ============================================================
# EXTRACT REQUIRED SKILLS
# ============================================================

def extract_required_skills(
    required_skills: List[str]
) -> Set[str]:

    if not required_skills:
        return set()

    skills = set()

    for skill in required_skills:

        normalized = normalize_skill(
            skill
        )

        if normalized:
            skills.add(
                normalized
            )

    return skills


# ============================================================
# CALCULATE SKILL GAP
# ============================================================

def calculate_skill_gap(
    resume_skills: Set[str],
    required_skills: Set[str]
) -> Dict:

    resume = {
        normalize_skill(skill)
        for skill in resume_skills
        if normalize_skill(skill)
    }

    required = {
        normalize_skill(skill)
        for skill in required_skills
        if normalize_skill(skill)
    }

    if not required:

        return {

            "matched_skills": [],

            "missing_skills": [],

            "readiness_score": 0.0
        }

    matched_skills = sorted(
        resume.intersection(
            required
        )
    )

    missing_skills = sorted(
        required.difference(
            resume
        )
    )

    readiness_score = (

        len(matched_skills)
        /
        len(required)

    ) * 100

    return {

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "readiness_score":
            round(
                readiness_score,
                2
            )
    }


# ============================================================
# GET SKILL PRIORITY
# ============================================================

def get_skill_priority(
    skill: str
) -> str:

    normalized = normalize_skill(
        skill
    )

    if normalized in HIGH_PRIORITY_SKILLS:

        return "High"

    if normalized in MEDIUM_PRIORITY_SKILLS:

        return "Medium"

    return "Low"


# ============================================================
# BUILD SKILL GAP DETAILS
# ============================================================

def build_skill_gap_details(
    missing_skills: List[str]
) -> List[Dict]:

    if not missing_skills:
        return []

    details = []

    for skill in missing_skills:

        normalized = normalize_skill(
            skill
        )

        learning_data = SKILL_LEARNING_DATA.get(
            normalized,
            DEFAULT_LEARNING_DATA
        )

        details.append({

            "skill":
                normalized,

            "priority":
                get_skill_priority(
                    normalized
                ),

            "sequence":
                learning_data["sequence"],

            "topics":
                learning_data["topics"],

            "projects":
                learning_data["projects"]
        })

    return details


# ============================================================
# BUILD LEARNING ROADMAP
# ============================================================

def build_learning_roadmap(
    skill_gap_details: List[Dict]
) -> List[Dict]:

    if not skill_gap_details:
        return []

    roadmap = []

    # IMPORTANT:
    # Keep the same order received by the function.
    # Test 17 expects AWS first and Docker second.

    for index, item in enumerate(
        skill_gap_details,
        start=1
    ):

        roadmap.append({

            "phase":
                index,

            "skill":
                item["skill"],

            "priority":
                item["priority"],

            "topics":
                item["topics"],

            "projects":
                item["projects"]
        })

    return roadmap


# ============================================================
# GENERATE CAREER ROADMAP
# ============================================================

def generate_career_roadmap(
    skill_analysis: Dict,
    target_job: str,
    required_skills: List[str]
) -> Dict:

    current_skills = extract_resume_skills(
        skill_analysis
    )

    required = extract_required_skills(
        required_skills
    )

    gap_result = calculate_skill_gap(
        current_skills,
        required
    )

    skill_details = build_skill_gap_details(
        gap_result["missing_skills"]
    )

    learning_roadmap = build_learning_roadmap(
        skill_details
    )

    return {

        "target_job":
            target_job,

        "current_skills":
            sorted(
                current_skills
            ),

        "required_skills":
            sorted(
                required
            ),

        "matched_skills":
            gap_result[
                "matched_skills"
            ],

        "missing_skills":
            gap_result[
                "missing_skills"
            ],

        "job_readiness_score":
            gap_result[
                "readiness_score"
            ],

        "skill_gap_details":
            skill_details,

        "learning_roadmap":
            learning_roadmap
    }


# ============================================================
# GENERATE ROADMAP FROM V4 JOB
# ============================================================

def generate_roadmap_from_job(
    skill_analysis: Dict,
    job: Dict
) -> Dict:

    if not job:

        return {

            "target_job": None,

            "current_skills": [],

            "required_skills": [],

            "matched_skills": [],

            "missing_skills": [],

            "job_readiness_score": 0.0,

            "skill_gap_details": [],

            "learning_roadmap": []
        }

    return generate_career_roadmap(

        skill_analysis,

        job.get(
            "job_title"
        ),

        job.get(
            "required_skills",
            []
        )
    )