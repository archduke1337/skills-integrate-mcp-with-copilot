from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory activities data
activities = {
    "Chess Club": {
        "description": "Play chess and improve your skills.",
        "schedule": "Mondays 3:30-4:30pm",
        "max_participants": 20,
        "participants": []
    },
    "Programming Class": {
        "description": "Learn Python and build cool projects.",
        "schedule": "Wednesdays 4:00-5:00pm",
        "max_participants": 25,
        "participants": []
    },
    "Gym Class": {
        "description": "Stay fit and healthy with group workouts.",
        "schedule": "Fridays 2:00-3:00pm",
        "max_participants": 30,
        "participants": []
    },
    "GitHub Skills": {
        "description": "Learn practical coding and collaboration skills with GitHub. Part of the GitHub Certifications program.",
        "schedule": "Fridays 3:30-4:30pm",
        "max_participants": 30,
        "participants": []
    }
}

@app.get("/activities")
def get_activities():
    return activities

@app.post("/activities/{activity_name}/signup")
def signup(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email in activity["participants"]:
        return JSONResponse(status_code=400, content={"detail": "Already registered"})
    if len(activity["participants"]) >= activity["max_participants"]:
        return JSONResponse(status_code=400, content={"detail": "No spots left"})
    activity["participants"].append(email)
    return {"message": f"Signed up for {activity_name}"}

@app.delete("/activities/{activity_name}/unregister")
def unregister(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email not in activity["participants"]:
        return JSONResponse(status_code=400, content={"detail": "Not registered"})
    activity["participants"].remove(email)
    return {"message": f"Unregistered from {activity_name}"}
