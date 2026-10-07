# ============================================================
# IntelliHire V4 - Dynamic Job Recommendation Engine
# ============================================================

from typing import Dict, List, Set
from itertools import combinations


# ============================================================
# SKILL NORMALIZATION
# ============================================================

def normalize_skill(skill: str) -> str:

    if not skill:
        return ""

    skill = str(skill).lower().strip()

    aliases = {

        "python3": "python",

        "sklearn": "scikit-learn",

        "scikit learn": "scikit-learn",

        "react.js": "react",

        "reactjs": "react",

        "nodejs": "node.js",

        "node js": "node.js",

        "postgres": "postgresql",

        "postgresql": "postgresql",

        "ml": "machine learning",

        "ai": "artificial intelligence",

        "rest": "rest api",

        "restful api": "rest api",

        "k8s": "kubernetes",

        "js": "javascript",

        "ts": "typescript"
    }

    return aliases.get(
        skill,
        skill
    )


# ============================================================
# SKILL CATEGORY
# ============================================================

SKILL_CATEGORIES = {

    "python": "Programming",

    "java": "Programming",

    "javascript": "Programming",

    "typescript": "Programming",

    "c++": "Programming",

    "html": "Web Development",

    "css": "Web Development",

    "react": "Web Development",

    "node.js": "Backend Development",

    "django": "Backend Development",

    "flask": "Backend Development",

    "fastapi": "Backend Development",

    "rest api": "Backend Development",

    "sql": "Database",

    "postgresql": "Database",

    "mysql": "Database",

    "mongodb": "Database",

    "machine learning": "Artificial Intelligence",

    "artificial intelligence": "Artificial Intelligence",

    "deep learning": "Artificial Intelligence",

    "nlp": "AI / NLP",

    "transformers": "AI / NLP",

    "hugging face": "AI / NLP",

    "tensorflow": "Machine Learning",

    "pytorch": "Machine Learning",

    "scikit-learn": "Machine Learning",

    "pandas": "Data Science",

    "numpy": "Data Science",

    "statistics": "Data Science",

    "docker": "DevOps",

    "kubernetes": "DevOps",

    "jenkins": "DevOps",

    "git": "DevOps",

    "aws": "Cloud",

    "azure": "Cloud",

    "gcp": "Cloud"
}


# ============================================================
# ROLE TEMPLATES
# ============================================================

ROLE_TEMPLATES = {

    "python": "Python Developer",

    "machine learning": "Machine Learning Engineer",

    "artificial intelligence": "AI Engineer",

    "deep learning": "Deep Learning Engineer",

    "nlp": "NLP Engineer",

    "pandas": "Data Scientist",

    "numpy": "Data Scientist",

    "sql": "Data Analyst",

    "fastapi": "Backend Developer",

    "django": "Backend Developer",

    "flask": "Backend Developer",

    "react": "Frontend Developer",

    "javascript": "Frontend Developer",

    "typescript": "Frontend Developer",

    "node.js": "Node.js Developer",

    "docker": "DevOps Engineer",

    "kubernetes": "DevOps Engineer",

    "aws": "Cloud Engineer",

    "azure": "Cloud Engineer",

    "gcp": "Cloud Engineer",

    "tensorflow": "Machine Learning Engineer",

    "pytorch": "Machine Learning Engineer",

    "transformers": "NLP Engineer"
}
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
    # Compatibility with skills key
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
# GENERATE DYNAMIC JOB TITLE
# ============================================================

def generate_job_title(
    skills: List[str]
) -> str:

    normalized_skills = [
        normalize_skill(skill)
        for skill in skills
        if skill
    ]

    # --------------------------------------------------------
    # Strong AI combinations
    # --------------------------------------------------------

    if (
        "machine learning" in normalized_skills
        and "python" in normalized_skills
    ):

        if "nlp" in normalized_skills:

            return "Python NLP Machine Learning Engineer"

        if "deep learning" in normalized_skills:

            return "Deep Learning Engineer"

        return "Machine Learning Engineer"

    # --------------------------------------------------------
    # Full Stack
    # --------------------------------------------------------

    if (
        "react" in normalized_skills
        and "node.js" in normalized_skills
    ):

        return "Full Stack Developer"

    # --------------------------------------------------------
    # AI
    # --------------------------------------------------------

    if (
        "artificial intelligence"
        in normalized_skills
        and "python"
        in normalized_skills
    ):

        return "AI Software Engineer"

    # --------------------------------------------------------
    # Data
    # --------------------------------------------------------

    if (
        "pandas" in normalized_skills
        and "sql" in normalized_skills
    ):

        return "Data Science Engineer"

    # --------------------------------------------------------
    # Cloud + DevOps
    # --------------------------------------------------------

    if (
        "docker" in normalized_skills
        and "kubernetes" in normalized_skills
    ):

        return "Cloud DevOps Engineer"

    # --------------------------------------------------------
    # Backend
    # --------------------------------------------------------

    if (
        "fastapi" in normalized_skills
        and "sql" in normalized_skills
    ):

        return "Python Backend Engineer"

    # --------------------------------------------------------
    # Template fallback
    # --------------------------------------------------------

    for skill in normalized_skills:

        if skill in ROLE_TEMPLATES:

            return ROLE_TEMPLATES[
                skill
            ]

    # --------------------------------------------------------
    # Generic fallback
    # --------------------------------------------------------

    if normalized_skills:

        return (
            normalized_skills[0].title()
            + " Technology Engineer"
        )

    return "Technology Engineer"

# ============================================================
# CALCULATE DYNAMIC JOB MATCH
# ============================================================

