from app.gemini_flash_generator import generate_nutrition_tip_with_flash

def get_nutrition_guidance(goal: str) -> dict:
    """
    Helper module for nutrition guidance and tip handling.
    """
    tip = generate_nutrition_tip_with_flash(goal)
    return {
        "goal": goal,
        "nutrition_tip": tip
    }
