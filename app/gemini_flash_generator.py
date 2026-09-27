import os
from dotenv import load_dotenv

load_dotenv()

def generate_nutrition_tip_with_flash(goal: str) -> str:
    """
    Generate a concise nutrition or recovery tip using Gemini Flash based on the user's fitness goal.
    Args:
        goal (str): User's fitness goal - "weight loss", "muscle gain", or "general fitness".
    Returns:
        str: Generated tip.
    """
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    if api_key and api_key != "your_gemini_api_key_here":
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. The tip should be practical, friendly, and easy to understand."
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini Flash API call failed: {e}. Using fallback tip.")

    # High quality fallbacks tailored to goals
    goal_lower = goal.lower()
    if "muscle" in goal_lower or "gain" in goal_lower or "strength" in goal_lower:
        return "Prioritize protein! Aim for 1.6 to 2.2 grams of protein per kilogram of body weight daily (chicken, fish, eggs, tofu, Greek yogurt). Include a post-workout meal with protein and complex carbs within 45 minutes to optimize muscle recovery and synthesis."
    elif "weight" in goal_lower or "fat" in goal_lower or "loss" in goal_lower or "slim" in goal_lower:
        return "Maintain a moderate calorie deficit and focus on high-fiber, protein-rich foods. Drink at least 3-4 liters of water daily, especially before meals, to stay hydrated, boost metabolic rate, and improve satiety throughout the day."
    else:
        return "Focus on balanced whole food nutrition with a 40/30/30 ratio of complex carbs, clean protein, and healthy fats. Stay consistently hydrated and aim for 7-8 hours of quality sleep each night for peak physical recovery."
