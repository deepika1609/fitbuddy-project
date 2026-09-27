import os
from dotenv import load_dotenv

load_dotenv()

# Function to generate workout plan using Gemini 1.5 Pro
def generate_workout_gemini(user_input: dict) -> str:
    """
    Implements the core logic to generate a personalized 7-day workout plan using user inputs
    such as goal (e.g. muscle gain, weight loss) and intensity (low, medium, high).
    Uses Gemini 1.5 Pro or intelligent fallback if API key is not configured.
    """
    goal = user_input.get("goal", "General Fitness")
    intensity = user_input.get("intensity", "Medium")
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    if api_key and api_key != "your_gemini_api_key_here":
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-pro")
            
            prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of **{goal}**, and prefers **{intensity}** intensity workouts.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...

(Repeat for Day 2-7)

Include a brief summary and important safety/nutrition notes at the end.
"""
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini API call failed: {e}. Using fallback generator.")

    # High quality dynamic fallback workout plan generator
    return _generate_fallback_workout(goal, intensity)

def _generate_fallback_workout(goal: str, intensity: str) -> str:
    intensity_caps = intensity.capitalize()
    return f"""## 7-Day {intensity_caps}-Intensity Workout Plan for {goal.title()}

This plan focuses on structured exercises to maximize results for {goal.lower()} while matching your {intensity_caps} intensity preference. Remember to stay hydrated and listen to your body.

**Day 1: Upper Body Strength & Focus**
* **Warm-up (5-10 mins):** Jumping jacks (60s), high knees (30s), arm circles (forward & backward, 30s each), dynamic torso twists (1 min).
* **Main Workout:**
  - Barbell / Dumbbell Bench Press: 3 sets of 8-12 reps
  - Pull-ups or Lat Pulldowns: 3 sets of 8-12 reps
  - Overhead Dumbbell Press: 3 sets of 8-12 reps
  - Dumbbell Rows: 3 sets of 8-12 reps per arm
  - Dumbbell Bicep Curls: 3 sets of 10-15 reps
  - Triceps Pushdowns or Dips: 3 sets of 10-15 reps
* **Cooldown:** Static chest and arm stretches holding each stretch for 30 seconds.

**Day 2: Lower Body & Core**
* **Warm-up (5-10 mins):** Bodyweight squats (15 reps), lunges (10 reps per leg), glute bridges (15 reps), light leg swings.
* **Main Workout:**
  - Barbell / Goblet Squats: 3 sets of 8-12 reps
  - Romanian Deadlifts: 3 sets of 10-15 reps
  - Walking Lunges: 3 sets of 12-15 reps per leg
  - Leg Press or Bulgarian Split Squats: 3 sets of 10 reps per leg
  - Hanging Leg Raises or Knees-to-Chest: 3 sets to near failure
  - Russian Twists: 3 sets of 15 reps per side
* **Cooldown:** Static stretches for quads, hamstrings, and glutes (30 seconds each).

**Day 3: HIIT Cardio & Active Core**
* **Warm-up (5 mins):** Light cardio, arm swings, dynamic hip openers.
* **Main Workout:**
  - Burpees: 3 sets of 10-15 reps
  - Mountain Climbers: 3 sets of 30-45 seconds
  - Jump Squats: 3 sets of 10-15 reps
  - Plank Variations (High plank, forearm plank, side plank): 30-60 seconds each, repeat 2-3 times
  - Kettlebell or Dumbbell Swings: 3 sets of 15-20 reps
* **Cooldown:** Light cardio cooldown (5 mins), static stretching for core and legs.

**Day 4: Rest & Active Recovery**
* **Active Recovery:** Light 30-minute walk, foam rolling, swimming, or mild yoga. Focus on mobility and muscle relaxation to allow optimal recovery.

**Day 5: Upper Body Hypertrophy & Pump**
* **Warm-up (5 mins):** Similar to Day 1 dynamic warm-up.
* **Main Workout:**
  - Incline Dumbbell Press: 3 sets of 8-12 reps
  - Seated Cable Rows / Close-Grip Pulldowns: 3 sets of 8-12 reps
  - Arnold Press: 3 sets of 8-12 reps
  - Lateral Raises: 3 sets of 12-15 reps
  - Hammer Curls: 3 sets of 10-15 reps
  - Overhead Triceps Extension: 3 sets of 10-15 reps
* **Cooldown:** Upper body stretch focusing on shoulders, chest, and lats.

**Day 6: Lower Body & Core Focus**
* **Warm-up (5 mins):** Bodyweight squats, high knees, leg swings.
* **Main Workout:**
  - Front Squats or Leg Press: 3 sets of 8-12 reps
  - Good Mornings / Hamstring Curls: 3 sets of 10-15 reps
  - Bulgarian Split Squats: 3 sets of 10-12 reps per leg
  - Calf Raises: 4 sets of 15-20 reps
  - Cable Crunches or Ab Wheel Rollouts: 3 sets of 12-15 reps
* **Cooldown:** Lower body stretching and foam rolling.

**Day 7: Full Body Mobility & Rest**
* **Active Recovery:** 20-30 minutes of deep yoga stretching, focusing on hips, spine, and hamstrings to prepare for the upcoming week.

**Important Notes:**
* **Progressive Overload:** Gradually increase weight, reps, or control each week to ensure continued growth.
* **Proper Form:** Prioritize clean execution over heavy weights to prevent injury.
* **Hydration & Nutrition:** Drink plenty of water throughout the day and fuel your body with protein and healthy nutrients.
"""
