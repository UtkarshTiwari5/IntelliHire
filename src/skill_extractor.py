# ============================================================
# IntelliHire V2 - Skill Extraction Engine
# ============================================================

import re


# ============================================================
# SKILL CATEGORIES
# ============================================================

SKILL_CATEGORIES = {

    "programming_language": [
        "python",
        "java",
        "c",
        "c++",
        "c#",
        "javascript",
        "typescript",
        "go",
        "golang",
        "rust",
        "kotlin",
        "swift",
        "php",
        "ruby",
        "scala",
        "r"
    ],

    "ai_ml": [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "natural language processing",
        "nlp",
        "computer vision",
        "generative ai",
        "generative artificial intelligence",
        "reinforcement learning",
        "supervised learning",
        "unsupervised learning",
        "llm",
        "large language model",
        "transformer",
        "neural network"
    ],

    "machine_learning_library": [
        "scikit-learn",
        "sklearn",
        "tensorflow",
        "keras",
        "pytorch",
        "xgboost",
        "lightgbm",
        "catboost",
        "opencv",
        "numpy",
        "pandas",
        "scipy"
    ],

    "nlp_genai": [
        "hugging face",
        "huggingface",
        "transformers",
        "langchain",
        "llamaindex",
        "llama index",
        "openai",
        "ollama",
        "rag",
        "retrieval augmented generation",
        "spacy",
        "nltk"
    ],

    "web_development": [
        "html",
        "css",
        "react",
        "react.js",
        "angular",
        "vue",
        "node.js",
        "nodejs",
        "express",
        "express.js",
        "django",
        "flask",
        "fastapi"
    ],

    "database": [
        "mysql",
        "postgresql",
        "postgres",
        "mongodb",
        "sqlite",
        "oracle",
        "redis",
        "elasticsearch",
        "sql"
    ],

    "cloud_devops": [
        "aws",
        "amazon web services",
        "azure",
        "google cloud",
        "gcp",
        "docker",
        "kubernetes",
        "jenkins",
        "github actions",
        "gitlab ci",
        "terraform"
    ],

    "tools": [
        "git",
        "github",
        "gitlab",
        "bitbucket",
        "streamlit",
        "jupyter",
        "jupyter notebook",
        "postman",
        "vs code",
        "visual studio code"
    ],

    "data_science": [
        "data analysis",
        "data science",
        "data visualization",
        "statistics",
        "statistical analysis",
        "power bi",
        "tableau",
        "excel"
    ]
}


# ============================================================
# NON-SKILL WORDS
# ============================================================

NON_SKILL_WORDS = {

    "arjun",
    "rahul",
    "rohit",
    "amit",
    "utkarsh",
    "kumar",
    "singh",

    "resume",
    "curriculum",
    "vitae",
    "candidate",
    "student",
    "engineer",
    "developer",

    "institute",
    "institution",
    "university",
    "college",
    "school",
    "academy",

    "technology",
    "technologies",

    "education",
    "experience",
    "project",
    "projects",
    "profile",
    "summary",
    "objective",

    "email",
    "phone",
    "mobile",
    "address",
    "linkedin",
    "github",

    "manager",
    "management",
    "company",
    "organization",
    "organisation",

    "analysis",
    "analyzer",
    "analyst",

    "btech",
    "b.tech",
    "mtech",
    "m.tech",
    "bsc",
    "msc",
    "bca",
    "mca",

    "present",
    "current",
    "year",
    "years",
    "month",
    "months"
}


# ============================================================
# SECTION HEADERS
# ============================================================

CONTEXT_HEADERS = [
    "education",
    "academic",
    "academics",
    "qualification",
    "qualifications",
    "personal information",
    "personal details",
    "contact",
    "contact information",
    "profile",
    "objective",
    "declaration"
]


SKILL_HEADERS = [
    "skills",
    "technical skills",
    "technical skill",
    "technologies",
    "technology",
    "tools",
    "technical expertise",
    "core skills",
    "programming skills",
    "software skills",
    "skills and technologies"
]


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if not text:
        return ""

    text = str(text).lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    return text


# ============================================================
# CANONICAL SKILL
# ============================================================

def canonical_skill(skill):

    if not skill:
        return ""

    skill = normalize_text(skill).strip()

    mapping = {

        "sklearn": "scikit-learn",
        "scikit learn": "scikit-learn",

        "react.js": "react",
        "reactjs": "react",

        "node.js": "node.js",
        "nodejs": "node.js",
        "node js": "node.js",

        "express.js": "express.js",

        "postgres": "postgresql",

        "gcp": "google cloud",
        "amazon web services": "aws",

        "artificial intelligence":
            "artificial intelligence",

        "machine-learning":
            "machine learning",

        "natural language processing":
            "nlp",

        "large language model":
            "llm",

        "generative artificial intelligence":
            "generative ai",

        "retrieval augmented generation":
            "rag",

        "llama index":
            "llamaindex",

        "huggingface":
            "hugging face",

        "visual studio code":
            "vs code"
    }

    return mapping.get(
        skill,
        skill
    )


# ============================================================
# DETECT CATEGORY
# ============================================================

