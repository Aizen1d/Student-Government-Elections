from fastapi import FastAPI, HTTPException, Depends, APIRouter, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from database import engine, SessionLocal

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi.responses import JSONResponse

from dotenv import load_dotenv # for .env file
load_dotenv()

import time
import os
import requests

from models import Student, Announcement, Rule, Guideline

#################################################################
""" Settings """

tags_metadata = [
    {
        "name": "Student",
        "description": "Manage students.",
    },
    {
        "name": "Announcement",
        "description": "Manage announcements.",
    },
    {
        "name": "Rule",
        "description": "Manage rules.",
    },
    {
        "name": "Guideline",
        "description": "Manage guidelines.",
    },
]

app = FastAPI(
    title="API for Student Goverment Election",
    description="This is the API for the Student Government Election",
    version="v1",
    docs_url="/",
    redoc_url="/redoc",
    openapi_tags=tags_metadata
)

router = APIRouter(prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8000', 'http://127.0.0.1:8000'], # Must change to appropriate frontend URL (local or production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

# Store the expiration time and access token
EXPIRES_AT = 0
ACCESS_TOKEN = ""

def get_access_token():
    global REFRESH_TOKEN
    global EXPIRES_AT
    global ACCESS_TOKEN

    # Check if the access token is expired or near to expire
    if time.time() > EXPIRES_AT - 60:  # refresh 60 seconds early
        token_url = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"

        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
            "grant_type": "refresh_token",
            "scope": "files.readwrite offline_access",
        }

        response = requests.post(token_url, data=payload)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get access token")

        # Update the stored refresh token and expiration time with the new ones
        REFRESH_TOKEN = response.json()["refresh_token"]
        EXPIRES_AT = time.time() + response.json()["expires_in"]
        ACCESS_TOKEN = response.json()["access_token"]

    return ACCESS_TOKEN, REFRESH_TOKEN


#################################################################
""" All about students APIs """

""" ** GET Methods: All about students APIs ** """

