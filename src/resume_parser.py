import re
from pathlib import Path
from typing import Dict, List, Any

import pdfplumber
from docx import Document

from utils.logger import get_logger


logger = get_logger(__name__)


# ============================================================
# SECTION ALIASES
# ============================================================

SECTION_ALIASES = {

    "summary": [
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective"
    ],

    "education": [
        "education",
        "academic background",
        "academic qualification",
        "qualifications"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history"
    ],

    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "technologies",
        "technical expertise"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project experience"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "licenses"
    ],

    "achievements": [
        "achievements",
        "accomplishments",
        "awards",
        "honors"
    ],

    "languages": [
        "languages",
        "language proficiency"
    ],

    "interests": [
        "interests",
        "hobbies"
    ]
}


# ============================================================
# TEXT EXTRACTION
# ============================================================

def extract_pdf_text(file_path: str) -> str:

    text_parts = []

    try:

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text_parts.append(page_text)

    except Exception as exc:

        logger.exception(
            "Failed to extract PDF text: %s",
            exc
        )

        raise

    return "\n".join(text_parts)


def extract_docx_text(file_path: str) -> str:

    try:

        document = Document(file_path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)

    except Exception as exc:

        logger.exception(
            "Failed to extract DOCX text: %s",
            exc
        )

        raise


def extract_text(file_path: str) -> str:

    path = Path(file_path)

    extension = path.suffix.lower()

    if extension == ".pdf":

        return extract_pdf_text(str(path))

    if extension == ".docx":

        return extract_docx_text(str(path))

    raise ValueError(
        "Unsupported file type. "
        "Only PDF and DOCX are supported."
    )


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text: str) -> str:

    if not text:
        return ""

    text = text.replace("\x00", " ")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
# CONTACT INFORMATION
# ============================================================

def extract_email(text: str):

    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    match = re.search(
        pattern,
        text
    )

    return match.group(0) if match else None


def extract_phone(text: str):

    patterns = [

        r"(?:\+?\d{1,3}[\s.-]?)?"
        r"(?:\(?\d{2,4}\)?[\s.-]?)"
        r"\d{3,4}[\s.-]?\d{3,4}",

        r"\+?\d{10,15}"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            return match.group(0).strip()

    return None


def extract_linkedin(text: str):

    pattern = (
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"linkedin\.com/in/[A-Za-z0-9._-]+"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    return match.group(0) if match else None


def extract_github(text: str):

    pattern = (
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"github\.com/[A-Za-z0-9._-]+"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    return match.group(0) if match else None


# ============================================================
# NAME EXTRACTION
# ============================================================

def extract_name(text: str):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    ignored_words = {
        "resume",
        "curriculum vitae",
        "cv",
        "profile"
    }

    for line in lines[:10]:

        cleaned = line.strip()

        lower = cleaned.lower()

        if lower in ignored_words:
            continue

        if "@" in cleaned:
            continue

        if "linkedin.com" in lower:
            continue

        if "github.com" in lower:
            continue

        if re.search(r"\d", cleaned):
            continue

        words = cleaned.split()

        if 2 <= len(words) <= 5:

            if all(
                re.match(
                    r"^[A-Za-zÀ-ÖØ-öø-ÿ.'-]+$",
                    word
                )
                for word in words
            ):

                return cleaned

    return None


# ============================================================
# SECTION DETECTION
# ============================================================

def normalize_heading(line: str) -> str:

    line = line.strip()

    line = re.sub(
        r"[:\-|]+$",
        "",
        line
    )

    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line.lower().strip()


def detect_section_heading(line: str):

    normalized = normalize_heading(line)

    for section, aliases in SECTION_ALIASES.items():

        if normalized in aliases:
            return section

    return None


def extract_sections(text: str) -> Dict[str, str]:

    sections = {}

    current_section = "other"

    sections[current_section] = []

    for line in text.splitlines():

        stripped = line.strip()

        if not stripped:
            continue

        detected = detect_section_heading(stripped)

        if detected:

            current_section = detected

            if current_section not in sections:
                sections[current_section] = []

            continue

        sections.setdefault(
            current_section,
            []
        ).append(stripped)

    final_sections = {}

    for section, lines in sections.items():

        content = "\n".join(lines).strip()

        if content:
            final_sections[section] = content

    return final_sections


# ============================================================
# LIST CONVERSION
# ============================================================

def section_to_list(content: str) -> List[str]:

    if not content:
        return []

    lines = []

    for line in content.splitlines():

        line = line.strip()

        line = re.sub(
            r"^[•●▪◦\-*]\s*",
            "",
            line
        )

        if line:
            lines.append(line)

    return lines


# ============================================================
# COMPLETE RESUME PARSER
# ============================================================

def parse_resume(file_path: str) -> Dict[str, Any]:

    logger.info(
        "Parsing resume: %s",
        file_path
    )

    raw_text = extract_text(file_path)

    cleaned_text = clean_text(raw_text)

    if not cleaned_text:

        raise ValueError(
            "No readable text was found in the resume."
        )

    sections = extract_sections(
        cleaned_text
    )

    resume_data = {

        "file_name": Path(file_path).name,

        "raw_text": cleaned_text,

        "name": extract_name(
            cleaned_text
        ),

        "email": extract_email(
            cleaned_text
        ),

        "phone": extract_phone(
            cleaned_text
        ),

        "linkedin": extract_linkedin(
            cleaned_text
        ),

        "github": extract_github(
            cleaned_text
        ),

        "sections": sections,

        "summary": sections.get(
            "summary",
            ""
        ),

        "education": section_to_list(
            sections.get(
                "education",
                ""
            )
        ),

        "experience": section_to_list(
            sections.get(
                "experience",
                ""
            )
        ),

        "skills": section_to_list(
            sections.get(
                "skills",
                ""
            )
        ),

        "projects": section_to_list(
            sections.get(
                "projects",
                ""
            )
        ),

        "certifications": section_to_list(
            sections.get(
                "certifications",
                ""
            )
        ),

        "achievements": section_to_list(
            sections.get(
                "achievements",
                ""
            )
        ),

        "languages": section_to_list(
            sections.get(
                "languages",
                ""
            )
        ),

        "interests": section_to_list(
            sections.get(
                "interests",
                ""
            )
        )
    }

    logger.info(
        "Resume parsed successfully: %s",
        Path(file_path).name
    )

    return resume_data