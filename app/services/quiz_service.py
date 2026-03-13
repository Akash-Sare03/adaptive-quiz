"""
Quiz service that manages the adaptive quiz flow
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database import questions_collection, sessions_collection
from app.algorithms import irt
from datetime import datetime
from bson import ObjectId
import random


def create_new_session(user_id: str = None) -> dict:
    """
    Create a new quiz session for a student
    """
    session = {
        "session_id": str(ObjectId()),
        "user_id": user_id or "anonymous",
        "current_ability": irt.estimate_starting_ability(),
        "questions_answered": [],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "completed": False
    }
    
    # Insert into database
    result = sessions_collection.insert_one(session)
    
    return session


def get_session(session_id: str) -> dict:
    """
    Get session by ID
    """
    session = sessions_collection.find_one({"session_id": session_id})
    return session


def get_next_question(session_id: str) -> dict:
    """
    Get the next adaptive question for a session
    """
    # Get session
    session = get_session(session_id)
    if not session:
        return {"error": "Session not found"}
    
    # Check if quiz is complete
    if session.get("completed", False):
        return {"message": "Quiz completed", "completed": True}
    
    # Get questions already answered
    answered_ids = [q["question_id"] for q in session.get("questions_answered", [])]
    
    # Get current ability
    current_ability = session.get("current_ability", 0.5)
    
    # Get difficulty range for next question
    min_diff, max_diff = irt.get_difficulty_range(current_ability)
    
    # Find unanswered questions within difficulty range
    query = {
        "question_id": {"$nin": answered_ids},
        "difficulty": {"$gte": min_diff, "$lte": max_diff}
    }
    
    available_questions = list(questions_collection.find(query))
    
    # If no questions in range, expand range
    if not available_questions:
        # Try all unanswered questions
        query = {"question_id": {"$nin": answered_ids}}
        available_questions = list(questions_collection.find(query))
    
    if not available_questions:
        return {"error": "No more questions available"}
    
    # Find question with difficulty closest to current ability
    next_question = min(available_questions, 
                       key=lambda q: abs(q["difficulty"] - current_ability))
    
    # Remove sensitive data (correct_answer) before sending to client
    client_question = {
        "question_id": next_question["question_id"],
        "text": next_question["text"],
        "options": next_question.get("options", []),
        "difficulty": next_question["difficulty"],
        "topic": next_question["topic"]
    }
    
    return client_question


def submit_answer(session_id: str, question_id: str, user_answer: str) -> dict:
    """
    Process student's answer and update ability
    """
    # Get session
    session = get_session(session_id)
    if not session:
        return {"error": "Session not found"}
    
    # Get question
    question = questions_collection.find_one({"question_id": question_id})
    if not question:
        return {"error": "Question not found"}
    
    # Check if correct
    is_correct = user_answer == question["correct_answer"]
    
    # Calculate new ability using IRT
    old_ability = session["current_ability"]
    new_ability = irt.calculate_new_ability(
        old_ability,
        question["difficulty"],
        is_correct
    )
    
    # Record this answer
    answer_record = {
        "question_id": question_id,
        "user_answer": user_answer,
        "is_correct": is_correct,
        "difficulty": question["difficulty"],
        "topic": question["topic"],
        "ability_before": old_ability,
        "ability_after": new_ability,
        "timestamp": datetime.now()
    }
    
    # Update session
    sessions_collection.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "current_ability": new_ability,
                "updated_at": datetime.now()
            },
            "$push": {"questions_answered": answer_record}
        }
    )
    
    # Check if quiz should end
    questions_answered = session.get("questions_answered", []) + [answer_record]
    is_complete = irt.is_quiz_complete(questions_answered)
    
    if is_complete:
        sessions_collection.update_one(
            {"session_id": session_id},
            {"$set": {"completed": True}}
        )
    
    # Prepare response
    result = {
        "correct": is_correct,
        "old_ability": round(old_ability, 3),
        "new_ability": round(new_ability, 3),
        "improvement": round(new_ability - old_ability, 3),
        "explanation": question.get("explanation", ""),
        "quiz_complete": is_complete
    }
    
    return result


def get_session_summary(session_id: str) -> dict:
    """
    Get summary of completed quiz session
    """
    session = get_session(session_id)
    if not session:
        return {"error": "Session not found"}
    
    questions = session.get("questions_answered", [])
    
    # Calculate statistics
    total = len(questions)
    correct = sum(1 for q in questions if q["is_correct"])
    
    # Group by topic
    topics = {}
    for q in questions:
        topic = q.get("topic", "Unknown")
        if topic not in topics:
            topics[topic] = {"total": 0, "correct": 0}
        topics[topic]["total"] += 1
        if q["is_correct"]:
            topics[topic]["correct"] += 1
    
    # Calculate percentages
    for topic in topics:
        topics[topic]["percentage"] = round(
            (topics[topic]["correct"] / topics[topic]["total"]) * 100, 1
        )
    
    summary = {
        "session_id": session_id,
        "total_questions": total,
        "correct_answers": correct,
        "score_percentage": round((correct/total)*100, 1) if total > 0 else 0,
        "final_ability": session.get("current_ability"),
        "starting_ability": session.get("questions_answered", [{}])[0].get("ability_before", 0.5) if questions else 0.5,
        "ability_improvement": round(session.get("current_ability", 0) - 0.5, 3),
        "topics_performance": topics,
        "completed": session.get("completed", False)
    }
    
    return summary


def get_all_questions() -> list:
    """
    Get all questions (for testing)
    """
    return list(questions_collection.find({}, {"correct_answer": 0}))


# Test the service
if __name__ == "__main__":
    print("Testing Quiz Service\n")
    
    # Create a test session
    session = create_new_session("test_user")
    print(f"Created session: {session['session_id']}")
    print(f"Starting ability: {session['current_ability']}\n")
    
    # Simulate a few answers
    test_answers = [
        ("q1", "5"),      # Easy - correct
        ("q6", "15"),     # Medium - correct
        ("q11", "24"),    # Hard - correct
        ("q7", "1/6"),    # Medium - correct
        ("q15", "3x²"),   # Hard - correct
    ]
    
    for q_id, answer in test_answers:
        print(f"\n--- Answering {q_id} with '{answer}' ---")
        result = submit_answer(session['session_id'], q_id, answer)
        print(f"Correct: {result['correct']}")
        print(f"Ability: {result['old_ability']} → {result['new_ability']}")
    
    # Get summary
    print("\n" + "="*40)
    summary = get_session_summary(session['session_id'])
    print("Session Summary:")
    print(f"Total Questions: {summary['total_questions']}")
    print(f"Score: {summary['correct_answers']}/{summary['total_questions']} ({summary['score_percentage']}%)")
    print(f"Final Ability: {summary['final_ability']}")
    print(f"Topics Performance:")
    for topic, data in summary['topics_performance'].items():
        print(f"  - {topic}: {data['correct']}/{data['total']} ({data['percentage']}%)")