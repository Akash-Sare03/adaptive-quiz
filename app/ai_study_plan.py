"""
AI-powered study plan generation using OpenRouter because 
OpenAI API key needed paid credits
"""

import os
from dotenv import load_dotenv
from openai import OpenAI  # Same OpenAI library, different base_url!
from typing import Dict

load_dotenv()

# Get OpenRouter API key from environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if OPENROUTER_API_KEY:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        default_headers={
            "HTTP-Referer": "http://localhost:8000",  
            "X-Title": "Adaptive Quiz Engine",  
        }
    )
else:
    client = None
    print("⚠️ WARNING: OPENROUTER_API_KEY not found in .env file")

def generate_study_plan(session_summary: Dict) -> str:
    """
    Generate personalized study plan using free OpenRouter models
    """
    if not OPENROUTER_API_KEY or not client:
        return get_mock_study_plan(session_summary)
    
    try:
        # Prepare the prompt
        prompt = create_study_plan_prompt(session_summary)
        
        # Use completely free model
        # can choose any of these free models:
        free_models = [
            "nvidia/nemotron-3-super-120b-a12b:free",  # Excellent for reasoning
            "stepfun-ai/step-3.5-flash:free",          # Fast and capable
            "cognitivecomputations/trinity-large-preview:free",  # Creative writing
            "qwen/qwen3-vl:free",                       # Strong general performance
            "google/gemma-3-27b:free",                  # Google's latest
            "meta-llama/llama-3.3-70b:free"             # Reliable multilingual
        ]
        
        # Using NVIDIA Nemotron (great for educational content)
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",  # 100% free!
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert GRE tutor. Create personalized, actionable study plans based on student performance data. Be encouraging and specific."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=800,  # Slightly longer for detailed plans
            top_p=0.95,
        )
        
        # Extract the study plan (same OpenAI response format!)
        study_plan = response.choices[0].message.content
        
        return study_plan
        
    except Exception as e:
        print(f"❌ Error generating study plan with OpenRouter: {e}")
        # Fall back to mock plan if API fails
        return get_mock_study_plan(session_summary)

def create_study_plan_prompt(summary: Dict) -> str:
    """
    Create a detailed prompt for the AI based on session summary
    """
    
    # Format topics performance
    topics_text = ""
    weak_topics_list = []
    
    for topic, data in summary.get("topics_performance", {}).items():
        topics_text += f"- {topic}: {data['correct']}/{data['total']} correct ({data['percentage']}%)\n"
        if data['percentage'] < 70:
            weak_topics_list.append(topic)
    
    # Identify weak topics (below 70%)
    weak_topics = ', '.join(weak_topics_list) if weak_topics_list else 'None identified'
    
    prompt = f"""
Based on this GRE practice test performance:

📊 **Overall Performance:**
- Total Questions: {summary.get('total_questions', 0)}
- Score: {summary.get('correct_answers', 0)}/{summary.get('total_questions', 0)} ({summary.get('score_percentage', 0)}%)
- Final Ability Score: {summary.get('final_ability', 0)}/1.0
- Starting Ability: {summary.get('starting_ability', 0.5)}/1.0
- Improvement: {summary.get('ability_improvement', 0)}

📚 **Performance by Topic:**
{topics_text}

🔍 **Areas Needing Improvement:**
{weak_topics}

Please provide a personalized 3-step study plan with:

1. **Immediate Focus (Next 3 days)**: 
   - Specific topics to review first
   - Key concepts to master
   - Recommended resources (videos, articles, practice problems)

2. **Practice Strategy (Days 4-7)**:
   - How to practice effectively (question types, timing)
   - Number of practice questions per day
   - How to track progress

3. **Long-term Preparation (Week 2+)**:
   - Advanced topics to cover
   - Test-taking strategies
   - Review techniques

Make it encouraging, specific, and actionable. Format with clear sections using emojis.
"""
    
    return prompt

def get_mock_study_plan(summary: Dict) -> str:
    """
    Generate a mock study plan (fallback when API is unavailable)
    """
    # Identify weak topics
    weak_topics = []
    for topic, data in summary.get("topics_performance", {}).items():
        if data['percentage'] < 70:
            weak_topics.append(topic)
    
    if not weak_topics:
        return """
🎉 **Excellent Work!**

You've demonstrated strong performance across all topics. Here's your maintenance plan:

**📅 Immediate Focus (Next 3 days)**
- Continue practicing with challenging questions (difficulty > 0.7)
- Review any questions you found tricky
- Focus on timing: aim for < 1.5 min per question

**🎯 Practice Strategy (Days 4-7)**
- Take one full-length practice section daily
- Analyze mistakes thoroughly
- Create flashcards for any concepts you need to review

**🚀 Long-term Preparation**
- Teach concepts to others (best way to solidify knowledge)
- Explore advanced problem variations
- Take full-length practice tests weekly

**💡 Quick Tip:** Keep a log of your mistakes and review them weekly!
"""
    else:
        topics_list = ", ".join(weak_topics)
        return f"""
📚 **Personalized Study Plan**

Based on your performance, focus on: **{topics_list}**

**📅 Step 1: Foundation (Days 1-3)**
- Review core concepts in {weak_topics[0] if weak_topics else 'your weak areas'}
- Watch Khan Academy videos on these topics
- Work through 10-15 basic problems daily

**🎯 Step 2: Practice (Days 4-7)**
- Solve 20-25 mixed difficulty problems daily
- Time yourself: start with 2 min/question, reduce to 1.5 min
- Focus especially on {weak_topics[1] if len(weak_topics) > 1 else weak_topics[0]}

**🚀 Step 3: Mastery (Week 2+)**
- Attempt hardest questions in your weak areas
- Review explanations thoroughly, even for correct answers
- Take one full practice test and analyze mistakes

**💡 Quick Tip:** Create flashcards for formulas you frequently forget!
"""

# Test the function
if __name__ == "__main__":
    # Create a mock summary for testing
    mock_summary = {
        "total_questions": 10,
        "correct_answers": 7,
        "score_percentage": 70,
        "final_ability": 0.65,
        "starting_ability": 0.5,
        "ability_improvement": 0.15,
        "topics_performance": {
            "Algebra": {"correct": 3, "total": 3, "percentage": 100},
            "Geometry": {"correct": 1, "total": 2, "percentage": 50},
            "Probability": {"correct": 1, "total": 2, "percentage": 50},
            "Calculus": {"correct": 2, "total": 3, "percentage": 66.7}
        }
    }
    
    print("🧪 Testing OpenRouter Study Plan Generator\n")
    
    if OPENROUTER_API_KEY:
        print("✅ Using OpenRouter API with free models...")
        print("   Model: nvidia/nemotron-3-super-120b-a12b:free\n")
        plan = generate_study_plan(mock_summary)
    else:
        print("⚠️ No API key found, using mock plan...\n")
        plan = get_mock_study_plan(mock_summary)
    
    print("="*60)
    print(plan)
    print("="*60)