@router.get("/student/all", tags=["Student"])
def get_All_Students(db: Session = Depends(get_db)):
    try:
        students = db.query(Student).all()
        return {"students": [student.to_dict() for student in students]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all students from the database"})
    
#################################################################
""" Announcement Table APIs """

class AnnouncementSaveData(BaseModel):
    type: str
    title: str
    body: str
    attachment_type: str
    attachment_image: str

""" ** GET Methods: Announcement Table APIs ** """

@router.get("/announcement/all", tags=["Announcement"])
def get_All_Announcement(db: Session = Depends(get_db)):
    try:
        announcements = db.query(Announcement).all()
        return {"Announcements": [announcement.to_dict(i+1) for i, announcement in enumerate(announcements)]} # Return the row number as well

    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all announcements from the database"})
    
@router.get("/announcement/id/latest", tags=["Announcement"])
def get_Announcement_Latest_Id(db: Session = Depends(get_db)):
    try:
        count = db.query(Announcement).count()
        return {"id": count}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching latest announcement id from the table Announcement"})
    

""" ** POST Methods: Announcement Table APIs ** """

@router.post("/announcement/save", tags=["Announcement"])
async def save_Announcement(type_select: str = Form(...), title_input: str = Form(...), body_input: str = Form(...), 
                            type_of_attachment: Optional[str] = Form(None), attachment_image: Optional[UploadFile] = File(None), 
                            db: Session = Depends(get_db)):
    contents = await attachment_image.read()
    filename = attachment_image.filename
    access_token, refresh_token = get_access_token()
    headers = {'Authorization': 'Bearer ' + access_token}
    user_id = 'c769839c034ecd32'  # replace with actual user id or userPrincipalName
    response = requests.put(
        f'https://graph.microsoft.com/v1.0/users/{user_id}/drive/root:/{filename}:/content',
        headers=headers,
        data=contents  # This is the file contents.
    )
    response.raise_for_status()  # Raise an exception if the request failed

    return {
        "form_data": {
            "type_select": type_select,
            "title_input": title_input,
            "body_input": body_input,
            "type_of_attachment": type_of_attachment,
        },
        "image_details": {
            "filename": filename,
            "size": len(contents),
            "content_type": attachment_image.content_type,
            "status": response.status_code,
            "refresh_token": refresh_token,
        },
       
    }

    
#################################################################
""" Rule Table APIs """

class RuleSaveData(BaseModel):
    title: str
    body: str

class RuleUpdateData(BaseModel):
    id: int
    title: str
    body: str

class RuleDeleteData(BaseModel):
    id: int

""" ** GET Methods: Rule Table APIs ** """

@router.get("/rule/all", tags=["Rule"])
def get_All_Rules(db: Session = Depends(get_db)):
    try:
        rules = db.query(Rule).order_by(Rule.RuleId).all()
        return {"rules": [rule.to_dict(i+1) for i, rule in enumerate(rules)]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all rules from the database"})

@router.get("/rule/id/latest", tags=["Rule"])
def get_Rule_Latest_Id(db: Session = Depends(get_db)):
    try:
        count = db.query(Rule).count()
        return {"id": count}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching latest rule id from the table Rule"})

""" ** POST Methods: Rule Table APIs ** """

@router.post("/rule/save", tags=["Rule"])
def save_Rule(rule_data: RuleSaveData, db: Session = Depends(get_db)):
    try:
        new_rule = Rule(RuleTitle=rule_data.title, 
                        RuleBody=rule_data.body, 
                        created_at=datetime.now(), 
                        updated_at=datetime.now())
        db.add(new_rule)
        db.commit()
        return {"id": new_rule.RuleId,
                "type": "rule",
                "title": new_rule.RuleTitle,
                "body": new_rule.RuleBody,
                "created_at": new_rule.created_at.isoformat() if new_rule.created_at else None,
                "updated_at": new_rule.updated_at.isoformat() if new_rule.updated_at else None
                }
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while creating new rule in the table Rule"})
    
@router.put("/rule/update", tags=["Rule"])
def update_Rule(rule_data: RuleUpdateData, db: Session = Depends(get_db)):
    try:
        rule = db.query(Rule).get(rule_data.id)
        
        # If the rule does not exist, return a 404 error
        if not rule:
            return JSONResponse(status_code=404, content={"detail": "Rule not found"})
        
        # Update the rule's title and body
        rule.RuleTitle = rule_data.title
        rule.RuleBody = rule_data.body
        rule.updated_at = datetime.now()
        
        db.commit()

        return {"id": rule.RuleId,
                "type": "rule",
                "title": rule.RuleTitle,
                "body": rule.RuleBody,
                "created_at": rule.created_at.isoformat() if rule.created_at else None,
                "updated_at": rule.updated_at.isoformat() if rule.updated_at else None
                }
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while updating rule in the table Rule"})
    
@router.delete("/rule/delete", tags=["Rule"])
def delete_Rule(rule_data: RuleDeleteData, db: Session = Depends(get_db)):
    try:
        rule = db.query(Rule).get(rule_data.id)
        
        # If the rule does not exist, return a 404 error
        if not rule:
            return JSONResponse(status_code=404, content={"detail": "Rule not found"})
        
        db.delete(rule)
        db.commit()
        
        # Fetch all remaining rules
        rules = db.query(Rule).order_by(Rule.RuleId).all()
        
        # Update the IDs of the remaining rules
        for i, rule in enumerate(rules, start=1):
            rule.RuleId = i
            db.add(rule)
        
        db.commit()

        return {"detail": "Rule id " + str(rule_data.id) + " was successfully deleted and re-arranged the IDs of the remaining rule(s)"}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while deleting rule from the table Rule"})


#################################################################
""" Guideline Table APIs """

class GuidelineSaveData(BaseModel):
    title: str
    body: str

class GuidelineUpdateData(BaseModel):
    id: int
    title: str
    body: str

class GuidelineDeleteData(BaseModel):
    id: int

""" ** GET Methods: Guideline Table APIs ** """

@router.get("/guideline/all", tags=["Guideline"])
def get_All_Guidelines(db: Session = Depends(get_db)):
    try:
        guidelines = db.query(Guideline).order_by(Guideline.GuideId).all()
        return {"guidelines": [guideline.to_dict(i+1) for i, guideline in enumerate(guidelines)]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all guidelines from the database"})

@router.get("/guideline/id/latest", tags=["Guideline"])
def get_Guideline_Latest_Id(db: Session = Depends(get_db)):
    try:
        count = db.query(Guideline).count()
        return {"id": count}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching latest guideline id from the table Guideline"})
    
""" ** POST Methods: Guideline Table APIs ** """

@router.post("/guideline/save", tags=["Guideline"])
def save_Guideline(guideline_data: GuidelineSaveData, db: Session = Depends(get_db)):
    try:
        new_guideline = Guideline(GuidelineTitle=guideline_data.title, 
                                GuidelineBody=guideline_data.body, 
                                created_at=datetime.now(), 
                                updated_at=datetime.now())
        db.add(new_guideline)
        db.commit()
        return {"id": new_guideline.GuideId,
                "type": "guideline",
                "title": new_guideline.GuidelineTitle,
                "body": new_guideline.GuidelineBody,
                "created_at": new_guideline.created_at.isoformat() if new_guideline.created_at else None,
                "updated_at": new_guideline.updated_at.isoformat() if new_guideline.updated_at else None
                }
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while creating new guideline in the table Guideline"})
    
@router.put("/guideline/update", tags=["Guideline"])
def update_Guideline(guideline_data: GuidelineUpdateData, db: Session = Depends(get_db)):
    try:
        guideline = db.query(Guideline).get(guideline_data.id)
        
        # If the guideline does not exist, return a 404 error
        if not guideline:
            return JSONResponse(status_code=404, content={"detail": "Guideline not found"})
        
        # Update the guideline's title and body
        guideline.GuidelineTitle = guideline_data.title
        guideline.GuidelineBody = guideline_data.body
        guideline.updated_at = datetime.now()
        
        db.commit()

        return {"id": guideline.GuideId,
                "type": "guideline",
                "title": guideline.GuidelineTitle,
                "body": guideline.GuidelineBody,
                "created_at": guideline.created_at.isoformat() if guideline.created_at else None,
                "updated_at": guideline.updated_at.isoformat() if guideline.updated_at else None
                }
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while updating guideline in the table Guideline"})
    
@router.delete("/guideline/delete", tags=["Guideline"])
def delete_Guideline(guideline_data: GuidelineDeleteData, db: Session = Depends(get_db)):
    try:
        guideline = db.query(Guideline).get(guideline_data.id)
        
        # If the guideline does not exist, return a 404 error
        if not guideline:
            return JSONResponse(status_code=404, content={"detail": "Guideline not found"})
        
        db.delete(guideline)
        db.commit()
        
        # Fetch all remaining guidelines
        guidelines = db.query(Guideline).order_by(Guideline.GuideId).all()
        
        # Update the IDs of the remaining guideline
        for i, guideline in enumerate(guidelines, start=1):
            guideline.GuideId = i
            db.add(guideline)
        
        db.commit()

        return {"detail": "Guideline id " + str(guideline_data.id) + " was successfully deleted and re-arranged the IDs of the remaining guideline(s)"}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while deleting guideline from the table Guideline"})

#################################################################
app.include_router(router)