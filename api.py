from fastapi import FastAPI, HTTPException, Depends, APIRouter, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from database import engine, SessionLocal, Base

from pydantic import BaseModel
from typing import Optional, List, Dict, Union
from datetime import datetime, date

from dotenv import load_dotenv # for .env file
load_dotenv()

import pandas as pd
import time
import os
import requests
import cloudinary
import cloudinary.uploader
from cloudinary.api import resources_by_tag, delete_resources_by_tag, delete_folder

from models import Student, Organization, Announcement, Rule, Guideline, AzureToken, Election, SavedPosition, CreatedElectionPosition

#################################################################
""" Settings """

tags_metadata = [
    {
        "name": "Student",
        "description": "Manage students.",
    },
    {
        "name": "Election",
        "description": "Manage elections.",
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

    {
        "name": "Organization Election",
        "description": "Manage organization elections.",
    },
]

app = FastAPI(
    title="API for Student Goverment Election",
    description="This is the API for the Student Government Election. (Default API's are for comelec e.g (Election APIs))",
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

class SaveStudentData(BaseModel):
    student_number: str
    course: str
    first_name: str
    middle_name: str
    last_name: str
    email: str
    birth_date: date
    semester: str
    year_enrolled: str

def validate_columns(df, expected_columns):
    if not set(expected_columns).issubset(df.columns):
        missing_columns = list(set(expected_columns) - set(df.columns))
        return False, {"message": f"Upload failed. The following required columns are missing: {missing_columns}"}
    return True, {}

def process_data(df):
    # Convert 'YearEnrolled' to string
    df['YearEnrolled'] = df['YearEnrolled'].apply(lambda x: str(int(x)) if pd.notnull(x) else x)

    # Clean the data: trim leading/trailing whitespace
    df = df.apply(lambda col: col.str.strip() if col.dtype == 'object' else col)

    # Remove duplicate entries based on 'StudentNumber'
    df.drop_duplicates(subset=['StudentNumber'], keep='first', inplace=True)

    # Replace 'nan' with an empty string
    df.fillna('', inplace=True)
    
    return df

""" ** GET Methods: All about students APIs ** """

@router.get("/student/all", tags=["Student"])
def get_All_Students(db: Session = Depends(get_db)):
    try:
        students = db.query(Student).order_by(Student.StudentId).all()
        return {"students": [student.to_dict() for student in students]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all students from the database"})
    
@router.post("/student/insert/data/manual", tags=["Student"])
def student_Insert_Data_Manual(data: SaveStudentData, db: Session = Depends(get_db)):
    # Check if a student with the given StudentNumber already exists
    existing_student = db.query(Student).filter(Student.StudentNumber == data.student_number).first()
    existing_email = db.query(Student).filter(Student.EmailAddress == data.email).first()

    if existing_student:
        return {"error": f"Student with student number {data.student_number} already exists."}
    
    if existing_email:
        return {"error": f"Student with email address {data.email} already exists."}

    # Insert the data into the database
    student = Student(
        StudentNumber=data.student_number,
        FirstName=data.first_name,
        MiddleName=data.middle_name,
        LastName=data.last_name,
        EmailAddress=data.email,
        BirthDate=data.birth_date,
        Course=data.course,
        CurrentSemesterEnrolled=data.semester,
        YearEnrolled=data.year_enrolled,
        IsOfficer=False
    )
    db.add(student)
    db.commit()

    return {"message": f"Student {data.student_number} was inserted successfully."}

@router.post("/student/insert/data/attachment", tags=["Student"])
async def student_Insert_Data_Attachment(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    responses = []
    elements = []
    styleSheet = getSampleStyleSheet()

    for file in files:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file.file, encoding='ISO-8859-1')
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file.file, engine='openpyxl')
        else:
            responses.append({"file": file.filename, "message": "Upload failed. The file format is not supported."})
            continue

        # Define the expected columns
        expected_columns = ['StudentNumber', 'FirstName', 'MiddleName', 'LastName', 'EmailAddress', 
                            'BirthDate', 'Course', 'CurrentSemesterEnrolled', 'YearEnrolled', 'IsOfficer']

        # Check if all expected columns exist in the DataFrame
        valid, response = validate_columns(df, expected_columns)
        if not valid:
            responses.append({"file": file.filename, "unexpected_columns": response})
            continue

        # Process the data
        df = process_data(df)

        existing_students = {student.StudentNumber for student in db.query(Student).all()}
        existing_emails = {student.EmailAddress for student in db.query(Student).all()}
        inserted_student_count = 0
        incomplete_student_column_count = 0

        # Insert the data into the database
        inserted_students = []
        not_inserted_students_due_to_uniqueness = []  # List to store students not inserted
        incomplete_student_column = []
        for index, row in df.iterrows():
           
            # If the student number and email do not exist and all fields are not empty
            if str(row['StudentNumber']) not in existing_students and str(row['EmailAddress']) not in existing_emails and all(row[field] != '' for field in ['FirstName', 'LastName', 'EmailAddress', 'BirthDate', 'Course', 'CurrentSemesterEnrolled', 'YearEnrolled', 'IsOfficer']):
                student = Student(
                    StudentNumber=row['StudentNumber'],
                    FirstName=row['FirstName'],
                    MiddleName=row.get('MiddleName', ''),  # Use .get() to make MiddleName optional
                    LastName=row['LastName'],
                    EmailAddress=row['EmailAddress'],
                    BirthDate=row['BirthDate'],
                    Course=row['Course'],
                    CurrentSemesterEnrolled=row['CurrentSemesterEnrolled'],
                    YearEnrolled=row['YearEnrolled'],
                    IsOfficer=row['IsOfficer']
                )
                inserted_student_count += 1
                db.add(student)
                inserted_students.append([row['StudentNumber'], row['FirstName'], row.get('MiddleName', ''), row['LastName'], row['EmailAddress']])

                # Commit every 100 students
                if inserted_student_count % 100 == 0:
                    db.commit()
            
            # If the student number or email already exists
            elif str(row['StudentNumber']) in existing_students or str(row['EmailAddress']) in existing_emails:
                not_inserted_students_due_to_uniqueness.append([row['StudentNumber'], row['FirstName'], row.get('MiddleName', ''), row['LastName'], row['EmailAddress']])
            
            # If there are missing fields
            else:
                incomplete_student_column_count += 1
                incomplete_student_column.append([row['StudentNumber'], row['FirstName'], row.get('MiddleName', ''), row['LastName'], row['EmailAddress']])

        # Commit any remaining students
        if inserted_student_count % 100 != 0:
            db.commit()

        if inserted_student_count == 0 and incomplete_student_column_count == 0:
            responses.append({"no_new_students": f"All students in ({file.filename}) were already inserted. No changes applied."})
        else:
            # If there are inserted students but no incomplete student columns
            if inserted_student_count > 0 and incomplete_student_column_count <= 0:
                responses.append({"file": file.filename, "message": "Upload successful, inserted students: " + str(inserted_student_count)})
            
            # If there are inserted students and incomplete student columns
            elif inserted_student_count > 0 and incomplete_student_column_count > 0:
                responses.append({"file": file.filename, "message": "Upload successful, inserted students: " + str(inserted_student_count) + ", incomplete student columns: " + str(incomplete_student_column_count)})
            
            # If there are no inserted students but there are incomplete student columns
            elif inserted_student_count <= 0 and incomplete_student_column_count > 0:
                responses.append({"file": file.filename, "message": "No new students were inserted, incomplete student columns: " + str(incomplete_student_column_count)})
            
        # Add a table to the PDF for each file
        if inserted_student_count > 0 or incomplete_student_column_count > 0:
            elements.append(Paragraph(f"<para align=center><b>{file.filename}</b></para>", styleSheet["BodyText"]))
            elements.append(Spacer(1, 12))

            if inserted_students:
                elements.append(Paragraph(f"Number of inserted students: {len(inserted_students)}"))
                elements.append(Spacer(1, 12))
                table = Table([["Student Number", "First Name", "Middle Name", "Last Name", "Email"]] + inserted_students)
                table.setStyle(TableStyle([
                    ('GRID', (0,0), (-1,-1), 1, colors.black),
                    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                ]))
                elements.append(table)

            if not_inserted_students_due_to_uniqueness:
                elements.append(Spacer(1, 12))
                elements.append(Paragraph(f"Number of not inserted students due to student number or email exists already: {len(not_inserted_students_due_to_uniqueness)}"))
                elements.append(Spacer(1, 12))
                table = Table([["Student Number", "First Name", "Middle Name", "Last Name", "Email"]] + not_inserted_students_due_to_uniqueness)
                table.setStyle(TableStyle([
                    ('GRID', (0,0), (-1,-1), 1, colors.black),
                    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                ]))
                elements.append(table)

            if incomplete_student_column:
                elements.append(Spacer(1, 12))
                elements.append(Paragraph(f"Number of not inserted students due to incomplete column value(s): {len(incomplete_student_column)}"))
                elements.append(Spacer(1, 12))
                table = Table([["Student Number", "First Name", "Middle Name", "Last Name", "Email"]] + incomplete_student_column)
                table.setStyle(TableStyle([
                    ('GRID', (0,0), (-1,-1), 1, colors.black),
                    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                ]))
                elements.append(table)

            elements.append(Spacer(1, 12))

    if inserted_student_count > 0 or incomplete_student_column_count > 0:
        # Save the PDF to a temporary file
        now = datetime.now()
        pdf_name = f"Report_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(pdf_name, pagesize=letter)
        doc.build(elements)

        # Upload to cloudinary
        upload_result = cloudinary.uploader.upload(pdf_name, 
                                            resource_type = "raw", 
                                            public_id = f"InsertData/Reports/{pdf_name}",
                                            tags=[pdf_name])
        
        # Delete the local file
        os.remove(pdf_name)

    # Return the responses and a URL to download the PDF
        return JSONResponse({
            "responses": responses,
            "pdf_url": upload_result['secure_url']
        })
    else:
        # Return the responses only if no PDF was generated
        return JSONResponse({
                    "responses": responses,
                })

#################################################################
""" Election Table APIs """

class ElectionInfoData(BaseModel):
    election_name: str
    election_type: str
    school_year: str
    semester: str
    election_start: datetime
    election_end: datetime
    filing_coc_start: datetime
    filing_coc_end: datetime
    campaign_start: datetime
    campaign_end: datetime
    voting_start: datetime
    voting_end: datetime
    appeal_start: datetime
    appeal_end: datetime
    created_by: str

class CreatedPositionData(BaseModel):
    value: str
    quantity: str

class CreateElectionData(BaseModel):
    positions: List[CreatedPositionData]
    election_info: ElectionInfoData

class SaveReusablePositionData(BaseModel):
    name: str

class ElectionDelete(BaseModel):
    id: int

""" ** GET Methods: All about election APIs ** """
@router.get("/election/all", tags=["Election"])
def get_All_Election(db: Session = Depends(get_db)):
    try:
        elections = db.query(Election).order_by(Election.ElectionId).all()
        elections_with_creator = []

        for i, election in enumerate(elections):
            creator = db.query(Student).filter(Student.StudentNumber == election.CreatedBy).first()
            election_dict = election.to_dict(i+1)
            election_dict["CreatedByName"] = (creator.FirstName + ' ' + (creator.MiddleName + ' ' if creator.MiddleName else '') + creator.LastName) if creator else ""
            
            elections_with_creator.append(election_dict)

        return {"elections": elections_with_creator}

    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all elections from the database"})

    
@router.get("/election/view/{id}", tags=["Election"])
def get_Election_By_Id(id: int, db: Session = Depends(get_db)):
    try:
        election = db.query(Election).get(id)

        if not election:
            return JSONResponse(status_code=404, content={"detail": "Election not found"})

        positions = db.query(CreatedElectionPosition).filter(CreatedElectionPosition.ElectionId == id).all()

        election_count = db.query(Election).count()
        return {"election": election.to_dict(election_count),
                "positions": [position.to_dict(i+1) for i, position in enumerate(positions)]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching election from the database"})

@router.get("/election/position/reusable/all", tags=["Election"])    
def get_All_Election_Position_Reusable(db: Session = Depends(get_db)):
    try:
        positions = db.query(SavedPosition).order_by(SavedPosition.SavedPositionId).all()
        return {"positions": [position.to_dict() for position in positions]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all positions from the database"})


""" ** POST Methods: All about election APIs ** """
@router.post("/election/create", tags=["Election"])
def save_election(election_data: CreateElectionData, db: Session = Depends(get_db)):
    new_election = Election(ElectionName=election_data.election_info.election_name,
                            ElectionType=election_data.election_info.election_type,
                            ElectionStatus="Active",
                            SchoolYear=election_data.election_info.school_year,
                            Semester=election_data.election_info.semester,
                            CreatedBy=election_data.election_info.created_by,
                            ElectionStart=election_data.election_info.election_start,
                            ElectionEnd=election_data.election_info.election_end,
                            CoCFilingStart=election_data.election_info.filing_coc_start,
                            CoCFilingEnd=election_data.election_info.filing_coc_end,
                            CampaignStart=election_data.election_info.campaign_start,
                            CampaignEnd=election_data.election_info.campaign_end,
                            VotingStart=election_data.election_info.voting_start,
                            VotingEnd=election_data.election_info.voting_end,
                            AppealStart=election_data.election_info.appeal_start,
                            AppealEnd=election_data.election_info.appeal_end,
                            created_at=datetime.now(), 
                            updated_at=datetime.now())
    db.add(new_election)
    db.commit()

    for position in election_data.positions:
        new_position = CreatedElectionPosition(ElectionId=new_election.ElectionId,
                                                PositionName=position.value,
                                                PositionQuantity=position.quantity,
                                                created_at=datetime.now(), 
                                                updated_at=datetime.now())
        db.add(new_position)
        db.commit()

    return {"message": "Election created successfully",
            "election_id": new_election.ElectionId,}


@router.post("/election/position/reusable/save", tags=["Election"])
async def save_Election_Position_Reusable(data: SaveReusablePositionData, db: Session = Depends(get_db)):
    capitalized_first_letter = data.name.capitalize()
    new_position = SavedPosition(PositionName=capitalized_first_letter,
                                            created_at=datetime.now(),
                                            updated_at=datetime.now())
    db.add(new_position)
    db.commit()

    return {"message": f"Position {capitalized_first_letter} is now re-usable."}

@router.delete("/election/position/reusable/delete", tags=["Election"])
def delete_Election_Position_Reusable(data: SaveReusablePositionData, db: Session = Depends(get_db)):
    capitalized_first_letter = data.name.capitalize()
    position = db.query(SavedPosition).filter(SavedPosition.PositionName == capitalized_first_letter).first()

    if not position:
        return {"error": "Position not found"}

    db.delete(position)
    db.commit()

    return {"message": f"Position {capitalized_first_letter} is not re-usable anymore."}

@router.post("/election/delete", tags=["Election"])
def delete_Election(data: ElectionDelete, db: Session = Depends(get_db)):
    election = db.query(Election).filter(Election.ElectionId == data.id).first()
    positions = db.query(CreatedElectionPosition).filter(CreatedElectionPosition.ElectionId == data.id).all()

    if not election:
        return {"error": "Election not found"}

    for position in positions:
        if position:
            db.delete(position)
            db.commit()

    db.delete(election)
    db.commit()

    return {"message": f"Election {election.ElectionName} was deleted successfully."}

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
    try:
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
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching announcement attachment from Cloudinary"})
        
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
                            new_files: List[UploadFile] = File(None), removed_files: List[UploadFile] = File(None),
                            db: Session = Depends(get_db), attachments_modified: bool = Form(False)):
    
    try:
        original_announcement = db.query(Announcement).get(id_input)

        if not original_announcement:
            return {"error": "Announcement not found"}

        # Use the ID of the announcement as the tag
        tag_name = original_announcement.AttachmentImage if original_announcement.AttachmentImage else "announcement_" + str(original_announcement.AnnouncementId)
        folder_name = f"Announcements/{tag_name}"

        if removed_files and attachments_modified:
            # Check for removed files
            for removed_file in removed_files:
                # This is a removed file, delete it from Cloudinary
                file_path = f"{folder_name}/{removed_file.filename}"
                cloudinary.uploader.destroy(file_path)

        uploaded_files = []

        if new_files and attachments_modified:
            # Check for new files
            for new_file in new_files:
                # This is a new file, upload it to Cloudinary
                contents = await new_file.read()
                filename = new_file.filename

                # Upload file to Cloudinary with the folder name in the public ID
                response = cloudinary.uploader.upload(contents, public_id=f"{folder_name}/{filename}", tags=[tag_name])

                # Add the name and URL of the uploaded file to the list
                uploaded_files.append({
                    'name': filename,
                    'url': response['url']
                })

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
            "uploaded_files": uploaded_files,  
        }
    
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while updating announcement in the table Announcement"})

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
## Organizations APIs ## 
class OrganizationName(BaseModel):
    name: str

""" Organization Election Table APIs """

""" ** POST Methods: All about orgnanization election APIs ** """
@router.post("/election/organization/all", tags=["Organization Election"])
def get_All_Organization_Election(org_data: OrganizationName, db: Session = Depends(get_db)):
    try:
        # Join Election and Organization tables
        elections = db.query(Election, Organization).join(Organization, Election.CreatedBy == Organization.StudentNumber).filter(Organization.OrganizationName == org_data.name).order_by(Election.ElectionId).all()
        
        elections_with_creator = []

        for i, (election, organization) in enumerate(elections):
            creator = db.query(Student).filter(Student.StudentNumber == election.CreatedBy).first()
            election_dict = election.to_dict(i+1)
            election_dict["CreatedByName"] = (creator.FirstName + ' ' + (creator.MiddleName + ' ' if creator.MiddleName else '') + creator.LastName) if creator else ""
            
            elections_with_creator.append(election_dict)

        return {"elections": elections_with_creator}

    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all elections from the database"})


#################################################################
app.include_router(router)