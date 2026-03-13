# AI-Driven Adaptive Diagnostic Engine

An intelligent GRE practice platform that adapts to student ability using Item Response Theory (IRT) and provides AI-powered study recommendations.

## Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (Atlas or local)
- OpenRouter API key (free)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/adaptive-quiz.git
cd adaptive-quiz

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your MongoDB and OpenRouter credentials

# Seed the database
python data/seed_questions.py

# Run the application
python start.py
```


## Adaptive Algorithm Logic

### The system uses a 1-Parameter Logistic IRT (Rasch) model:

**How It Works**:
- Student Ability (θ) : Starts at 0.5, ranges 0.1-1.0

- Question Difficulty (b) : Each question has difficulty 0.1-1.0

- Probability of Correct Answer:

P(correct) = 1 / (1 + e^-(θ - b))
Ability Update:

Correct answer: θ_new = θ + α(1 - P)

Wrong answer: θ_new = θ - α(P)
where α = 0.1 (learning rate)

- Next Question Selection: Choose question with difficulty closest to current ability

**Example Flow:**

Student starts: ability = 0.5
→ Gets Q1 (difficulty 0.5) → Correct → ability = 0.55
→ Gets Q2 (difficulty 0.55) → Wrong → ability = 0.52
→ Gets Q3 (difficulty 0.52) → Correct → ability = 0.56

### AI Log
**How I Used AI Tools**:
- Cursor.ai: Generated initial FastAPI boilerplate and MongoDB schemas

- ChatGPT: Helped debug IRT implementation and optimize the adaptive algorithm

- GitHub Copilot: Assisted with writing test cases and API endpoint documentation

**Challenges AI Couldn't Solve:**
- Learning Rate Tuning: Had to manually test different α values to find the right balance between stability and responsiveness

- MongoDB Connection Issues: SSL/TLS errors on Windows required manual troubleshooting and connection string modifications

- OpenAI API Migration: Had to manually update code for openai>=1.0.0 breaking changes

- OpenRouter Integration: Since OpenAI's API KEY require Paid Credid so I used this and it Required understanding of free model capabilities and prompt engineering for educational content

## API Documentation

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/start-session` | POST | Create new quiz session | `{"user_id": "optional"}` | `{"session_id": "...", "current_ability": 0.5}` |
| `/next-question/{session_id}` | GET | Get adaptive question | - | Question with options |
| `/submit-answer` | POST | Submit answer | `{"session_id": "...", "question_id": "...", "answer": "..."}` | Correctness + new ability |
| `/session-summary/{session_id}` | GET | Get performance summary | - | Topic-wise breakdown |
| `/study-plan/{session_id}` | POST | Get AI study plan | - | Personalized 3-step plan |

### Testing the API

Using Swagger UI:
- Run python start.py

- Open http://localhost:8000/docs

- Test endpoints interactively

**Sample Test Flow:**

# Start session
POST /start-session → {"session_id": "abc123"}

# Get first question
GET /next-question/abc123 → {"text": "What is 2+2?", "difficulty": 0.2}

# Submit answer
POST /submit-answer → {"correct": true, "new_ability": 0.55}

# After 10 questions, get study plan
POST /study-plan/abc123 → "Focus on Algebra and Probability..."

### Performance Considerations
- MongoDB Indexing: Created indexes on difficulty and question_id for fast queries

- IRT Optimization: Used clipping to prevent math overflow in logistic function

- Caching: Session data cached to reduce database calls

### Future Improvements

- Add user authentication

- Implement 2-parameter IRT model (discrimination parameter)

- Create React frontend

- Add more question types (quantitative, verbal)

- Deploy to cloud (Render/AWS)