# ============================================================
# IntelliHire - Phase 11 AI Interview
# Gemini AI Integrated Version
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import re

from api.database import get_db
from api.models import User, Job, Interview, InterviewQuestion
from api.auth import require_role

from api.gemini_service import (
    generate_interview_question,
    evaluate_interview_answer
)

router = APIRouter(
    prefix="/interviews",
    tags=["AI Interviews"]
)


# ============================================================
# REQUEST MODELS
# ============================================================

class InterviewStart(BaseModel):
    job_id: int


class QuestionCreate(BaseModel):
    question: str


class AnswerSubmit(BaseModel):
    answer: str


# ============================================================
# HELPER - EXTRACT SCORE FROM GEMINI RESPONSE
# ============================================================

def extract_ai_score(ai_response: str):

    match = re.search(
        r"Score\s*:\s*(\d{1,3})",
        ai_response,
        re.IGNORECASE
    )

    if not match:
        raise ValueError(
            "Gemini response did not contain a valid score."
        )

    score = int(match.group(1))

    if score < 0:
        score = 0

    if score > 100:
        score = 100

    return score


# ============================================================
# HELPER - EXTRACT FEEDBACK
# ============================================================

def extract_ai_feedback(ai_response: str):

    feedback_match = re.search(
        r"Feedback\s*:\s*(.*?)(?=\n\s*Strengths\s*:|\n\s*Weaknesses\s*:|$)",
        ai_response,
        re.IGNORECASE | re.DOTALL
    )

    strengths_match = re.search(
        r"Strengths\s*:\s*(.*?)(?=\n\s*Weaknesses\s*:|$)",
        ai_response,
        re.IGNORECASE | re.DOTALL
    )

    weaknesses_match = re.search(
        r"Weaknesses\s*:\s*(.*)$",
        ai_response,
        re.IGNORECASE | re.DOTALL
    )

    feedback = ""

    if feedback_match:
        feedback += (
            "Feedback: "
            + feedback_match.group(1).strip()
        )

    if strengths_match:
        feedback += (
            "\nStrengths: "
            + strengths_match.group(1).strip()
        )

    if weaknesses_match:
        feedback += (
            "\nWeaknesses: "
            + weaknesses_match.group(1).strip()
        )

    if not feedback:
        feedback = ai_response.strip()

    return feedback


# ============================================================
# 11.1 - START AI INTERVIEW
# ============================================================

