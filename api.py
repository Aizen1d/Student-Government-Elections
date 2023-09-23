from fastapi import FastAPI, HTTPException, Depends, APIRouter, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from fastapi.responses import JSONResponse

from dotenv import load_dotenv # for .env file
load_dotenv()

import time
import os
import requests
import cloudinary
import cloudinary.uploader
from cloudinary.api import resources_by_tag, delete_resources_by_tag, delete_folder

from models import Student, Announcement, Rule, Guideline, AzureToken 

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
#################################################################
""" Initial Setup """

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Store the expiration time and access token
EXPIRES_AT = 0
ACCESS_TOKEN = ""
REFRESH_TOKEN = ""

def get_initial_tokens(db: Session = Depends(get_db)):
    # Redirect the user to the OAuth server to log in
    auth_url = "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "http://localhost:8000/callback",  #
        "scope": "files.readwrite offline_access",
    }
    response = requests.get(auth_url, params=params)
    return response.url

def callback(code, db: Session = Depends(get_db)):
    # The user has logged in and authorized your app, and the OAuth server has redirected them back to your app
    # Now you can exchange the authorization code for an access token and refresh token
    token_url = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8000/callback",  # Use your actual redirect URI
    }
    response = requests.post(token_url, data=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get tokens")

    # Save the refresh token to the database
    db.add(AzureToken(access_token=response.json()["access_token"], expires_at=time.time() + response.json()["expires_in"], refresh_token=response.json()["refresh_token"]))
    db.commit()

def get_access_token(db: Session = Depends(get_db)):
    global REFRESH_TOKEN

    # Load the stored tokens and expiration time from the database
    token = db.query(AzureToken).first()

    if token is None:
        # No token in the database, need to get a new one
        EXPIRES_AT = 0
        ACCESS_TOKEN = ""
    else:
        EXPIRES_AT = token.expires_at
        ACCESS_TOKEN = token.access_token
        REFRESH_TOKEN = token.refresh_token  # Load the refresh token from the database

    # Check if the access token is expired or near to expire
    if time.time() > EXPIRES_AT:  # refresh
        token_url = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"

        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
            "grant_type": "refresh_token",
            "scope": "files.readwrite",
        }

        response = requests.post(token_url, data=payload)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get access token")

        # Update the stored refresh token and expiration time with the new ones
        REFRESH_TOKEN = response.json()["refresh_token"]
        EXPIRES_AT = time.time() + response.json()["expires_in"]
        ACCESS_TOKEN = response.json()["access_token"]

        # Save the updated tokens and expiration time to the database
        if token is None:
            # No existing token, create a new one
            db.add(AzureToken(access_token=ACCESS_TOKEN, expires_at=EXPIRES_AT, refresh_token=REFRESH_TOKEN))
        else:
            # Update the existing token
            token.access_token = ACCESS_TOKEN
            token.expires_at = EXPIRES_AT
            token.refresh_token = REFRESH_TOKEN  # Save the new refresh token to the database
            token.token_updates += 1  # Increment the token_updates value

        db.commit()

    return ACCESS_TOKEN, REFRESH_TOKEN

#################################################################
""" All about students APIs """

""" ** GET Methods: All about students APIs ** """

