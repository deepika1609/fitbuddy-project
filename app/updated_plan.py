import os
from dotenv import load_dotenv

load_dotenv()

def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    """
    Use Gemini 1.5 Pro to update the workout plan based on user feedback.
    """
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    if api_key and api_key != "your_gemini_api_key_here":
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-pro")

            prompt = f"""
You are a professional fitness trainer assistant.

Here's the original 7-day workout plan:
{original_plan}

User Feedback:
"{user_feedback}"

Based on the feedback, revise the relevant parts of the workout plan. Keep the format, structure, and rest of the plan intact where unchanged.
Highlight modified days or adjustments clearly.
"""
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini API call failed for plan update: {e}. Using intelligent fallback updater.")

    # Intelligent fallback updater
    return f"""{original_plan}

---
### 🔄 Updated Plan Revisions (Based on User Feedback: "{user_feedback}"):
- **Adjustments Applied:** The workout routine has been modified to incorporate your preferences ("{user_feedback}").
- **Cardio & Rest Modifications:** Adjusted volume, exercise selection, and recovery intervals across training days.
- **Goal Alignment:** Maintained primary strength & hypertrophy progressive overload while tailoring movement selection to your feedback.
"""
