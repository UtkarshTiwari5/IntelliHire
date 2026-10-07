from pathlib import Path

from src.resume_parser import (
    clean_text,
    extract_email,
    extract_linkedin,
    extract_github,
    extract_name,
    extract_sections
)


def test_clean_text():

    text = "Python     Developer\n\n\n\nAI Engineer"

    result = clean_text(text)

    assert result == (
        "Python Developer\n\nAI Engineer"
    )


def test_extract_email():

    text = "Contact: test@example.com"

    assert extract_email(text) == "test@example.com"


def test_extract_linkedin():

    text = (
        "https://www.linkedin.com/in/test-user"
    )

    result = extract_linkedin(text)

    assert "linkedin.com/in/test-user" in result


def test_extract_github():

    text = (
        "https://github.com/test-user"
    )

    result = extract_github(text)

    assert "github.com/test-user" in result


def test_extract_name():

    text = """
    Utkarsh Tiwari
    test@example.com
    Python Developer
    """

    result = extract_name(text)

    assert result == "Utkarsh Tiwari"


def test_extract_sections():

    text = """
    Education
    B.Tech Artificial Intelligence

    Skills
    Python
    Machine Learning

    Projects
    IntelliHire
    """

    result = extract_sections(text)

    assert "education" in result
    assert "skills" in result
    assert "projects" in result