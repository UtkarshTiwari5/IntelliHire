# ============================================================
# IntelliHire - Gemini AI Service
# Phase 11 - AI Interview
# ============================================================

import os
import time

from dotenv import load_dotenv
from  google import genai


# ============================================================
# LOAD .ENV FROM PROJECT ROOT
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ENV_PATH = os.path.join(
    BASE_DIR,
    ".env"
)

load_dotenv(
    dotenv_path=ENV_PATH,
    override=True
)


# ============================================================
# GEMINI API KEY
# ============================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured in .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "gemini-3.8-flash"


# ============================================================
# GEMINI TEXT GENERATION WITH RETRY
# ============================================================

def generate_ai_response(
    prompt: str,
    max_retries: int = 3
) -> str:

    if not prompt or not prompt.strip():
        raise ValueError(
            "Prompt cannot be empty."
        )

    last_error = None

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text.strip()

        except Exception as e:

            last_error = e

            error_text = str(e)

            print(
                f"Gemini error (attempt {attempt + 1}): "
                f"{error_text}"
            )

            # ------------------------------------------------
            # RETRY TEMPORARY ERRORS
            # ------------------------------------------------

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
            ):

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

            # ------------------------------------------------
            # 429 = QUOTA / RATE LIMIT
            # ------------------------------------------------

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):

                print(
                    "Gemini API quota/rate limit reached."
                )

                raise RuntimeError(
                    "Gemini API quota/rate limit reached. "
                    "Please check the Google AI Studio project "
                    "and API key quota."
                )

            # ------------------------------------------------
            # OTHER ERRORS
            # ------------------------------------------------

            raise e

    raise RuntimeError(
        f"Gemini request failed after "
        f"{max_retries} attempts: {last_error}"
    )


# ============================================================
# AI INTERVIEW QUESTION GENERATION
# ============================================================

def generate_interview_question(
    job_title: str,
    job_description: str
) -> str:

    prompt = f"""
You are an AI technical interviewer for IntelliHire.

Generate ONE interview question for the candidate.

Job Title:
{job_title}

Job Description:
{job_description}

Requirements:
- Ask one clear interview question.
- Make it relevant to the job.
- Do not provide the answer.
- Do not add unnecessary explanation.
- Return only the question.
"""

    return generate_ai_response(prompt)


# ============================================================
# AI ANSWER EVALUATION
# ============================================================

def evaluate_interview_answer(
    question: str,
    answer: str,
    job_title: str,
    job_description: str
) -> str:

    prompt = f"""
You are an expert AI interviewer evaluating a candidate.

Job Title:
{job_title}

Job Description:
{job_description}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Consider:
- Technical correctness
- Understanding of the concept
- Relevance to the question
- Explanation quality
- Practical knowledge

Return the evaluation in exactly this format:

Score: <number from 0 to 100>
Feedback: <short constructive feedback>
Strengths: <main strengths>
Weaknesses: <main weaknesses>
"""

    return generate_ai_response(prompt)