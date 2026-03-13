import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import questions_collection
from datetime import datetime

# Sample GRE-style questions
questions = [
    # Easy questions (difficulty 0.2-0.4)
    {
        "question_id": "q1",
        "text": "If x + 5 = 10, what is the value of x?",
        "difficulty": 0.2,
        "topic": "Algebra",
        "tags": ["linear equations", "basic"],
        "options": ["3", "5", "7", "10"],
        "correct_answer": "5",
        "explanation": "Subtract 5 from both sides: x = 5"
    },
    {
        "question_id": "q2",
        "text": "What is the square root of 144?",
        "difficulty": 0.25,
        "topic": "Arithmetic",
        "tags": ["square roots", "basic"],
        "options": ["10", "11", "12", "13"],
        "correct_answer": "12",
        "explanation": "12 × 12 = 144"
    },
    {
        "question_id": "q3",
        "text": "If a triangle has angles 45° and 45°, what is the third angle?",
        "difficulty": 0.3,
        "topic": "Geometry",
        "tags": ["triangles", "angles"],
        "options": ["45°", "60°", "90°", "100°"],
        "correct_answer": "90°",
        "explanation": "Sum of angles in triangle = 180°, so 180 - 45 - 45 = 90°"
    },
    {
        "question_id": "q4",
        "text": "What is 25% of 80?",
        "difficulty": 0.3,
        "topic": "Percentages",
        "tags": ["percentages", "basic"],
        "options": ["20", "25", "30", "40"],
        "correct_answer": "20",
        "explanation": "25% = 1/4, so 80 ÷ 4 = 20"
    },
    {
        "question_id": "q5",
        "text": "If 2x + 3 = 9, what is x?",
        "difficulty": 0.35,
        "topic": "Algebra",
        "tags": ["linear equations"],
        "options": ["2", "3", "4", "6"],
        "correct_answer": "3",
        "explanation": "2x = 6, so x = 3"
    },
    
    # Medium questions (difficulty 0.5-0.7)
    {
        "question_id": "q6",
        "text": "If the average of 5, 10, and x is 10, what is x?",
        "difficulty": 0.5,
        "topic": "Statistics",
        "tags": ["averages"],
        "options": ["10", "15", "20", "25"],
        "correct_answer": "15",
        "explanation": "(5 + 10 + x)/3 = 10, so 15 + x = 30, x = 15"
    },
    {
        "question_id": "q7",
        "text": "What is the probability of rolling a sum of 7 with two dice?",
        "difficulty": 0.6,
        "topic": "Probability",
        "tags": ["probability", "dice"],
        "options": ["1/6", "1/8", "1/12", "1/36"],
        "correct_answer": "1/6",
        "explanation": "6 combinations sum to 7 out of 36 total: 1/6"
    },
    {
        "question_id": "q8",
        "text": "If log₂x = 3, what is x?",
        "difficulty": 0.65,
        "topic": "Logarithms",
        "tags": ["logs"],
        "options": ["3", "6", "8", "9"],
        "correct_answer": "8",
        "explanation": "2³ = 8"
    },
    {
        "question_id": "q9",
        "text": "The sum of three consecutive integers is 72. What is the largest?",
        "difficulty": 0.6,
        "topic": "Algebra",
        "tags": ["consecutive numbers"],
        "options": ["23", "24", "25", "26"],
        "correct_answer": "25",
        "explanation": "x + (x+1) + (x+2) = 72, 3x + 3 = 72, x = 23, largest = 25"
    },
    {
        "question_id": "q10",
        "text": "A rectangle has length 8 and width 6. What is the diagonal?",
        "difficulty": 0.55,
        "topic": "Geometry",
        "tags": ["pythagorean theorem"],
        "options": ["8", "10", "12", "14"],
        "correct_answer": "10",
        "explanation": "√(8² + 6²) = √(64 + 36) = √100 = 10"
    },
    
    # Hard questions (difficulty 0.8-1.0)
    {
        "question_id": "q11",
        "text": "How many different 3-digit numbers can be formed using digits 1,2,3,4 without repetition?",
        "difficulty": 0.8,
        "topic": "Permutations",
        "tags": ["counting"],
        "options": ["12", "24", "36", "48"],
        "correct_answer": "24",
        "explanation": "4 × 3 × 2 = 24"
    },
    {
        "question_id": "q12",
        "text": "If f(x) = 2x² - 3x + 1, what is f(2)?",
        "difficulty": 0.75,
        "topic": "Functions",
        "tags": ["evaluation"],
        "options": ["3", "5", "7", "9"],
        "correct_answer": "3",
        "explanation": "2(4) - 6 + 1 = 8 - 6 + 1 = 3"
    },
    {
        "question_id": "q13",
        "text": "What is the sum of all angles in a pentagon?",
        "difficulty": 0.8,
        "topic": "Geometry",
        "tags": ["polygons"],
        "options": ["360°", "450°", "540°", "720°"],
        "correct_answer": "540°",
        "explanation": "(n-2) × 180° = 3 × 180° = 540°"
    },
    {
        "question_id": "q14",
        "text": "If 3ˣ = 81, what is x?",
        "difficulty": 0.7,
        "topic": "Exponents",
        "tags": ["exponential"],
        "options": ["2", "3", "4", "5"],
        "correct_answer": "4",
        "explanation": "3⁴ = 81"
    },
    {
        "question_id": "q15",
        "text": "What is the derivative of x³?",
        "difficulty": 0.9,
        "topic": "Calculus",
        "tags": ["derivatives"],
        "options": ["x²", "3x²", "x³", "3x"],
        "correct_answer": "3x²",
        "explanation": "Power rule: bring down exponent and reduce by 1"
    },
    {
        "question_id": "q16",
        "text": "How many ways can 5 people sit in a row?",
        "difficulty": 0.8,
        "topic": "Permutations",
        "tags": ["factorial"],
        "options": ["25", "60", "120", "240"],
        "correct_answer": "120",
        "explanation": "5! = 5 × 4 × 3 × 2 × 1 = 120"
    },
    {
        "question_id": "q17",
        "text": "What is the area of a circle with radius 7?",
        "difficulty": 0.7,
        "topic": "Geometry",
        "tags": ["circles"],
        "options": ["49π", "14π", "7π", "49"],
        "correct_answer": "49π",
        "explanation": "Area = πr² = 49π"
    },
    {
        "question_id": "q18",
        "text": "If sin θ = 1/2, what is θ in degrees (0° to 90°)?",
        "difficulty": 0.85,
        "topic": "Trigonometry",
        "tags": ["sine"],
        "options": ["30°", "45°", "60°", "90°"],
        "correct_answer": "30°",
        "explanation": "sin 30° = 1/2"
    },
    {
        "question_id": "q19",
        "text": "What is the value of 7! / 5! ?",
        "difficulty": 0.75,
        "topic": "Factorials",
        "tags": ["simplification"],
        "options": ["42", "35", "30", "25"],
        "correct_answer": "42",
        "explanation": "7! / 5! = (7 × 6 × 5!)/5! = 7 × 6 = 42"
    },
    {
        "question_id": "q20",
        "text": "If 2x - y = 7 and x + y = 5, what is x?",
        "difficulty": 0.8,
        "topic": "Algebra",
        "tags": ["system of equations"],
        "options": ["2", "3", "4", "5"],
        "correct_answer": "4",
        "explanation": "Add equations: 3x = 12, x = 4"
    },
    {
        "question_id": "q21",
        "text": "What is the distance between points (1,2) and (4,6)?",
        "difficulty": 0.7,
        "topic": "Coordinate Geometry",
        "tags": ["distance formula"],
        "options": ["3", "4", "5", "6"],
        "correct_answer": "5",
        "explanation": "√[(4-1)² + (6-2)²] = √(9 + 16) = √25 = 5"
    },
    {
        "question_id": "q22",
        "text": "If a number is divisible by both 4 and 6, it must be divisible by?",
        "difficulty": 0.65,
        "topic": "Number Theory",
        "tags": ["LCM"],
        "options": ["8", "12", "18", "24"],
        "correct_answer": "12",
        "explanation": "LCM of 4 and 6 is 12"
    }
]

def seed_database():
    # Clear existing questions
    questions_collection.delete_many({})
    
    # Insert new questions
    result = questions_collection.insert_many(questions)
    
    print(f"Added {len(result.inserted_ids)} questions to database!")
    print("\nSample questions by difficulty:")
    
    # Show count by difficulty range
    easy = questions_collection.count_documents({"difficulty": {"$lt": 0.4}})
    medium = questions_collection.count_documents({"difficulty": {"$gte": 0.4, "$lte": 0.7}})
    hard = questions_collection.count_documents({"difficulty": {"$gt": 0.7}})
    
    print(f"Easy (0.1-0.4): {easy}")
    print(f"Medium (0.4-0.7): {medium}")
    print(f"Hard (0.7-1.0): {hard}")

if __name__ == "__main__":
    seed_database()