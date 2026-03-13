"""
Main FastAPI application for Adaptive Quiz Engine
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
from datetime import datetime

from app.services import quiz_service
from app.algorithms import irt
from app.ai_study_plan import generate_study_plan

# Create FastAPI app
app = FastAPI(
    title="Adaptive Quiz Engine",
    description="AI-powered adaptive testing system using IRT",
    version="1.0.0"
)

# Enable CORS (so frontend can access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== Request/Response Models ==========

class StartSessionRequest(BaseModel):
    user_id: Optional[str] = None

class SessionResponse(BaseModel):
    session_id: str
    current_ability: float
    message: str

class AnswerSubmission(BaseModel):
    session_id: str
    question_id: str
    answer: str

class AnswerResponse(BaseModel):
    correct: bool
    old_ability: float
    new_ability: float
    improvement: float
    explanation: Optional[str] = None
    quiz_complete: bool
    message: Optional[str] = None

class QuestionResponse(BaseModel):
    question_id: str
    text: str
    options: List[str]
    difficulty: float
    topic: str

class StudyPlanRequest(BaseModel):
    session_id: str

class StudyPlanResponse(BaseModel):
    study_plan: str
    session_summary: Dict

# ========== API Endpoints ==========

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Adaptive Quiz Engine API",
        "version": "1.0.0",
        "endpoints": [
            "/docs - API Documentation",
            "/start-session - Start new quiz",
            "/next-question/{session_id} - Get next question",
            "/submit-answer - Submit answer",
            "/session-summary/{session_id} - Get session summary",
            "/study-plan/{session_id} - Get AI study plan"
        ]
    }

@app.post("/start-session", response_model=SessionResponse)
async def start_session(request: StartSessionRequest):
    """
    Start a new quiz session
    Returns a session ID and starting ability
    """
    try:
        session = quiz_service.create_new_session(request.user_id)
        return {
            "session_id": session["session_id"],
            "current_ability": session["current_ability"],
            "message": "Session created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/next-question/{session_id}", response_model=QuestionResponse)
async def get_next_question(session_id: str):
    """
    Get the next adaptive question for a session
    """
    try:
        question = quiz_service.get_next_question(session_id)
        
        if "error" in question:
            raise HTTPException(status_code=404, detail=question["error"])
        
        if "message" in question:
            # Quiz completed
            raise HTTPException(status_code=200, detail=question["message"])
        
        return question
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/submit-answer", response_model=AnswerResponse)
async def submit_answer(submission: AnswerSubmission):
    """
    Submit an answer and get updated ability
    """
    try:
        result = quiz_service.submit_answer(
            submission.session_id,
            submission.question_id,
            submission.answer
        )
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        # Add user-friendly message
        if result["quiz_complete"]:
            result["message"] = "Quiz completed! Get your study plan at /study-plan/" + submission.session_id
        else:
            if result["correct"]:
                result["message"] = "Correct! Your ability increased."
            else:
                result["message"] = "Incorrect. Keep trying!"
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/session-summary/{session_id}")
async def get_session_summary(session_id: str):
    """
    Get summary of completed quiz session
    """
    try:
        summary = quiz_service.get_session_summary(session_id)
        
        if "error" in summary:
            raise HTTPException(status_code=404, detail=summary["error"])
        
        return summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/study-plan/{session_id}", response_model=StudyPlanResponse)
async def get_study_plan(session_id: str):
    """
    Generate AI-powered personalized study plan
    """
    try:
        # Get session summary
        summary = quiz_service.get_session_summary(session_id)
        
        if "error" in summary:
            raise HTTPException(status_code=404, detail=summary["error"])
        
        # Generate study plan using AI
        study_plan = generate_study_plan(summary)
        
        return {
            "study_plan": study_plan,
            "session_summary": summary
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/questions")
async def get_all_questions():
    """
    Get all questions (for testing/debugging)
    """
    try:
        questions = quiz_service.get_all_questions()
        return {"total": len(questions), "questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========== Run the app ==========
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)