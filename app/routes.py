import os
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.schemas import UserInput, FeedbackRequest, WorkoutRequest
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan
from app.database import (
    save_user,
    save_plan,
    update_plan,
    get_original_plan,
    get_workout_plan,
    get_user,
    get_all_users,
    get_all_plans,
    delete_user
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

router = APIRouter()

# ---------------------------------------------------------
# HTML Template Web Routes
# ---------------------------------------------------------

@router.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    """
    Renders the homepage form (index.html)
    """
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout_web(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    """
    Processes form input, generates workout plan and nutrition tip,
    stores user info and plan in SQLite DB, and renders result.html.
    """
    user_input_dict = {
        "goal": goal,
        "intensity": intensity
    }

    # Generate AI Workout Plan and Nutrition Tip
    workout_plan = generate_workout_gemini(user_input_dict)
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    # Save to SQLite Database
    save_user(
        user_id=user_id,
        name=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )
    save_plan(user_id=user_id, plan=workout_plan)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "updated_plan": None,
            "nutrition_tip": nutrition_tip,
            "success_message": None
        }
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback_web(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):
    """
    Processes feedback form submission, retrieves original plan,
    generates updated workout plan via Gemini, updates DB, and renders result.html.
    """
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please generate a plan first.")

    original_plan = get_original_plan(user_id)
    if not original_plan:
        raise HTTPException(status_code=404, detail="Original workout plan not found for this user.")

    # Generate updated plan via Gemini 1.5 Pro
    revised_plan = update_workout_plan(original_plan, feedback)

    # Update plan in SQLite database
    update_plan(user_id=user_id, updated_text=revised_plan)

    # Generate tip based on goal
    nutrition_tip = generate_nutrition_tip_with_flash(user.goal)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": user.name,
            "user_id": user.id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": original_plan,
            "updated_plan": revised_plan,
            "nutrition_tip": nutrition_tip,
            "success_message": "Your plan has been updated based on your feedback!"
        }
    )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    """
    Admin View: Displays a list of all registered users and their original/updated workout plans.
    """
    users = get_all_users()
    plans_map = get_all_plans()

    user_data = []
    for u in users:
        plan_obj = plans_map.get(u.id)
        orig = plan_obj.original_plan if plan_obj and plan_obj.original_plan else "N/A"
        upd = plan_obj.updated_plan if plan_obj and plan_obj.updated_plan else "Not updated"

        user_data.append({
            "id": u.id,
            "name": u.name,
            "age": u.age,
            "weight": u.weight,
            "goal": u.goal,
            "intensity": u.intensity,
            "original_plan": orig,
            "updated_plan": upd
        })

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": user_data
        }
    )


@router.post("/delete-user/{user_id}")
def delete_user_route(user_id: int):
    """
    Admin route to delete a user by ID.
    """
    delete_user(user_id)
    return RedirectResponse(url="/view-all-users", status_code=303)


# ---------------------------------------------------------
# API Endpoints (as per Page 13 & 14 documentation)
# ---------------------------------------------------------

@router.post("/generate-workout/gemini")
async def generate_gemini_workout(request: WorkoutRequest):
    """
    API 1: Generate workout plan using Gemini Pro
    """
    try:
        result = generate_workout_gemini({"goal": request.goal, "intensity": request.intensity})
        return {"model": "gemini-pro", "workout_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nutrition-tip")
def get_flash_tip(goal: str):
    """
    API 2: Generate nutrition tip using Gemini Flash
    """
    tip = generate_nutrition_tip_with_flash(goal)
    return {"goal": goal, "nutrition_tip": tip}


@router.post("/generate-plan")
def generate_plan_api(user_data: UserInput):
    """
    API 3: Save user info & generate plan
    """
    try:
        save_user(
            user_id=user_data.user_id,
            name=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )
        plan = generate_workout_gemini({"goal": user_data.goal, "intensity": user_data.intensity})
        save_plan(user_data.user_id, plan)
        return {
            "message": "Workout plan generated and saved successfully!",
            "workout_plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


@router.post("/update-plan/{user_id}")
def update_user_plan_api(user_id: int, data: FeedbackRequest):
    """
    API 4: Update workout plan based on user feedback
    """
    original = get_original_plan(user_id)
    if not original:
        return {"error": "Original plan not found for this user."}

    updated = update_workout_plan(original, data.feedback)
    update_plan(user_id, updated)
    return {"updated_plan": updated}