@router.get("/student/all", tags=["Student"])
def get_All_Students(db: Session = Depends(get_db)):
    try:
        students = db.query(Student).order_by(Student.StudentId).all()
        return {"students": [student.to_dict() for student in students]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all students from the database"})
    
#################################################################
""" Announcement Table APIs """

class AnnouncementDeleteData(BaseModel):
    id: int

""" ** GET Methods: Announcement Table APIs ** """

@router.get("/announcement/all", tags=["Announcement"])
def get_All_Announcement(db: Session = Depends(get_db)):
    try:
        announcements = db.query(Announcement).order_by(Announcement.AnnouncementId).all() 
        return {"announcements": [announcement.to_dict(i+1) for i, announcement in enumerate(announcements)]} # Return the row number as well
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all announcements from the database"})
    
@router.get("/announcement/get/attachment/{id}", tags=["Announcement"])
def get_Announcement_Attachment_By_Id(id: int, db: Session = Depends(get_db)):

    announcement = db.query(Announcement).get(id)

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    tag_name = announcement.AttachmentImage

    if tag_name:

        # Search for images with the tag using the Admin API
        response = resources_by_tag(tag_name)

        # Get the URLs and file names of the images
        images = [{"url": resource['secure_url'], 
                "name": resource['public_id'].split('/')[-1]} for resource in response['resources']]

        return {"images": images}
    
    return {"images": []}
        
@router.get("/announcement/count/latest", tags=["Announcement"])
def get_Announcement_Latest_Count(db: Session = Depends(get_db)):
    try:
        count = db.query(Announcement).count()
        return {"count": count}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching latest announcement count from the table Announcement"})
    
""" ** POST Methods: Announcement Table APIs ** """

@router.post("/announcement/save", tags=["Announcement"])
async def save_Announcement(type_select: str = Form(...), title_input: str = Form(...), body_input: str = Form(...), 
                            type_of_attachment: Optional[str] = Form(None), attachment_images: List[UploadFile] = File(None), 
                            db: Session = Depends(get_db)):
    
    # Create a new announcement with an empty string as the initial AttachmentImage
    new_announcement = Announcement(
        AnnouncementType=type_select, 
        AnnouncementTitle=title_input, 
        AnnouncementBody=body_input,
        AttachmentType=type_of_attachment,
        AttachmentImage='',  # Initialize with an empty string
        created_at=datetime.now(), 
        updated_at=datetime.now()
    )

    db.add(new_announcement)
    db.commit()

    try:
        if attachment_images:
            # Use the ID of the new announcement as the subfolder name under 'Announcements'            
            folder_name = f"Announcements/announcement_{new_announcement.AnnouncementId}"

            for attachment_image in attachment_images:
                contents = await attachment_image.read()
                filename = attachment_image.filename

                # Upload file to Cloudinary with the folder name in the public ID
                response = cloudinary.uploader.upload(contents, public_id=f"{folder_name}/{filename}", tags=[f'announcement_{new_announcement.AnnouncementId}'])

                # Store the URL in the AttachmentImage column
                new_announcement.AttachmentImage = f'announcement_{new_announcement.AnnouncementId}'
                db.commit()
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while uploading attachment to Cloudinary"})

    return {
        "id": new_announcement.AnnouncementId,
        "type": new_announcement.AnnouncementType,
        "title": new_announcement.AnnouncementTitle,
        "body": new_announcement.AnnouncementBody,
        "attachment_type": new_announcement.AttachmentType,
        "attachment_image": new_announcement.AttachmentImage,
    }

@router.put("/announcement/update", tags=["Announcement"])
async def update_Announcement(id_input: int = Form(...), type_select: str = Form(...), title_input: str = Form(...), body_input: str = Form(...), 
                            type_of_attachment: Optional[str] = Form(None), attachment_images: List[UploadFile] = File(None),
                            new_files: List[UploadFile] = File(None),
                            db: Session = Depends(get_db), attachments_modified: bool = Form(False)):
    
    original_announcement = db.query(Announcement).get(id_input)

    if not original_announcement:
        return {"error": "Announcement not found"}

    # Use the ID of the announcement as the tag
    folder_name = f"Announcements/announcement_{id_input}"
    tag_name = f'announcement_{id_input}'

    if attachment_images and attachments_modified:
        # Get all images with the tag
        response = resources_by_tag(tag_name)
        images_in_folder = [{"url": resource['secure_url'], "name": resource['public_id'].split('/')[-1]} for resource in response['resources']]

        # Check for removed files
        for image in images_in_folder:
            if not any(attachment_image.filename == image['name'] for attachment_image in attachment_images):
                # This file has been removed locally, delete it from Cloudinary
                delete_resources_by_tag(image['name'])

    if new_files and attachments_modified:
        # Check for new files
        for new_file in new_files:
            # This is a new file, upload it to Cloudinary
            contents = await new_file.read()
            filename = new_file.filename

            # Upload file to Cloudinary with the folder name in the public ID
            response = cloudinary.uploader.upload(contents, public_id=f"{folder_name}/{filename}", tags=[tag_name])

        original_announcement.AttachmentImage = tag_name

    if type_of_attachment == 'None' and original_announcement.AttachmentImage:
        # Delete all images with the tag
        delete_resources_by_tag(tag_name)

        # Delete the folder in Cloudinary
        delete_folder(folder_name)

        original_announcement.AttachmentImage = ''

    # Update the announcement in the database
    original_announcement.AnnouncementType = type_select
    original_announcement.AnnouncementTitle = title_input
    original_announcement.AnnouncementBody = body_input
    original_announcement.AttachmentType = type_of_attachment
    original_announcement.updated_at = datetime.now()

    db.commit()
    
    return {
        "id": original_announcement.AnnouncementId,
        "type": original_announcement.AnnouncementType,
        "title": original_announcement.AnnouncementTitle,
        "body": original_announcement.AnnouncementBody,
        "attachment_type": original_announcement.AttachmentType if original_announcement.AttachmentType else 'None',
        "attachment_image": original_announcement.AttachmentImage if original_announcement.AttachmentImage else '',
    }

@router.delete("/announcement/delete", tags=["Announcement"])
def delete_Announcement(announcement_data: AnnouncementDeleteData, db: Session = Depends(get_db)):
    try:
        announcement = db.query(Announcement).get(announcement_data.id)

        if not announcement:
            return {"error": "Announcement not found"}

        if announcement.AttachmentImage:
            folder_name = f"Announcements/announcement_{announcement.AnnouncementId}"
            tag_name = f'announcement_{announcement.AnnouncementId}'

            # Delete all images with the tag
            response = delete_resources_by_tag(tag_name)

            # Check if the request was successful
            if 'result' in response and response['result'] != 'ok':
                return JSONResponse(status_code=500, content={"detail": "Failed to delete images"})

            # Delete the folder in Cloudinary
            response = delete_folder(folder_name)

            # Check if the request was successful
            if 'result' in response and response['result'] != 'ok':
                return JSONResponse(status_code=500, content={"detail": "Failed to delete folder"})
        
        db.delete(announcement)
        db.commit()
        
        return {"detail": "Announcement id " + str(announcement_data.id) + " was successfully deleted)"}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while deleting announcement from the table Announcement"})
  
    
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

@router.get("/rule/count/latest", tags=["Rule"])
def get_Rule_Latest_Count(db: Session = Depends(get_db)):
    try:
        count = db.query(Rule).count()
        return {"count": count}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching latest rule count from the table Rule"})

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

        return {"detail": "Rule id " + str(rule_data.id) + " was successfully deleted"}
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

@router.get("/guideline/count/latest", tags=["Guideline"])
def get_Guideline_Latest_Count(db: Session = Depends(get_db)):
    try:
        count = db.query(Guideline).count()
        return {"count": count}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching latest guideline count from the table Guideline"})
    
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
        
        return {"detail": "Guideline id " + str(guideline_data.id) + " was successfully deleted)"}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while deleting guideline from the table Guideline"})

#################################################################
app.include_router(router)