def detect_category(skill):

    """
    Return test-compatible category names.

    Example:
        python
        -> programming_language

        machine learning
        -> ai_ml
    """

    if not skill:
        return "other"

    skill = normalize_text(skill).strip()

    for category, skills in SKILL_CATEGORIES.items():

        for known_skill in skills:

            if skill == normalize_text(
                known_skill
            ):

                return category

    return "other"


# ============================================================
# GET CATEGORY
# ============================================================

def get_category(skill):

    return detect_category(skill)


# ============================================================
# EXTRACT KNOWN SKILLS
# ============================================================

def extract_known_skills(text):

    normalized = normalize_text(text)

    detected = {}

    for category, skills in SKILL_CATEGORIES.items():

        for skill in skills:

            pattern = (
                r"(?<![a-zA-Z0-9])"
                + re.escape(
                    skill.lower()
                )
                + r"(?![a-zA-Z0-9])"
            )

            if re.search(
                pattern,
                normalized
            ):

                canonical = canonical_skill(
                    skill
                )

                detected[canonical] = {
                    "skill": canonical,
                    "category": category,
                    "confidence": 0.98
                }

    return list(
        detected.values()
    )


# ============================================================
# EXTRACT SKILL SECTION
# ============================================================

def extract_skill_section(text):

    if not text:
        return ""

    lines = text.splitlines()

    skill_lines = []

    inside_skill_section = False

    for line in lines:

        clean = line.strip()

        if not clean:
            continue

        lower = clean.lower()

        # Start skill section
        if any(
            header in lower
            for header in SKILL_HEADERS
        ):

            inside_skill_section = True
            continue

        # Stop skill section
        if inside_skill_section and any(
            header in lower
            for header in CONTEXT_HEADERS
        ):

            inside_skill_section = False
            continue

        if inside_skill_section:

            skill_lines.append(clean)

    return "\n".join(
        skill_lines
    )


# ============================================================
# UNKNOWN SKILL CANDIDATES
# ============================================================

def detect_unknown_candidates(
    text,
    known_skills
):

    candidates = []

    skill_section = extract_skill_section(
        text
    )

    if not skill_section.strip():
        return candidates

    known_names = {
        item["skill"].lower()
        for item in known_skills
    }

    parts = re.split(
        r"[,|;/•\n]+",
        skill_section
    )

    for part in parts:

        candidate = part.strip()

        if not candidate:
            continue

        candidate = re.sub(
            r"^[\-\*\d\.\)\s]+",
            "",
            candidate
        ).strip()

        if not candidate:
            continue

        candidate_lower = candidate.lower()

        # Known skill
        if candidate_lower in known_names:
            continue

        # Non skill
        if candidate_lower in NON_SKILL_WORDS:
            continue

        # Institution
        if any(
            word in candidate_lower
            for word in [
                "institute",
                "university",
                "college",
                "school",
                "academy"
            ]
        ):
            continue

        # Email
        if "@" in candidate:
            continue

        # URLs
        if "http://" in candidate_lower:
            continue

        if "https://" in candidate_lower:
            continue

        # Long sentence
        if len(candidate.split()) > 5:
            continue

        # Technical signal
        technical_signal = (

            any(
                ch in candidate
                for ch in [
                    ".",
                    "+",
                    "#",
                    "-"
                ]
            )

            or any(
                word in candidate_lower
                for word in [
                    "ai",
                    "ml",
                    "data",
                    "cloud",
                    "dev",
                    "api",
                    "sql",
                    "model",
                    "learning",
                    "framework",
                    "database",
                    "analytics",
                    "automation"
                ]
            )
        )

        if not technical_signal:
            continue

        canonical = canonical_skill(
            candidate
        )

        if canonical.lower() in known_names:
            continue

        if any(
            item["skill"].lower()
            == canonical.lower()
            for item in candidates
        ):
            continue

        candidates.append({
            "skill": canonical,
            "category": "unknown",
            "confidence": 0.70
        })

    return candidates


# ============================================================
# MAIN SKILL EXTRACTION
# ============================================================

def extract_skills(text):

    if not text:

        return {
            "total_skills": 0,
            "known_skills": [],
            "unknown_candidates": [],
            "skills": []
        }

    # --------------------------------------------------------
    # Known
    # --------------------------------------------------------

    known_skills = extract_known_skills(
        text
    )

    # --------------------------------------------------------
    # Unknown
    # --------------------------------------------------------

    unknown_candidates = detect_unknown_candidates(
        text,
        known_skills
    )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    known_lower = {
        item["skill"].lower()
        for item in known_skills
    }

    unknown_candidates = [
        item
        for item in unknown_candidates
        if item["skill"].lower()
        not in known_lower
    ]

    # --------------------------------------------------------
    # Compatibility "skills" list
    # --------------------------------------------------------

    all_skills = []

    for item in known_skills:

        all_skills.append({
            "skill": item["skill"],
            "category": item["category"],
            "confidence": item["confidence"],
            "known_skill": True
        })

    for item in unknown_candidates:

        all_skills.append({
            "skill": item["skill"],
            "category": item["category"],
            "confidence": item["confidence"],
            "known_skill": False
        })

    # --------------------------------------------------------
    # Total
    # --------------------------------------------------------

    total_skills = len(all_skills)

    return {

        "total_skills":
            total_skills,

        "known_skills":
            known_skills,

        "unknown_candidates":
            unknown_candidates,

        # Backward compatibility for tests/V3
        "skills":
            all_skills
    }