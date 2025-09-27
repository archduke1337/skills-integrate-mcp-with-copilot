from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Dict, List
import uvicorn

app = FastAPI(title="Mergington High School Activities API")

# Sample activities data - using meaningful identifiers as mentioned in README
activities_data: Dict[str, Dict] = {
    "Chess Club": {
        "description": "Learn strategic thinking and compete in tournaments with fellow chess enthusiasts.",
        "schedule": "Tuesdays and Thursdays, 3:30-5:00 PM",
        "max_participants": 20,
        "participants": ["alice.student@mergington.edu", "bob.learner@mergington.edu"]
    },
    "Programming Class": {
        "description": "Introduction to Python programming and computer science fundamentals.",
        "schedule": "Mondays, Wednesdays, and Fridays, 4:00-5:30 PM",
        "max_participants": 15,
        "participants": ["charlie.coder@mergington.edu", "diana.dev@mergington.edu", "eve.engineer@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical fitness activities, team sports, and wellness education.",
        "schedule": "Daily, 2:00-3:00 PM",
        "max_participants": 30,
        "participants": ["frank.fitness@mergington.edu", "grace.gym@mergington.edu", "henry.health@mergington.edu", "iris.active@mergington.edu"]
    },
    "Drama Club": {
        "description": "Explore theater arts, acting, and stage production with creative peers.",
        "schedule": "Mondays and Wednesdays, 3:00-5:00 PM",
        "max_participants": 25,
        "participants": []
    },
    "Science Fair": {
        "description": "Prepare and present innovative science projects in annual competition.",
        "schedule": "Thursdays, 3:30-5:00 PM",
        "max_participants": 12,
        "participants": ["jack.scientist@mergington.edu"]
    },
    "GitHub Skills": {
        "description": "Learn practical coding and collaboration skills through GitHub's interactive learning platform. First part of the GitHub Certifications program to help with college applications.",
        "schedule": "Fridays, 3:30-5:00 PM",
        "max_participants": 20,
        "participants": []
    }
}

@app.get("/activities")
async def get_activities():
    """Get all activities with their details and current participant count"""
    return activities_data

@app.post("/activities/{activity_name}/signup")
async def signup_for_activity(activity_name: str, email: str = Query(...)):
    """Sign up for an activity"""
    if activity_name not in activities_data:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity = activities_data[activity_name]
    
    # Check if already registered
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already registered for this activity")
    
    # Check if activity is full
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
    
    # Add student to activity
    activity["participants"].append(email)
    
    return {
        "message": f"Successfully signed up for {activity_name}",
        "activity": activity_name,
        "email": email
    }

@app.delete("/activities/{activity_name}/unregister")
async def unregister_from_activity(activity_name: str, email: str = Query(...)):
    """Remove student from an activity"""
    if activity_name not in activities_data:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity = activities_data[activity_name]
    
    # Check if student is registered
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is not registered for this activity")
    
    # Remove student from activity
    activity["participants"].remove(email)
    
    return {
        "message": f"Successfully unregistered from {activity_name}",
        "activity": activity_name,
        "email": email
    }

# Mount static files
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)