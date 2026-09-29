from pathlib import Path
import json,joblib,pandas as pd
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from fastapi.responses import FileResponse
from .db import init_db,list_projects,create_project,create_activity,get_activity,update_progress

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/"artifacts"
UI=ROOT/"ui"
app=FastAPI(title="Engineering Project Progress")

class ProjectIn(BaseModel):
    name:str
    budget:float=Field(gt=0)

class ActivityIn(BaseModel):
    name:str
    planned_days:int=Field(gt=0)
    progress:float=Field(ge=0,le=1)
    risk_signal:float

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/health")
def health():
    return {"status":"ok"}

@app.get("/api/metrics")
def metrics():
    p=ART/"metrics.json"
    return json.loads(p.read_text()) if p.exists() else {}

@app.get("/api/projects")
def projects():
    return list_projects()

@app.post("/api/projects")
def add_project(x:ProjectIn):
    return {"id":create_project(x.name,x.budget)}

@app.post("/api/projects/{pid}/activities")
def add_activity(pid:int,x:ActivityIn):
    return {"id":create_activity(pid,x.name,x.planned_days,x.progress,x.risk_signal)}

@app.put("/api/activities/{aid}/progress")
def progress(aid:int,value:float):
    if not 0<=value<=1:
        raise HTTPException(422,"Progress must be between 0 and 1")
    if not get_activity(aid):
        raise HTTPException(404,"Activity not found")
    update_progress(aid,value)
    return {"updated":True}

@app.post("/api/activities/{aid}/delay-risk")
def delay_risk(aid:int):
    a=get_activity(aid)
    if not a:
        raise HTTPException(404,"Activity not found")
    model=joblib.load(ART/"delay_model.joblib")
    X=pd.DataFrame([{"planned_days":a["planned_days"],"progress":a["progress"],"risk_signal":a["risk_signal"]}])
    p=float(model.predict_proba(X)[:,1][0])
    return {"activity_id":aid,"delay_probability":p,"delay_percent":round(p*100,2),"risk_level":"high" if p>=.5 else ("medium" if p>=.25 else "low")}

@app.get("/")
def root():
    return FileResponse(UI/"index.html")
