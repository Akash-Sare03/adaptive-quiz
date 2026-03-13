"""
Item Response Theory (IRT) implementation for adaptive testing
Uses 1-Parameter Logistic Model (Rasch Model)
"""

import math

def calculate_new_ability(current_ability: float, question_difficulty: float, was_correct: bool) -> float:
    """
    Update student's ability score based on their answer
    
    Args:
        current_ability: Current ability score (0.1 to 1.0)
        question_difficulty: Difficulty of answered question (0.1 to 1.0)
        was_correct: Whether student answered correctly
    
    Returns:
        New ability score (0.1 to 1.0)
    """
    # Learning rate - how fast ability changes (smaller = more stable)
    LEARNING_RATE = 0.1
    
    # Calculate probability of correct answer given current ability
    # Using logistic function: P(correct) = 1 / (1 + e^-(ability - difficulty))
    try:
        # Theta = ability - difficulty
        theta = current_ability - question_difficulty
        
        # Clip theta to avoid overflow in exp()
        theta = max(-10, min(10, theta))
        
        # Probability of getting this question correct
        p_correct = 1 / (1 + math.exp(-theta))
        
        # Update ability based on actual vs expected performance
        if was_correct:
            # If correct, ability increases more if it was unexpected (low p_correct)
            new_ability = current_ability + LEARNING_RATE * (1 - p_correct)
        else:
            # If wrong, ability decreases more if it was unexpected (high p_correct)
            new_ability = current_ability - LEARNING_RATE * p_correct
        
        # Keep ability within bounds (0.1 to 1.0)
        new_ability = max(0.1, min(1.0, new_ability))
        
        return round(new_ability, 3)
        
    except Exception as e:
        print(f"Error in ability calculation: {e}")
        return current_ability


def calculate_question_difficulty(ability: float, p_correct: float = 0.5) -> float:
    """
    Calculate ideal question difficulty for given ability
    For p_correct = 0.5, difficulty should equal ability
    
    Args:
        ability: Student's current ability
        p_correct: Desired probability of correct answer (default 0.5)
    
    Returns:
        Ideal difficulty score
    """
    # For 1PL model, difficulty = ability when p_correct = 0.5
    if p_correct == 0.5:
        return ability
    
    # Adjust difficulty based on desired probability
    # This is a simplified version
    log_odds = math.log(p_correct / (1 - p_correct))
    return ability - log_odds


def get_difficulty_range(current_ability: float) -> tuple:
    """
    Get acceptable difficulty range for next question
    
    Args:
        current_ability: Student's current ability
    
    Returns:
        (min_difficulty, max_difficulty) tuple
    """
    # Allow questions within ±0.2 of current ability
    min_diff = max(0.1, current_ability - 0.2)
    max_diff = min(1.0, current_ability + 0.2)
    
    return (round(min_diff, 2), round(max_diff, 2))


def estimate_starting_ability() -> float:
    """
    Get starting ability for new student
    """
    return 0.5  # Start at medium difficulty


def is_quiz_complete(questions_answered: list, min_questions: int = 5) -> bool:
    """
    Check if quiz should end
    
    Args:
        questions_answered: List of answered questions
        min_questions: Minimum questions required
    
    Returns:
        True if quiz should end
    """
    if len(questions_answered) < min_questions:
        return False
    
    # Optional: End if ability stabilizes (changes less than 0.05 for last 3 questions)
    if len(questions_answered) >= 3:
        last_3 = questions_answered[-3:]
        abilities = [q.get('ability_after', 0) for q in last_3]
        if len(abilities) == 3:
            max_change = max(abilities) - min(abilities)
            if max_change < 0.05:
                return True
    
    # End after 10 questions max
    return len(questions_answered) >= 10


# Test the algorithm
if __name__ == "__main__":
    print("Testing IRT Algorithm\n")
    
    # Test 1: Correct answer increases ability
    ability = 0.5
    new_ability = calculate_new_ability(ability, 0.5, True)
    print(f"Correct answer on difficulty 0.5: {ability} → {new_ability}")
    
    # Test 2: Wrong answer decreases ability
    ability = 0.5
    new_ability = calculate_new_ability(ability, 0.5, False)
    print(f"Wrong answer on difficulty 0.5: {ability} → {new_ability}")
    
    # Test 3: Correct on hard question increases more
    ability = 0.5
    new_ability = calculate_new_ability(ability, 0.8, True)
    print(f"Correct on hard (0.8): {ability} → {new_ability}")
    
    # Test 4: Wrong on easy question decreases more
    ability = 0.5
    new_ability = calculate_new_ability(ability, 0.2, False)
    print(f"Wrong on easy (0.2): {ability} → {new_ability}")
    
    # Test 5: Difficulty range
    ability = 0.6
    min_d, max_d = get_difficulty_range(ability)
    print(f"\nFor ability {ability}, next question difficulty should be between {min_d} and {max_d}")