def calculate_job_match(
    resume_skills: Set[str],
    required_skills: List[str]
) -> Dict:

    required = {

        normalize_skill(skill)

        for skill in required_skills

        if skill
    }

    resume = {

        normalize_skill(skill)

        for skill in resume_skills

        if skill
    }

    required.discard("")
    resume.discard("")

    if not required:

        return {

            "score": 0.0,

            "matched_skills": [],

            "missing_skills": []
        }

    matched = sorted(
        resume.intersection(
            required
        )
    )

    missing = sorted(
        required.difference(
            resume
        )
    )

    score = (
        len(matched)
        /
        len(required)
    ) * 100

    return {

        "score": round(
            score,
            2
        ),

        "matched_skills":
            matched,

        "missing_skills":
            missing
    }


# ============================================================
# GENERATE REQUIRED SKILLS
# ============================================================

def generate_required_skills(
    resume_skills: List[str],
    combination_size: int
) -> List[str]:

    skills = [

        normalize_skill(skill)

        for skill in resume_skills

        if skill
    ]

    skills = list(
        dict.fromkeys(
            skills
        )
    )

    if not skills:
        return []

    # --------------------------------------------------------
    # Select combination
    # --------------------------------------------------------

    if combination_size >= len(skills):

        return skills

    return skills[
        :combination_size
    ]


# ============================================================
# GENERATE DYNAMIC JOB
# ============================================================

def generate_dynamic_job(
    resume_skills: List[str],
    job_number: int
) -> Dict:

    if not resume_skills:

        return {}

    total_skills = len(
        resume_skills
    )

    # Different combinations create
    # different recommendation profiles.

    combination_size = (
        (job_number - 1)
        % max(
            1,
            min(
                total_skills,
                5
            )
        )
    ) + 1

    selected_skills = (
        generate_required_skills(
            resume_skills,
            combination_size
        )
    )

    # --------------------------------------------------------
    # Rotate skills for diversity
    # --------------------------------------------------------

    if total_skills > 1:

        shift = (
            job_number - 1
        ) % total_skills

        rotated = (
            resume_skills[
                shift:
            ]
            +
            resume_skills[
                :shift
            ]
        )

        selected_skills = (
            rotated[
                :combination_size
            ]
        )

    job_title = generate_job_title(
        selected_skills
    )

    # Make title unique when
    # multiple generated profiles
    # produce the same role.

    if job_number > 1:

        job_title = (
            f"{job_title} "
            f"Specialist {job_number}"
        )

    categories = []

    for skill in selected_skills:

        category = SKILL_CATEGORIES.get(
            skill,
            "Technology"
        )

        if category not in categories:

            categories.append(
                category
            )

    category = (
        " / ".join(categories)
        if categories
        else "Technology"
    )

    return {

        "job_title":
            job_title,

        "category":
            category,

        "required_skills":
            selected_skills,

        "description":
            (
                f"Technology role focused on "
                f"{', '.join(selected_skills)}."
            )
    }

# ============================================================
# RECOMMEND JOBS DYNAMICALLY
# ============================================================

def recommend_jobs(
    skill_analysis: Dict,
    top_n: int = 5
) -> List[Dict]:

    """
    Dynamic V4 recommendation engine.

    The requested number of recommendations
    is generated dynamically from the candidate's
    detected skills.

    No fixed job dataset is required.
    """

    if top_n <= 0:

        return []

    resume_skills = extract_resume_skills(
        skill_analysis
    )

    if not resume_skills:

        return []

    resume_skill_list = sorted(
        resume_skills
    )

    recommendations = []

    # --------------------------------------------------------
    # Generate requested number
    # --------------------------------------------------------

    for job_number in range(
        1,
        top_n + 1
    ):

        job = generate_dynamic_job(
            resume_skill_list,
            job_number
        )

        if not job:
            continue

        result = calculate_job_match(
            resume_skills,
            job["required_skills"]
        )

        recommendations.append({

            "job_title":
                job["job_title"],

            "match_score":
                result["score"],

            "matched_skills":
                result["matched_skills"],

            "missing_skills":
                result["missing_skills"],

            "category":
                job["category"],

            "description":
                job["description"],

            "required_skills":
                job["required_skills"]
        })

    # --------------------------------------------------------
    # Sort by score
    # --------------------------------------------------------

    recommendations.sort(

        key=lambda item:
            item["match_score"],

        reverse=True
    )

    # --------------------------------------------------------
    # Add rank
    # --------------------------------------------------------

    for index, item in enumerate(
        recommendations,
        start=1
    ):

        item["rank"] = index

    return recommendations

# ============================================================
# RECOMMEND FROM RAW SKILLS
# ============================================================

def recommend_jobs_from_skills(
    resume_skills,
    top_n: int = 5
) -> List[Dict]:

    if not resume_skills:

        return []

    skill_analysis = {

        "skills": [

            {
                "skill": skill
            }

            for skill in resume_skills
        ]
    }

    return recommend_jobs(
        skill_analysis,
        top_n
    )


# ============================================================
# BEST JOB
# ============================================================

def get_best_job(
    skill_analysis: Dict
) -> Dict:

    recommendations = recommend_jobs(
        skill_analysis,
        top_n=1
    )

    if not recommendations:

        return {}

    return recommendations[0]


# ============================================================
# RECOMMENDATION SUMMARY
# ============================================================

def get_recommendation_summary(
    skill_analysis: Dict,
    top_n: int = 5
) -> Dict:

    recommendations = recommend_jobs(
        skill_analysis,
        top_n
    )

    if not recommendations:

        return {

            "total_recommendations":
                0,

            "best_match":
                None,

            "best_match_score":
                0.0,

            "recommendations":
                []
        }

    return {

        "total_recommendations":
            len(recommendations),

        "best_match":
            recommendations[0][
                "job_title"
            ],

        "best_match_score":
            recommendations[0][
                "match_score"
            ],

        "recommendations":
            recommendations
    }







