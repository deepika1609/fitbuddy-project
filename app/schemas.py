from pydantic import BaseModel, Field
from typing import Optional

class UserInput(BaseModel):
    username: str = Field(..., alias="name")
    user_id: int
    age: int
    weight: float
    goal: str
    intensity: str

    class Config:
        populate_by_name = True

class FeedbackRequest(BaseModel):
    user_id: int
    feedback: str

class WorkoutRequest(BaseModel):
    goal: str
    intensity: str

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    weight: float
    goal: str
    intensity: str
    original_plan: Optional[str] = "N/A"
    updated_plan: Optional[str] = "Not updated"
