from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from database import engine, SessionLocal

from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import JSONResponse

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
    allow_origins=['http://127.0.0.1:8000'], # Must change to appropriate frontend URL (local or production)
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
        return {"Announcements": [announcement.to_dict() for announcement in announcements]}
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
def save_Announcement(announcement_data: AnnouncementSaveData, db: Session = Depends(get_db)):
    try:
        new_announcement = Announcement(
                        AnnouncementType=announcement_data.type, 
                        AnnouncementTitle=announcement_data.title, 
                        AnnouncementBody=announcement_data.body,
                        AttachmentType=announcement_data.attachment_type,
                        AttachmentImage=announcement_data.attachment_type,
                        created_at=datetime.now(), 
                        updated_at=datetime.now()
                        )
        db.add(new_announcement)
        db.commit()
        return {"id": new_announcement.AnnouncementId,
                "type": new_announcement.AnnouncementType,
                "title": new_announcement.AnnouncementTitle,
                "body": new_announcement.AnnouncementBody,
                "attachment_type": new_announcement.AttachmentType,
                "attachment_image": new_announcement.AttachmentImage,

                "created_at": new_announcement.created_at.isoformat() if new_announcement.created_at else None,
                "updated_at": new_announcement.updated_at.isoformat() if new_announcement.updated_at else None
                }
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while creating new announcement in the table Announcement"})

    
#################################################################
""" Rule Table APIs """

class RuleSaveData(BaseModel):
    title: str
    body: str

""" ** GET Methods: Rule Table APIs ** """

@router.get("/rule/all", tags=["Rule"])
def get_All_Rules(db: Session = Depends(get_db)):
    try:
        rules = db.query(Rule).all()
        return {"rules": [rule.to_dict() for rule in rules]}
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


#################################################################
""" Guideline Table APIs """

class GuidelineSaveData(BaseModel):
    title: str
    body: str

""" ** GET Methods: Guideline Table APIs ** """

@router.get("/guideline/all", tags=["Guideline"])
def get_All_Guidelines(db: Session = Depends(get_db)):
    try:
        guidelines = db.query(Guideline).all()
        return {"guidelines": [guideline.to_dict() for guideline in guidelines]}
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

#################################################################
app.include_router(router)