@router.post("/start")
def start_interview(
    interview_data: InterviewStart,
    current_user: User = Depends(
        require_role("user")
    ),
    db: Session = Depends(get_db)
):

    job = (
        db.query(Job)
        .filter(
            Job.id == interview_data.job_id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    new_interview = Interview(
        user_id=current_user.id,
        job_id=job.id,
        score=None,
        result=None
    )

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return {
        "message": "Interview started successfully",

        "interview": {
            "id": new_interview.id,
            "user_id": new_interview.user_id,
            "job_id": new_interview.job_id,
            "job_title": job.title,
            "score": new_interview.score,
            "result": new_interview.result,
            "created_at": new_interview.created_at
        }
    }


# ============================================================
# 11.3 - CREATE MANUAL INTERVIEW QUESTION
# ============================================================

@router.post("/{interview_id}/questions")
def create_question(
    interview_id: int,
    question_data: QuestionCreate,
    current_user: User = Depends(
        require_role("user")
    ),
    db: Session = Depends(get_db)
):

    interview = (
        db.query(Interview)
        .filter(
            Interview.id == interview_id,
            Interview.user_id == current_user.id
        )
        .first()
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    question_text = question_data.question.strip()

    if not question_text:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    new_question = InterviewQuestion(
        interview_id=interview.id,
        question=question_text,
        answer=None,
        score=None,
        feedback=None
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return {
        "message": "Interview question created successfully",

        "question": {
            "id": new_question.id,
            "interview_id": new_question.interview_id,
            "question": new_question.question,
            "answer": new_question.answer,
            "score": new_question.score,
            "feedback": new_question.feedback,
            "created_at": new_question.created_at
        }
    }


# ============================================================
# 11.3 - GENERATE QUESTION USING GEMINI
# ============================================================

@router.post("/{interview_id}/generate-question")
def generate_question(
    interview_id: int,
    current_user: User = Depends(
        require_role("user")
    ),
    db: Session = Depends(get_db)
):

    interview = (
        db.query(Interview)
        .filter(
            Interview.id == interview_id,
            Interview.user_id == current_user.id
        )
        .first()
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    job = (
        db.query(Job)
        .filter(
            Job.id == interview.job_id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    try:

        question_text = generate_interview_question(
            job_title=job.title,
            job_description=job.description
        )

    except Exception as e:

     print(
        f"Gemini unavailable. Using dynamic fallback question. "
        f"Error: {e}"
    )

    # --------------------------------------------------------
    # DYNAMIC FALLBACK QUESTIONS
    # --------------------------------------------------------

    fallback_questions = [
        f"Explain the core concepts and important skills required for the {job.title} role.",

        f"Describe a technical project where you used skills relevant to the {job.title} role.",

        f"What is the most challenging problem you have solved using your technical skills? Explain your approach.",

        f"Suppose you are given a difficult technical problem related to the {job.title} role. How would you analyze and solve it?",

        f"What are the common challenges faced by a professional working as a {job.title}, and how would you handle them?",

        f"Explain how you would improve the performance, reliability, or efficiency of a system related to the {job.title} role.",

        f"Which technical skill do you consider strongest for the {job.title} role, and how have you applied it in a real project?",

        f"Describe a situation where your first technical approach failed. What did you change to solve the problem?",

        f"How would you design a simple solution for a real-world problem related to the {job.title} role?",

        f"What new technology or concept related to the {job.title} role would you like to learn, and why?"
    ]

    # Get existing questions
    existing_questions = (
        db.query(InterviewQuestion)
        .filter(
            InterviewQuestion.interview_id == interview.id
        )
        .count()
    )

    # Select next question dynamically
    question_index = existing_questions % len(
        fallback_questions
    )

    question_text = fallback_questions[
        question_index
    ]

    question_text = question_text.strip()

    if not question_text:
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an empty question."
        )

    new_question = InterviewQuestion(
        interview_id=interview.id,
        question=question_text,
        answer=None,
        score=None,
        feedback=None
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return {
        "message": "AI interview question generated successfully",

        "question": {
            "id": new_question.id,
            "interview_id": new_question.interview_id,
            "question": new_question.question,
            "answer": new_question.answer,
            "score": new_question.score,
            "feedback": new_question.feedback
        }
    }
# ============================================================
# 11.3 - GET INTERVIEW QUESTIONS
# ============================================================

@router.get("/{interview_id}/questions")
def get_interview_questions(
    interview_id: int,
    current_user: User = Depends(
        require_role("user")
    ),
    db: Session = Depends(get_db)
):

    interview = (
        db.query(Interview)
        .filter(
            Interview.id == interview_id,
            Interview.user_id == current_user.id
        )
        .first()
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    questions = (
        db.query(InterviewQuestion)
        .filter(
            InterviewQuestion.interview_id == interview_id
        )
        .order_by(
            InterviewQuestion.created_at.asc()
        )
        .all()
    )

    return {
        "interview_id": interview_id,

        "questions": [
            {
                "id": question.id,
                "question": question.question,
                "answer": question.answer,
                "score": question.score,
                "feedback": question.feedback,
                "created_at": question.created_at
            }
            for question in questions
        ]
    }


# ============================================================
# 11.3 - SUBMIT ANSWER + GEMINI AI EVALUATION
# ============================================================

@router.post("/questions/{question_id}/answer")
def submit_answer(
    question_id: int,
    answer_data: AnswerSubmit,
    current_user: User = Depends(
        require_role("user")
    ),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # FIND QUESTION
    # --------------------------------------------------------

    question = (
        db.query(InterviewQuestion)
        .join(
            Interview,
            InterviewQuestion.interview_id == Interview.id
        )
        .filter(
            InterviewQuestion.id == question_id,
            Interview.user_id == current_user.id
        )
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Interview question not found."
        )

    # --------------------------------------------------------
    # VALIDATE ANSWER
    # --------------------------------------------------------

    answer = answer_data.answer.strip()

    if not answer:
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty."
        )

    # --------------------------------------------------------
    # GET INTERVIEW
    # --------------------------------------------------------

    interview = (
        db.query(Interview)
        .filter(
            Interview.id == question.interview_id
        )
        .first()
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    # --------------------------------------------------------
    # GET JOB
    # --------------------------------------------------------

    job = (
        db.query(Job)
        .filter(
            Job.id == interview.job_id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    # --------------------------------------------------------
    # GEMINI AI EVALUATION
    # --------------------------------------------------------

    try:

        ai_evaluation = evaluate_interview_answer(
            question=question.question,
            answer=answer,
            job_title=job.title,
            job_description=job.description
        )

    except Exception as e:

        # ----------------------------------------------------
        # GEMINI UNAVAILABLE FALLBACK
        # ----------------------------------------------------

        print(
            f"Gemini answer evaluation unavailable. "
            f"Using fallback evaluation. Error: {e}"
        )

        score = 70

        feedback = (
            "Feedback: Your answer has been submitted successfully. "
            "The AI evaluator is temporarily unavailable, so a "
            "fallback evaluation was used."
            "\nStrengths: The answer addresses the interview question."
            "\nWeaknesses: Detailed AI-based feedback is unavailable "
            "at the moment."
        )

        question.answer = answer
        question.score = score
        question.feedback = feedback

        db.commit()
        db.refresh(question)

        return {
            "message": (
                "Answer submitted successfully. "
                "Fallback evaluation used."
            ),

            "question": {
                "id": question.id,
                "interview_id": question.interview_id,
                "question": question.question,
                "answer": question.answer,
                "score": question.score,
                "feedback": question.feedback
            },

            "ai_evaluation": (
                "Gemini unavailable. Fallback evaluation used."
            )
        }

    # --------------------------------------------------------
    # EXTRACT SCORE
    # --------------------------------------------------------

    try:

        score = extract_ai_score(
            ai_evaluation
        )

    except ValueError as e:

        # ----------------------------------------------------
        # INVALID GEMINI RESPONSE FALLBACK
        # ----------------------------------------------------

        print(
            f"Invalid Gemini evaluation response. "
            f"Using fallback score. Error: {e}"
        )

        score = 70

        feedback = (
            "Feedback: Your answer was submitted successfully. "
            "The AI response could not be parsed completely."
            "\nStrengths: Your answer was received."
            "\nWeaknesses: Detailed AI feedback was unavailable."
        )

        question.answer = answer
        question.score = score
        question.feedback = feedback

        db.commit()
        db.refresh(question)

        return {
            "message": (
                "Answer submitted successfully. "
                "Fallback evaluation used."
            ),

            "question": {
                "id": question.id,
                "interview_id": question.interview_id,
                "question": question.question,
                "answer": question.answer,
                "score": question.score,
                "feedback": question.feedback
            },

            "ai_evaluation": ai_evaluation
        }

    # --------------------------------------------------------
    # EXTRACT FEEDBACK
    # --------------------------------------------------------

    feedback = extract_ai_feedback(
        ai_evaluation
    )

    # --------------------------------------------------------
    # SAVE ANSWER + SCORE + FEEDBACK
    # --------------------------------------------------------

    question.answer = answer
    question.score = score
    question.feedback = feedback

    db.commit()
    db.refresh(question)

    return {
        "message": "Answer evaluated successfully by Gemini AI",

        "question": {
            "id": question.id,
            "interview_id": question.interview_id,
            "question": question.question,
            "answer": question.answer,
            "score": question.score,
            "feedback": question.feedback
        },

        "ai_evaluation": ai_evaluation
    }
# ============================================================
# USER - MY INTERVIEWS
# ============================================================

@router.get("/my-interviews")
def get_my_interviews(
    current_user: User = Depends(
        require_role("user")
    ),
    db: Session = Depends(get_db)
):

    interviews = (
        db.query(Interview)
        .filter(
            Interview.user_id == current_user.id
        )
        .order_by(
            Interview.created_at.desc()
        )
        .all()
    )

    return {
        "interviews": [
            {
                "id": interview.id,
                "job_id": interview.job_id,
                "score": interview.score,
                "result": interview.result,
                "created_at": interview.created_at
            }
            for interview in interviews
        ]
    }


# ============================================================
# GET SINGLE INTERVIEW
# ============================================================

@router.get("/{interview_id}")
def get_interview(
    interview_id: int,
    current_user: User = Depends(
        require_role("user")
    ),
    db: Session = Depends(get_db)
):

    interview = (
        db.query(Interview)
        .filter(
            Interview.id == interview_id,
            Interview.user_id == current_user.id
        )
        .first()
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    return {
        "interview": {
            "id": interview.id,
            "user_id": interview.user_id,
            "job_id": interview.job_id,
            "score": interview.score,
            "result": interview.result,
            "created_at": interview.created_at
        }
    }


# ============================================================
# 11.4 - OVERALL INTERVIEW EVALUATION
# ============================================================

@router.post("/{interview_id}/evaluate")
def evaluate_interview(
    interview_id: int,
    current_user: User = Depends(
        require_role("user")
    ),
    db: Session = Depends(get_db)
):

    interview = (
        db.query(Interview)
        .filter(
            Interview.id == interview_id,
            Interview.user_id == current_user.id
        )
        .first()
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    questions = (
        db.query(InterviewQuestion)
        .filter(
            InterviewQuestion.interview_id == interview_id
        )
        .all()
    )

    if not questions:
        raise HTTPException(
            status_code=400,
            detail="No questions found for this interview."
        )

    scored_questions = [
        question
        for question in questions
        if question.score is not None
    ]

    if not scored_questions:
        raise HTTPException(
            status_code=400,
            detail="No answered questions available for evaluation."
        )

    total_score = sum(
        question.score
        for question in scored_questions
    )

    overall_score = round(
        total_score / len(scored_questions)
    )

    if overall_score >= 60:
        result = "Passed"
    else:
        result = "Needs Improvement"

    interview.score = overall_score
    interview.result = result

    db.commit()
    db.refresh(interview)

    return {
        "message": "Interview evaluated successfully",

        "interview": {
            "id": interview.id,
            "job_id": interview.job_id,
            "score": interview.score,
            "result": interview.result,
            "total_questions": len(questions),
            "answered_questions": len(scored_questions)
        }
    }


# ============================================================
# 11.5 - DETAILED INTERVIEW EVALUATION
# ============================================================

@router.get("/{interview_id}/evaluation")
def get_interview_evaluation(
    interview_id: int,
    current_user: User = Depends(
        require_role("user")
    ),
    db: Session = Depends(get_db)
):

    interview = (
        db.query(Interview)
        .filter(
            Interview.id == interview_id,
            Interview.user_id == current_user.id
        )
        .first()
    )

    if not interview:
        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    questions = (
        db.query(InterviewQuestion)
        .filter(
            InterviewQuestion.interview_id == interview_id
        )
        .order_by(
            InterviewQuestion.created_at.asc()
        )
        .all()
    )

    question_details = []

    for question in questions:

        question_details.append({
            "question_id": question.id,
            "question": question.question,
            "answer": question.answer,
            "score": question.score,
            "feedback": question.feedback,
            "created_at": question.created_at
        })

    answered_questions = sum(
        1
        for question in questions
        if question.answer is not None
    )

    return {
        "message": "Detailed interview evaluation fetched successfully",

        "interview": {
            "id": interview.id,
            "user_id": interview.user_id,
            "job_id": interview.job_id,
            "overall_score": interview.score,
            "result": interview.result,
            "total_questions": len(questions),
            "answered_questions": answered_questions
        },

        "evaluation": question_details
    }