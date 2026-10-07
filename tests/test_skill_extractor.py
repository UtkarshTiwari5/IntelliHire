from src.skill_extractor import (
    extract_skills,
    detect_category
)


def test_detect_python():

    assert (
        detect_category("python")
        == "programming_language"
    )


def test_detect_machine_learning():

    assert (
        detect_category("machine learning")
        == "ai_ml"
    )


def test_extract_known_skills():

    text = """
    I have experience with Python,
    Machine Learning, FastAPI and Docker.
    """

    result = extract_skills(text)

    skills = [
        item["skill"]
        for item in result["known_skills"]
    ]

    assert "python" in skills
    assert "machine learning" in skills
    assert "fastapi" in skills
    assert "docker" in skills


def test_unknown_skill_is_not_ignored():

    text = """
    Built an AI agent using Python,
    LangChain and RAG.
    """

    result = extract_skills(text)

    all_skill_names = [
        item["skill"].lower()
        for item in result["skills"]
    ]

    assert "langchain" in all_skill_names


def test_skill_count():

    text = """
    Python
    FastAPI
    Docker
    """

    result = extract_skills(text)

    assert result["total_skills"] >= 3