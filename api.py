from fastapi import FastAPI, HTTPException, Depends, APIRouter, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse

from sqlalchemy import inspect, func, and_
from sqlalchemy.orm import Session

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Flowable, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.date import DateTrigger

from database import engine, SessionLocal, Base

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
from datetime import datetime, date, timedelta
from collections import defaultdict

from dotenv import load_dotenv # for .env file
load_dotenv()

import pandas as pd
import time
import string
import random
import os
import requests
import cloudinary
import cloudinary.uploader
import asyncio
import requests

from passlib.context import CryptContext
from cloudinary.api import resources_by_tag, delete_resources_by_tag, delete_folder
from services import send_verification_code_email, send_pass_code_queue_email, send_pass_code_manual_email, send_coc_status_email, send_partylist_status_email

from models import Student, Announcement, Rule, Guideline, AzureToken, Election, SavedPosition, CreatedElectionPosition, Code, StudentPassword, PartyList, CoC, InsertDataQueues, Candidates, RatingsTracker, VotingsTracker, ElectionAnalytics, ElectionWinners, Certifications, CreatedAdminSignatory, StudentOrganization, OrganizationOfficer, OrganizationMember
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
    {
        "name": "CoC",
        "description": "Manage CoCs."
    },
    {
        "name": "Code",
        "description": "Manage codes.",
    },
    {
        "name": "Party List",
        "description": "Manage party lists.",
    }
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
    allow_origins=['http://localhost:8000', 'http://127.0.0.1:8000', 'http://127.0.0.1:7500', 'http://127.0.0.1:7000'], # Must change to appropriate frontend URL (local or production)
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

# Create anbd start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_jobstore(SQLAlchemyJobStore(url='sqlite:///jobs.sqlite'), 'default')

@app.on_event("startup")
def start_up():
    scheduler.start()

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
    year: str
    semester: str
    year_enrolled: str

def validate_columns(df, expected_columns):
    if not set(expected_columns).issubset(df.columns):
        missing_columns = list(set(expected_columns) - set(df.columns))
        return False, {"message": f"Upload failed. The following required columns are missing: {missing_columns}"}
    return True, {}

def process_data(df):
    # Make a copy of the DataFrame before removing duplicates
    df_before = df.copy()

    # Convert 'YearEnrolled' to string
    df['YearEnrolled'] = df['YearEnrolled'].apply(lambda x: str(int(x)) if pd.notnull(x) else x)

    # Remove duplicate entries based on 'EmailAddress'
    df.sort_values(by=['EmailAddress'], inplace=True)
    df.drop_duplicates(subset=['EmailAddress'], keep='first', inplace=True)

    # Remove duplicate entries based on 'StudentNumber'
    df.sort_values(by=['StudentNumber'], inplace=True)
    df.drop_duplicates(subset=['StudentNumber'], keep='first', inplace=True)

    # Replace 'nan' with an empty string
    df.fillna('', inplace=True)
    
    # Get the removed duplicates by finding rows in df_before that aren't in df
    removed_duplicates = df_before.loc[df_before.index.difference(df.index)]

    # Drop additional columns from removed_duplicates
    removed_duplicates = removed_duplicates[['StudentNumber', 'FirstName', 'MiddleName', 'LastName', 'EmailAddress']]

    return df, removed_duplicates

""" ** GET Methods: All about students APIs ** """

@router.get("/student/all", tags=["Student"])
def get_All_Students(db: Session = Depends(get_db)):
    try:
        students = db.query(Student).order_by(Student.StudentId).all()
        return {"students": [student.to_dict() for student in students]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all students from the database"})
    
@router.get("/student/all/arranged", tags=["Student"])
def get_All_Students_Arranged(db: Session = Depends(get_db)):
    try:
        # Arrange by course, last name, first name, middle name
        students = db.query(Student).order_by(Student.Course, Student.LastName, Student.FirstName, Student.MiddleName).all()

        return {"students": [student.to_dict() for student in students]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all students from the database"})
    
@router.get("/student/fullname/{student_number}", tags=["Student"])
def get_Student_By_Student_Number(student_number: str, db: Session = Depends(get_db)):
    try:
        student = db.query(Student).filter(Student.StudentNumber == student_number).first()
        
        # Get the full name of the student check for middle name
        full_name = student.FirstName + ' ' + (student.MiddleName + ' ' if student.MiddleName else '') + student.LastName

        return {"full_name": full_name}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching the student from the database"})
    
@router.get("/student/insert/data/queues/all", tags=["Student"])
def get_All_Insert_Data_Queues(db: Session = Depends(get_db)):
    try:
        queues = db.query(InsertDataQueues).order_by(InsertDataQueues.QueueId).all()
        return {"queues": [queue.to_dict() for queue in queues]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all queues from the database"})

    
""" ** POST Methods: All about students APIs ** """
# Create a queue
queue = asyncio.Queue()

# Define a worker function
async def insert_data_email_worker():
    while True:
        db = SessionLocal()

        # Get a task from the queue
        task = await queue.get()

        # Process the task
        queue_id, student_number, student_email, pass_code = task
        send_pass_code_queue_email(student_number, student_email, pass_code, queue_id)

        # Indicate that the task is done
        queue.task_done()

# Start the worker in the background
asyncio.create_task(insert_data_email_worker())
    
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
        Year=data.year,
        Course=data.course,
        CurrentSemesterEnrolled=data.semester,
        YearEnrolled=data.year_enrolled,
        IsOfficer=False
    )
    db.add(student)
    db.commit()

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Generate a unique code and add it to the database
    while True:
        # Generate a random code
        pass_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

        # Hash the password
        hashed_password = pwd_context.hash(pass_value)

        # Check if the code already exists in the database
        existing_code = db.query(StudentPassword).filter(StudentPassword.Password == hashed_password).first()

        # If the code doesn't exist in the database, insert it and break the loop
        if not existing_code:
            new_pass = StudentPassword(StudentNumber=data.student_number, 
                            Password=hashed_password,
                            created_at=datetime.now(),
                            updated_at=datetime.now())
            db.add(new_pass)
            db.commit()

            send_pass_code_manual_email(data.student_number, data.email, pass_value)
            break

    return {"message": f"Student {data.student_number} was inserted successfully."}

@router.post("/student/insert/data/attachment", tags=["Student"])
async def student_Insert_Data_Attachment(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    responses = []
    elements = []
    styleSheet = getSampleStyleSheet()

    inserted_student_count = 0
    incomplete_student_column_count = 0

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
                            'Year', 'Course', 'CurrentSemesterEnrolled', 'YearEnrolled', 'IsOfficer']

        # Check if all expected columns exist in the DataFrame
        valid, response = validate_columns(df, expected_columns)
        if not valid:
            responses.append({"file": file.filename, "unexpected_columns": response})
            continue

        # Process the data
        df, removed_duplicates = process_data(df)

        existing_students = {student.StudentNumber for student in db.query(Student).all()}
        existing_emails = {student.EmailAddress for student in db.query(Student).all()}

        # Insert the data into the database
        inserted_students = []
        not_inserted_students_due_to_uniqueness = []  # List to store students not inserted
        incomplete_student_column = []

        # Create a new queue in the InsertDataQueues table
        new_queue = InsertDataQueues(QueueName=file.filename, 
                                   ToEmailTotal=0, 
                                   EmailSent=0, 
                                   EmailFailed=0,
                                   Status="Pending",
                                   created_at=datetime.now(),
                                   updated_at=datetime.now())
        db.add(new_queue)
        db.flush() # Flush the session to get the QueueId

        for index, row in df.iterrows():
           
            # If the student number and email do not exist and all fields are not empty
            if str(row['StudentNumber']) not in existing_students and str(row['EmailAddress']) not in existing_emails and all(row[field] != '' for field in ['FirstName', 'LastName', 'EmailAddress', 'Year', 'Course', 'CurrentSemesterEnrolled', 'YearEnrolled', 'IsOfficer']):
                student = Student(
                    StudentNumber=row['StudentNumber'],
                    FirstName=row['FirstName'],
                    MiddleName=row.get('MiddleName', ''),  # Use .get() to make MiddleName optional
                    LastName=row['LastName'],
                    EmailAddress=row['EmailAddress'],
                    Year=row['Year'],
                    Course=row['Course'],
                    CurrentSemesterEnrolled=row['CurrentSemesterEnrolled'],
                    YearEnrolled=row['YearEnrolled'],
                    IsOfficer=row['IsOfficer']
                )
                inserted_student_count += 1
                db.add(student)
                inserted_students.append([row['StudentNumber'], row['FirstName'], row.get('MiddleName', ''), row['LastName'], row['EmailAddress']])

                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

                # Generate a unique code and add it to the database
                while True:
                    # Generate a random code
                    pass_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

                    # Hash the password
                    hashed_password = pwd_context.hash(pass_value)

                    # Check if the code already exists in the database
                    existing_code = db.query(StudentPassword).filter(StudentPassword.Password == hashed_password).first()

                    # If the code doesn't exist in the database, insert it and break the loop
                    if not existing_code:
                        new_pass = StudentPassword(StudentNumber=row['StudentNumber'], 
                                        Password=hashed_password,
                                        created_at=datetime.now(),
                                        updated_at=datetime.now())
                        db.add(new_pass)
                        db.commit()

                        # Add the email task to the queue
                        new_queue.ToEmailTotal += 1
                        await queue.put((new_queue.QueueId, row['StudentNumber'], row['EmailAddress'], pass_value))
                        break

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

            if not removed_duplicates.empty:
                elements.append(Paragraph(f"Number of removed duplicates: {len(removed_duplicates.values.tolist())}"))
                elements.append(Spacer(1, 12))
                table = Table([["Student Number", "First Name", "Middle Name", "Last Name", "Email"]] + removed_duplicates.values.tolist())
                table.setStyle(TableStyle([
                    ('GRID', (0,0), (-1,-1), 1, colors.black),
                    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                ]))
                elements.append(table)

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
    
class LoginData(BaseModel):
    StudentNumber: str
    Password: str

@router.post("/student/voting/login", tags=["Student"])
def student_Voting_Login(data: LoginData, db: Session = Depends(get_db)):
    StudentNumber = data.StudentNumber
    Password = data.Password

    student = db.query(Student).filter(Student.StudentNumber == StudentNumber).first()
    if not student:
        return {"error": "Student not found."}

    student_password = db.query(StudentPassword).filter(StudentPassword.StudentNumber == StudentNumber).first()
    if not student_password:
        return {"error": "Student password not found."}

    # Check if the password matches
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(Password, student_password.Password):
        return {"error": "Incorrect password."}

    return {"message": True}

#################################################################
""" Student Organization Table APIs """
class Officer(BaseModel):
    student_number: str
    position: str
    image: str

class Member(BaseModel):
    student_number: str

class StudentOrganizationData(BaseModel):
    organization_logo: str
    organization_name: str
    organization_requirements: str
    organization_adviser_image: str
    organization_adviser_name: str
    organization_vision: str
    organization_mission: str
    officers: List[Officer]
    members: List[Member]

""" ** GET Methods: All about Student Organizations APIs ** """
@router.get("/student/organization/all", tags=["Student Organization"])
def get_All_Student_Organization(db: Session = Depends(get_db)):
    student_organizations = db.query(StudentOrganization).order_by(StudentOrganization.StudentOrganizationId).all()
    return {"student_organizations": [student_organization.to_dict() for student_organization in student_organizations]}

""" ** POST Methods: All about Student Organizations APIs ** """
@router.post("/student/organization/create", tags=["Student Organization"])
def student_Organization_Create(data: StudentOrganizationData, db: Session = Depends(get_db)):
    # Check if the organization already exists
    existing_organization = db.query(StudentOrganization).filter(StudentOrganization.OrganizationName == data.organization_name).first()
    if existing_organization:
        return JSONResponse(status_code=400, content={"detail": "Organization already exists."})
    
    organization = StudentOrganization(
        OrganizationLogo='',
        OrganizationName=data.organization_name,
        OrganizationMemberRequirements=data.organization_requirements,
        AdviserImage='',
        AdviserName=data.organization_adviser_name,
        Vision=data.organization_vision,
        Mission=data.organization_mission,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(organization)
    db.commit()

    organization_logo_tag = 'OrganizationLogo' + str(organization.StudentOrganizationId)
    adviser_image_tag = 'AdviserImage' + str(organization.StudentOrganizationId)

    # Upload the organization logo to cloudinary
    upload_result1 = cloudinary.uploader.upload(data.organization_logo,
                                        public_id = f"StudentOrganization/{data.organization_name + str(organization.StudentOrganizationId)}/Logo",
                                        tags=[organization_logo_tag])
    
    # Upload the organization adviser image to cloudinary
    upload_result2 = cloudinary.uploader.upload(data.organization_adviser_image,
                                        public_id = f"StudentOrganization/{data.organization_name + str(organization.StudentOrganizationId)}/Adviser",
                                        tags=[adviser_image_tag])
    
    organization.OrganizationLogo = organization_logo_tag
    organization.AdviserImage = adviser_image_tag

    db.commit()
            
    # Create the officers
    for officer in data.officers:
        new_officer = OrganizationOfficer(
            StudentOrganizationId=organization.StudentOrganizationId,
            StudentNumber=officer.student_number,
            Position=officer.position,
            Image='',
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(new_officer)
        db.commit()

        officer_image_tag = 'OrganizationOfficer' + str(new_officer.OrganizationOfficerId)

        # uplaod the officer image to cloudinary
        upload_result = cloudinary.uploader.upload(officer.image,
                                        public_id = f"StudentOrganization/{data.organization_name + str(organization.StudentOrganizationId)}/Officers/{officer.student_number}",
                                        tags=[officer_image_tag])

        new_officer.Image = officer_image_tag
        db.commit()

    # Create the members
    for member in data.members:
        new_member = OrganizationMember(
            StudentOrganizationId=organization.StudentOrganizationId,
            StudentNumber=member.student_number,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(new_member)
        db.commit()

    return {"message": "Organization created successfully."}

#################################################################
""" Organization Officer Table APIs """

""" ** GET Methods: All about Organization Officers APIs ** """
@router.get("/organization/officer/all", tags=["Organization Officer"])
def get_All_Organization_Officer(db: Session = Depends(get_db)):
    try:
        officers = db.query(OrganizationOfficer).order_by(OrganizationOfficer.OrganizationOfficerId).all()
        return {"officers": [officer.to_dict() for officer in officers]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all organization officers from the database"})
    
@router.get("/organization/officer/existing/{student_number}", tags=["Organization Officer"])
def get_Organization_Officer_By_Student_Number(student_number: str, db: Session = Depends(get_db)):
    try:
        officer = db.query(OrganizationOfficer).filter(OrganizationOfficer.StudentNumber == student_number).first()
        
        if not officer:
            return {"response": False}
        
        return {"response": True}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching the organization officer from the database"})
    
@router.get("/organization/officer/{student_organization_id}", tags=["Organization Officer"])
def get_Organization_Officer_By_Student_Organization_Id(student_organization_id: int, db: Session = Depends(get_db)):
    try:
        officers = db.query(OrganizationOfficer).filter(OrganizationOfficer.StudentOrganizationId == student_organization_id).order_by(OrganizationOfficer.OrganizationOfficerId).all()
        return {"officers": [officer.to_dict() for officer in officers]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all organization officers from the database"})

""" ** POST Methods: All about Organization Officers APIs ** """

#################################################################
""" Organization Member Table APIs """

""" ** GET Methods: All about Organization Members APIs ** """
@router.get("/organization/member/all", tags=["Organization Member"])
def get_All_Organization_Member(db: Session = Depends(get_db)):
    try:
        members = db.query(OrganizationMember).order_by(OrganizationMember.OrganizationMemberId).all()
        return {"members": [member.to_dict() for member in members]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all organization members from the database"})
    
@router.get("/organization/member/existing/{student_number}", tags=["Organization Member"])
def get_Organization_Member_By_Student_Number(student_number: str, db: Session = Depends(get_db)):
    try:
        member = db.query(OrganizationMember).filter(OrganizationMember.StudentNumber == student_number).first()
        
        if not member:
            return {"response": False}
        
        return {"response": True}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching the organization member from the database"})
    
#################################################################
""" Election Table APIs """

class ElectionInfoData(BaseModel):
    election_name: str
    election_type: int
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
            
            # Get the StudentOrganizationName of the election from the StudentOrganization table
            student_organization = db.query(StudentOrganization).filter(StudentOrganization.StudentOrganizationId == election.StudentOrganizationId).first()
            election_dict["StudentOrganizationName"] = student_organization.OrganizationName if student_organization else ""

            # Get the OrganizationMemberRequirement of the election from the StudentOrganization table
            student_organization = db.query(StudentOrganization).filter(StudentOrganization.StudentOrganizationId == election.StudentOrganizationId).first()
            election_dict["OrganizationMemberRequirement"] = student_organization.OrganizationMemberRequirements if student_organization else ""
           
            # Get the CreatedElectionPositions of the election then append it to the election_dict
            positions = db.query(CreatedElectionPosition).filter(CreatedElectionPosition.ElectionId == election.ElectionId).all()
            election_dict["Positions"] = [position.to_dict(i+1) for i, position in enumerate(positions)]

            # Determine what election period
            now = datetime.now()
            if now < election.CoCFilingStart:
                election_dict["ElectionPeriod"] = "Pre-Election"
            elif now >= election.CoCFilingStart and now <= election.CoCFilingEnd:
                election_dict["ElectionPeriod"] = "Filing Period"
            elif now >= election.CampaignStart and now <= election.CampaignEnd:
                election_dict["ElectionPeriod"] = "Campaign Period"
            elif now >= election.VotingStart and now <= election.VotingEnd:
                election_dict["ElectionPeriod"] = "Voting Period"
            elif now >= election.AppealStart and now <= election.AppealEnd:
                election_dict["ElectionPeriod"] = "Appeal Period"
            else:
                election_dict["ElectionPeriod"] = "Post-Election"

            elections_with_creator.append(election_dict)

        return {"elections": elections_with_creator}

    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all elections from the database"})

@router.get("/election/all/is-student-voted", tags=["Election"])
def get_All_Election_Is_Student_Voted(student_number: str, db: Session = Depends(get_db)):
    try:
        # Check if the student has voted in the election
        elections = db.query(Election).order_by(Election.ElectionId).all()
        elections_with_creator = []

        for i, election in enumerate(elections):
            creator = db.query(Student).filter(Student.StudentNumber == election.CreatedBy).first()
            election_dict = election.to_dict(i+1)
            election_dict["CreatedByName"] = (creator.FirstName + ' ' + (creator.MiddleName + ' ' if creator.MiddleName else '') + creator.LastName) if creator else ""
            
            # Return the OrganizationMemberRequirement of the election from the StudentOrganization table
            student_organization = db.query(StudentOrganization).filter(StudentOrganization.StudentOrganizationId == election.StudentOrganizationId).first()
            election_dict["OrganizationMemberRequirement"] = student_organization.OrganizationMemberRequirements if student_organization else ""

            # Get the CreatedElectionPositions of the election then append it to the election_dict
            positions = db.query(CreatedElectionPosition).filter(CreatedElectionPosition.ElectionId == election.ElectionId).all()
            election_dict["Positions"] = [position.to_dict(i+1) for i, position in enumerate(positions)]

            elections_with_creator.append(election_dict)
            
            # Check if the student has voted in the election
            student_voted = db.query(VotingsTracker).filter(VotingsTracker.ElectionId == election.ElectionId, VotingsTracker.StudentNumber == student_number).first()
            election_dict["IsStudentVoted"] = True if student_voted else False

        return {"elections": elections_with_creator}
    
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all elections from the database"})
    
@router.get("/election/view/{id}", tags=["Election"])
def get_Election_By_Id(id: int, db: Session = Depends(get_db)):
    try:
        election = db.query(Election).get(id)

        if not election:
            return JSONResponse(status_code=404, content={"detail": "Election not found"})

        positions = db.query(CreatedElectionPosition).filter(CreatedElectionPosition.ElectionId == id).order_by(CreatedElectionPosition.CreatedElectionPositionId).all()
        student_organization_name = db.query(StudentOrganization).filter(StudentOrganization.StudentOrganizationId == election.StudentOrganizationId).first().OrganizationName

        organiztion_member_requirement = db.query(StudentOrganization).filter(StudentOrganization.StudentOrganizationId == election.StudentOrganizationId).first().OrganizationMemberRequirements

        election_count = db.query(Election).count()
        return {"election": election.to_dict(election_count),
                "student_organization_name": student_organization_name,
                "organization_member_requirement": organiztion_member_requirement,
                "positions": [position.to_dict(i+1) for i, position in enumerate(positions)]
                }
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching election from the database"})

@router.get("/election/position/reusable/all", tags=["Election"])    
def get_All_Election_Position_Reusable(db: Session = Depends(get_db)):
    try:
        positions = db.query(SavedPosition).order_by(SavedPosition.SavedPositionId).all()
        return {"positions": [position.to_dict() for position in positions]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all positions from the database"})

@router.get("/election/{id}/approved/coc/all", tags=["Election"])
def get_All_Approved_Candidates_CoC_By_Election_Id(id: int, db: Session = Depends(get_db)):
    try:
        cocs = db.query(CoC).filter(CoC.ElectionId == id, CoC.Status == "Approved").order_by(CoC.CoCId).all()

        # Get the student row from student table using the student number in the coc
        cocs_with_student = []
        for i, coc in enumerate(cocs):
            student = db.query(Student).filter(Student.StudentNumber == coc.StudentNumber).first()
            coc_dict = coc.to_dict(i+1)
            coc_dict["Student"] = student.to_dict() if student else {}

            # Get the party list name from partylist table using the partylist id in the coc
            if coc.PartyListId:
                partylist = db.query(PartyList).filter(PartyList.PartyListId == coc.PartyListId).first()
                coc_dict["PartyListName"] = partylist.PartyListName if partylist else ""

            # Get the display photo from cloudinary using the coc.displayphoto resources by tag in cloudinary
            try:
                display_photo = resources_by_tag(coc.DisplayPhoto)
                coc_dict["DisplayPhoto"] = display_photo["resources"][0]["secure_url"] if display_photo else ""
            except Exception as e:
                print(f"Error fetching image from Cloudinary: {e}")
                coc_dict["DisplayPhoto"] = ""

            cocs_with_student.append(coc_dict)

        return {"cocs": cocs_with_student}

    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all approved coc from the database"})
    

""" ** POST Methods: All about election APIs ** """
@router.post("/election/create", tags=["Election"])
def save_election(election_data: CreateElectionData, db: Session = Depends(get_db)):
    new_election = Election(ElectionName=election_data.election_info.election_name,
                            StudentOrganizationId=election_data.election_info.election_type,
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

    new_election_analytics = ElectionAnalytics(ElectionId=new_election.ElectionId,
                                                AbstainCount=0,
                                                VotesCount=0,
                                                created_at=datetime.now(), 
                                                updated_at=datetime.now())
    db.add(new_election_analytics)
    db.commit()

    for position in election_data.positions:
        new_position = CreatedElectionPosition(ElectionId=new_election.ElectionId,
                                                PositionName=position.value,
                                                PositionQuantity=position.quantity,
                                                created_at=datetime.now(), 
                                                updated_at=datetime.now())
        db.add(new_position)
        db.commit()

    # Schedule the get_winners function to run at election.VotingEnd
    trigger = DateTrigger(run_date=new_election.VotingEnd)
    scheduler.add_job(gather_winners_by_election_id, trigger=trigger, id=f'gather_winners{new_election.ElectionId}', args=[new_election.ElectionId])

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

def delete_rows(db: Session, table, election_id: int):
    rows = db.query(table).filter(table.ElectionId == election_id).all()
    for row in rows:
        db.delete(row)
    db.commit()

@router.post("/election/delete", tags=["Election"])
def delete_Election(data: ElectionDelete, db: Session = Depends(get_db)):
    election = db.query(Election).filter(Election.ElectionId == data.id).first()
    if not election:
        return {"error": "Election not found"}

    # DELETE ALL REFERENCED ROWS with the election id
    tables = [CreatedElectionPosition, CoC, ElectionAnalytics, Candidates, PartyList, RatingsTracker, VotingsTracker]
    for table in tables:
        delete_rows(db, table, data.id)

    # FINALLY DELETE ELECTION with the election id
    db.delete(election)
    db.commit()

    return {"message": f"Election {election.ElectionName} was deleted successfully."}

#################################################################
""" Announcement Table APIs """

class AnnouncementDeleteData(BaseModel):
    id: int

""" ** GET Methods: Announcement Table APIs ** """

@router.get("/announcement/all", tags=["Announcement"])
def get_All_Announcement(include_images: Optional[bool] = False, db: Session = Depends(get_db)):
    try:
        announcements = db.query(Announcement).order_by(Announcement.AnnouncementId).all() 
        return {"announcements": [announcement.to_dict(i+1, include_images=include_images) for i, announcement in enumerate(announcements)]} # Return the row number as well
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all announcements from the database"})
    
@router.get("/announcement/{type}", tags=["Announcement"])
def get_Announcement_By_Type(type: str, include_images: Optional[bool] = False, db: Session = Depends(get_db)):
    try:
        announcements = db.query(Announcement).filter(Announcement.AnnouncementType == type).order_by(Announcement.AnnouncementId).all()
        return {"announcements": [announcement.to_dict(i+1, include_images=include_images) for i, announcement in enumerate(announcements)]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching announcements from the database"})
    
@router.get("/announcement/get/{id}", tags=["Announcement"])
def get_Announcement_By_Id(id: int, include_images: Optional[bool] = False, db: Session = Depends(get_db)):
    try:
        announcement = db.query(Announcement).get(id)

        if not announcement:
            return JSONResponse(status_code=404, content={"detail": "Announcement not found"})

        return {"announcement": announcement.to_dict(include_images=include_images)}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching announcement from the database"})
    
@router.get("/announcement/get/attachment/{id}", tags=["Announcement"])
def get_Announcement_Attachment_By_Id(id: int, db: Session = Depends(get_db)):
    try:
        announcement = db.query(Announcement).get(id)

        if not announcement:
            return JSONResponse(status_code=404, content={"detail": "Announcement not found"})

        tag_name = announcement.AttachmentImage

        if tag_name:
            try:
                # Search for images with the tag using the Admin API
                response = resources_by_tag(tag_name)

                # Get the URLs and file names of the images
                images = [{"url": resource['secure_url'], 
                        "name": resource['public_id'].split('/')[-1]} for resource in response['resources']]

                return {"images": images}
            except Exception as e:
                print(f"Error fetching image from Cloudinary: {e}")
                return {"images": []}
        
        return {"images": []}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching announcement attachment from the database"})
        
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
""" Certifications Table APIs """

class SignatoryData(BaseModel):
    name: str
    position: str

class CertificationData(BaseModel):
    title: str
    election_id: int
    date: date
    quantity: str
    signatories: List[SignatoryData]

""" ** GET Methods: Certifications Table APIs ** """
@router.get("/certification/all", tags=["Certification"])
def get_All_Certification(db: Session = Depends(get_db)):
    try:
        certifications = db.query(Certifications).order_by(Certifications.CertificationId).all()
        certifications_with_election = []

        for i, certification in enumerate(certifications):
            election = db.query(Election).filter(Election.ElectionId == certification.ElectionId).first()
            certification_dict = certification.to_dict()
            certification_dict["ElectionName"] = election.ElectionName if election else ""

            certifications_with_election.append(certification_dict)

        return {"certifications": certifications_with_election}
    
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all certifications from the database"})

""" ** POST Methods: Certifications Table APIs ** """
class SignatureLine(Flowable):
    def __init__(self, width):
        Flowable.__init__(self)
        self.width = width

    def draw(self):
        self.canv.line(self.width, 0, 0, 0)  # Start from the right and extend to the left

@router.post("/certification/create", tags=["Certification"])
def create_Certification(certification_data: CertificationData, db: Session = Depends(get_db)):
    new_certification = Certifications(Title=certification_data.title,
                                        ElectionId=certification_data.election_id,
                                        Date=certification_data.date,
                                        AdminSignatoryQuantity=certification_data.quantity,
                                        created_at=datetime.now(),
                                        updated_at=datetime.now())
    db.add(new_certification)
    db.commit()

    for signatory in certification_data.signatories:
        new_signatory = CreatedAdminSignatory(CertificationId=new_certification.CertificationId,
                                    SignatoryName=signatory.name,
                                    SignatoryPosition=signatory.position,
                                    created_at=datetime.now(),
                                    updated_at=datetime.now())
        db.add(new_signatory)
        db.commit()

    # Create the PDF
    now = datetime.now()
    pdf_name = f"Report_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(pdf_name, pagesize=letter, topMargin=36)

    # Get the default style sheet
    styles = getSampleStyleSheet()

    # Create a list to hold the PDF elements
    elements = []

    # Styles
    styles.add(ParagraphStyle(name="SchoolStyle", fontName="Californian FB", fontSize=18, alignment=TA_CENTER, spaceAfter=10))
    styles.add(ParagraphStyle(name="BranchStyle", fontSize=16, alignment=TA_CENTER, spaceAfter=18))
    styles.add(ParagraphStyle(name="TitleStyle", fontName="Times-Roman", bold=True, fontSize=24, alignment=TA_CENTER, spaceAfter=26))
    styles.add(ParagraphStyle(name="ParagraphStyle", fontName="Times-Roman", fontSize=12, alignment=TA_JUSTIFY, spaceAfter=6, leading=12, firstLineIndent=36))
    styles.add(ParagraphStyle(name="ParagraphStyle2", fontName="Times-Roman", fontSize=12, alignment=TA_LEFT, spaceAfter=6, leading=12))

    # Add the logo
    logo = Image("puplogo.png", width=100, height=100)  # Adjust the path and size as needed
    elements.append(logo)
    elements.append(Spacer(1, 12))

    school = Paragraph("Polytechnic University of the Philippines", styles["SchoolStyle"])
    elements.append(school)
    elements.append(Spacer(1, 2))

    branch = Paragraph("QUEZON CITY BRANCH", styles["BranchStyle"])
    elements.append(branch)
    elements.append(Spacer(1, 12))

    date = Paragraph('<para align="right">' + certification_data.date.strftime("%B %d, %Y") + '</para>', styles["Normal"])
    elements.append(date)
    elements.append(Spacer(1, 24))

    title = Paragraph("<b>OATH OF OFFICE</b>", styles["TitleStyle"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Add the first part of the content (justified)
    text = f'''
    \tI, <b>{certification_data.signatories[0].name.upper()}</b>, having been elected as {certification_data.signatories[0].position} of
    the Supreme Student Council of the Polytechnic University of
    the Philippines, Quezon City do solemnly swear that:
    '''
    paragraph = Paragraph(text, styles["ParagraphStyle"])
    elements.append(paragraph)
    elements.append(Spacer(1, 12))

    text = f'''
    I will maintain allegiance to the Republic of the Philippines
    I will abide by laws of the Supreme Student Council and the
            Polytechnic University Of The Philippines;
    I will perform my duties and responsibilities as {certification_data.signatories[0].position},
            and conduct myself as a true professional according to best
            of my duty knowledge and discretion.
    
    So help me God.
    '''
    paragraph = Paragraph(text, styles["ParagraphStyle2"])
    paragraph_table = Table([[text]], colWidths=[300], hAlign='CENTER')  # Adjust the column width as needed
    elements.append(paragraph_table)
    elements.append(Spacer(1, 12))

    # Add the signatures (right-aligned with a line for the signature)
    for i, signatory in enumerate(certification_data.signatories):
        # Signature line and name
        signature_line = SignatureLine(130)  # Adjust the width as needed
        signature_name = Paragraph('<para align="center">' + signatory.name + '<br/>' + signatory.position + '</para>', styles["Normal"])
        signature_table = Table([[signature_line], [signature_name]], colWidths=[140], hAlign='RIGHT')  # Adjust the column width as needed
        elements.append(signature_table)
        elements.append(Spacer(1, 28))

    # Build the PDF
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
        "message": "Certification created successfully",
        "pdf_url": upload_result['secure_url']
    })


#################################################################
## Organizations APIs ## 
class OrganizationName(BaseModel):
    name: str

""" Organization Election Table APIs """

""" ** GET Methods: All about orgnanization election APIs ** """

""" ** POST Methods: All about orgnanization election APIs ** """

#################################################################
## CoC APIs ## 

""" CoC Table APIs """

""" ** GET Methods: CoC Table APIs ** """
@router.get("/coc/all", tags=["CoC"])
def get_All_CoC(db: Session = Depends(get_db)):
    try:
        coc = db.query(CoC).order_by(CoC.CoCId).all()
        coc_dict = [coc.to_dict(i+1) for i, coc in enumerate(coc)]

        # Include the election name using the election id in the CoC dictionary
        for coc in coc_dict:
            if coc["ElectionId"]:
                election = db.query(Election).filter(Election.ElectionId == coc["ElectionId"]).first()
                coc["ElectionName"] = election.ElectionName if election else None

                # Get the studentorganizationname from studentorganization table using the election table's studentorganizationid to look at studentorganizationname
                student_organization = db.query(StudentOrganization).filter(StudentOrganization.StudentOrganizationId == election.StudentOrganizationId).first()
                coc["StudentOrganizationName"] = student_organization.OrganizationName if student_organization else None

        return {"coc": coc_dict}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all CoCs from the database"})
    
@router.get("/coc/{id}", tags=["CoC"])
def get_CoC_By_Id(id: int, db: Session = Depends(get_db)):
    try:
        coc = db.query(CoC).get(id)

        if not coc:
            return JSONResponse(status_code=404, content={"detail": "CoC not found"})
        
        # Get the student from the Student table using the student number in the CoC table
        student = db.query(Student).filter(Student.StudentNumber == coc.StudentNumber).first()
       
        # Include student details in the CoC dictionary
        coc_dict = coc.to_dict()

        # Include the election name using the election id in the CoC dictionary
        if coc.ElectionId:
            election = db.query(Election).filter(Election.ElectionId == coc.ElectionId).first()
            coc_dict["ElectionName"] = election.ElectionName if election else None

            student_organization = db.query(StudentOrganization).filter(StudentOrganization.StudentOrganizationId == election.StudentOrganizationId).first()
            coc_dict["StudentOrganizationName"] = student_organization.OrganizationName if student_organization else None

        # Include the party list name using the party list id in the CoC dictionary
        if coc.PartyListId:
            party_list = db.query(PartyList).filter(PartyList.PartyListId == coc.PartyListId).first()
            coc_dict["PartyListName"] = party_list.PartyListName if party_list else None

        # Include image URLs in the CoC dictionary from cloudinary
        try:
            if coc.DisplayPhoto:
                response = resources_by_tag(coc.DisplayPhoto)
                coc_dict["DisplayPhoto"] = response['resources'][0]['secure_url']
        except Exception as e:
            print(f"Error fetching DisplayPhoto from Cloudinary: {e}")
            coc_dict["DisplayPhoto"] = ""

        try:
            if coc.CertificationOfGrades:
                response = resources_by_tag(coc.CertificationOfGrades)
                coc_dict["CertificationOfGrades"] = response['resources'][0]['secure_url']
        except Exception as e:
            print(f"Error fetching CertificationOfGrades from Cloudinary: {e}")
            coc_dict["CertificationOfGrades"] = ""

        coc_dict["Student"] = student.to_dict() if student else None

        return {"coc": coc_dict}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching CoC from the database"})

""" ** POST Methods: All about CoC Table APIs ** """
@router.post("/coc/submit", tags=["CoC"])
async def save_CoC(election_id: int = Form(...), student_number: str = Form(...),
                   verification_code: str = Form(...), motto: Optional[str] = Form(None),
                   political_affiliation: str = Form(...), party_list: Optional[str] = Form(None),
                   position: str = Form(...), display_photo: str = Form(...),
                   display_photo_file_name : str = Form(...), certification_of_grades_file_name: str = Form(...),
                   certification_of_grades: str = Form(...), db: Session = Depends(get_db)):

    # Check if current datetime is within the filing period of the election
    election = db.query(Election).filter(Election.ElectionId == election_id).first()
    
    if election.CoCFilingStart > datetime.now() or election.CoCFilingEnd < datetime.now():
        return JSONResponse(status_code=400, content={"error": "Filing period for this election has ended."})
    
    # Check if the student exists in the database
    student = db.query(Student).filter(Student.StudentNumber == student_number).first()
    if not student:
        return JSONResponse(status_code=404, content={"error": "Student number does not exist."})
    
    # Check if verification code is correct in code table and is not expired
    code = db.query(Code).filter(Code.StudentNumber == student_number, Code.CodeType == 'Verification', Code.CodeValue == verification_code, Code.CodeExpirationDate > datetime.now()).first()
    if not code:
        return JSONResponse(status_code=400, content={"error": "Verification code is invalid or has expired."})
    
    # Check if the student has already filed a CoC for this position and is still pending or approved
    existing_coc = db.query(CoC).filter(CoC.ElectionId == election_id, CoC.StudentNumber == student_number, CoC.SelectedPositionName == position, CoC.Status.in_(['Pending', 'Approved'])).first()
    if existing_coc:
        return JSONResponse(status_code=400, content={"error": "You have already filed a CoC for this position."})
    
    # Get the partylist id if the student is running under a partylist base on the partylist name
    get_party_list = db.query(PartyList).filter(PartyList.PartyListName == party_list).first()

    if get_party_list:
        party_list = get_party_list.PartyListId
    
    new_coc = CoC(ElectionId=election_id,
                    StudentNumber=student_number,
                    VerificationCode=verification_code,
                    Motto=motto,
                    PoliticalAffiliation=political_affiliation,
                    PartyListId=party_list,
                    SelectedPositionName=position,
                    DisplayPhoto='',
                    CertificationOfGrades='',
                    Status='Pending',
                    created_at=datetime.now(),
                    updated_at=datetime.now())
    db.add(new_coc)
    db.flush() # Flush the session to get the ID of the new CoC

    if display_photo:
        # Remove the prefix of the base64 string and keep only the data
        base64_data = display_photo.split(',')[1]
        
        # Use the ID of the new CoC as the subfolder name under 'CoCs'            
        folder_name = f"CoCs/coc_{new_coc.CoCId}"
        tag_name = f'coc_display_photo_{new_coc.CoCId}'

        # Upload file to Cloudinary with the folder name in the public ID
        response = cloudinary.uploader.upload("data:image/jpeg;base64," + base64_data, public_id=f"{folder_name}/display_photo/{display_photo_file_name}", tags=[tag_name])

        # Store the tag in the DisplayPhoto column
        new_coc.DisplayPhoto = tag_name

    if certification_of_grades:
        # Remove the prefix of the base64 string and keep only the data
        base64_data = certification_of_grades.split(',')[1]
        
        # Use the ID of the new CoC as the subfolder name under 'CoCs'            
        folder_name = f"CoCs/coc_{new_coc.CoCId}"
        tag_name = f'coc_cert_grades_{new_coc.CoCId}'

        # Upload file to Cloudinary with the folder name in the public ID
        response = cloudinary.uploader.upload("data:image/jpeg;base64," + base64_data, public_id=f"{folder_name}/cert_grades/{certification_of_grades_file_name}", tags=[tag_name])

        # Store the tag in the CertificationOfGrades column
        new_coc.CertificationOfGrades = tag_name

    db.commit()

    return {
        "id": new_coc.CoCId,
        "election_id": new_coc.ElectionId,
        "student_number": new_coc.StudentNumber,
        "verification_code": new_coc.VerificationCode,
        "motto": new_coc.Motto,
        "political_affiliation": new_coc.PoliticalAffiliation,
        "party_list_id": new_coc.PartyListId,
        "position": new_coc.SelectedPositionName,
        "display_photo": new_coc.DisplayPhoto,
        "certification_of_grades": new_coc.CertificationOfGrades,
    }

# Create a queue
queue_email_coc_status = asyncio.Queue()

# Define a worker function
async def email_coc_status_wroker():
    while True:
        # Get a task from the queue
        task = await queue_email_coc_status.get()

        # Process the task
        student_number, student_email, status, position_name, election_name = task
        send_coc_status_email(student_number, student_email, status, position_name, election_name)

        # Indicate that the task is done
        queue_email_coc_status.task_done()

asyncio.create_task(email_coc_status_wroker())
    
@router.put("/coc/{id}/accept", tags=["CoC"])
async def accept_CoC(id: int, db: Session = Depends(get_db)):
    try:
        coc = db.query(CoC).get(id)

        if not coc:
            return JSONResponse(status_code=404, content={"detail": "CoC not found"})

        coc.Status = 'Approved'
        coc.updated_at = datetime.now()

        db.commit()

        # Put to the Candidates table
        new_candidate = Candidates(StudentNumber=coc.StudentNumber,
                                    ElectionId=coc.ElectionId,
                                    PartyListId=coc.PartyListId,
                                    SelectedPositionName=coc.SelectedPositionName,
                                    DisplayPhoto=coc.DisplayPhoto,
                                    created_at=datetime.now(),
                                    updated_at=datetime.now())
        
        db.add(new_candidate)
        db.commit()

        # Get the student from the Student table using the student number in the CoC table
        student = db.query(Student).filter(Student.StudentNumber == coc.StudentNumber).first()

        # Get the election from the Election table using the election id in the CoC table
        election = db.query(Election).filter(Election.ElectionId == coc.ElectionId).first()

        await queue_email_coc_status.put((student.StudentNumber, student.EmailAddress, 'Approved', coc.SelectedPositionName, election.ElectionName))

        return {"detail": "CoC id " + str(id) + " was successfully approved"}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while approving CoC in the table CoC"})
    
@router.put("/coc/{id}/reject", tags=["CoC"])
async def reject_CoC(id: int, db: Session = Depends(get_db)):
    try:
        coc = db.query(CoC).get(id)

        if not coc:
            return JSONResponse(status_code=404, content={"detail": "CoC not found"})

        coc.Status = 'Rejected'
        coc.updated_at = datetime.now()

        db.commit()

        # Get the student from the Student table using the student number in the CoC table
        student = db.query(Student).filter(Student.StudentNumber == coc.StudentNumber).first()

        # Get the election from the Election table using the election id in the CoC table
        election = db.query(Election).filter(Election.ElectionId == coc.ElectionId).first()

        await queue_email_coc_status.put((student.StudentNumber, student.EmailAddress, 'Rejected', coc.SelectedPositionName, election.ElectionName))

        return {"detail": "CoC id " + str(id) + " was successfully rejected"}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while rejecting CoC in the table CoC"})


#################################################################
## Code APIs ## 

""" Code Table APIs """
class CodeForStudent(BaseModel):
    student_number: str
    code_type: str

""" ** POST Methods: All about Code Table APIs ** """
@router.post("/code/coc/verification/generate", tags=["Code"])
def generate_Coc_Verification_Code(code_for_student:CodeForStudent, db: Session = Depends(get_db)):
    # Check if the student exists in the database
    student = db.query(Student).filter(Student.StudentNumber == code_for_student.student_number).first()
    if not student:
        return JSONResponse(status_code=404, content={"error": "Student number does not exist"})

    # Check if a code already exists with same code type for this student
    existing_code_type = db.query(Code).filter(Code.StudentNumber == code_for_student.student_number, Code.CodeType == code_for_student.code_type).first()

    # Generate a random code
    code_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    if existing_code_type:
        # If a code already exists for this student, update it
        existing_code_type.CodeValue = code_value
        existing_code_type.CodeExpirationDate = datetime.now() + timedelta(minutes=30)
        existing_code_type.updated_at = datetime.now()
    else:
        # If no code exists for this student, create a new one
        new_code = Code(StudentNumber=code_for_student.student_number, 
                        CodeValue=code_value,
                        CodeType=code_for_student.code_type,
                        CodeExpirationDate=datetime.now() + timedelta(minutes=30),
                        created_at=datetime.now(),
                        updated_at=datetime.now())
        db.add(new_code)

    # Commit the session to save the changes in the database
    db.commit()

    send_verification_code_email(student.StudentNumber, student.EmailAddress, code_value)

    # Return the new or updated code including the email address of the student
    return {
        "student_number": student.StudentNumber,
        "email_address": student.EmailAddress,
        "code_value": code_value,
        "code_type": code_for_student.code_type,
    }

@router.post("/code/ratings/verification/generate", tags=["Code"])
def generate_Ratings_Verification_Code(code_for_student:CodeForStudent, db: Session = Depends(get_db)):
    # Check if the student exists in the database
    student = db.query(Student).filter(Student.StudentNumber == code_for_student.student_number).first()

    if not student:
        return JSONResponse(status_code=404, content={"error": "Student number does not exist"})

    # Check RatinsTracker table if the student has already submitted ratings
    ratings_tracker = db.query(RatingsTracker).filter(RatingsTracker.StudentNumber == code_for_student.student_number).first()

    if ratings_tracker:
        return JSONResponse(status_code=400, content={"error": "You have already submitted your ratings"})
    
    # Check if a code already exists with same code type for this student
    existing_code_type = db.query(Code).filter(Code.StudentNumber == code_for_student.student_number, Code.CodeType == code_for_student.code_type).first()

    # Generate a random code
    code_value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    if existing_code_type:
        # If a code already exists for this student, update it
        existing_code_type.CodeValue = code_value
        existing_code_type.CodeExpirationDate = datetime.now() + timedelta(minutes=30)
        existing_code_type.updated_at = datetime.now()

    else:
        # If no code exists for this student, create a new one
        new_code = Code(StudentNumber=code_for_student.student_number, 
                        CodeValue=code_value,
                        CodeType=code_for_student.code_type,
                        CodeExpirationDate=datetime.now() + timedelta(minutes=30),
                        created_at=datetime.now(),
                        updated_at=datetime.now())
        db.add(new_code)

    # Commit the session to save the changes in the database
    db.commit()

    send_verification_code_email(student.StudentNumber, student.EmailAddress, code_value)

    # Return the new or updated code including the email address of the student
    return {
        "student_number": student.StudentNumber,
        "email_address": student.EmailAddress,
        "code_value": code_value,
        "code_type": code_for_student.code_type,
    }

@router.post("/code/ratings/verify/{code}/{type}", tags=["Code"])
def verify_Ratings_Code(code: str, type: str, db: Session = Depends(get_db)):
    # Check if the code exists in the database
    code = db.query(Code).filter(Code.CodeValue == code, Code.CodeType == type, Code.CodeExpirationDate > datetime.now()).first()

    if not code:
        return JSONResponse(status_code=404, content={"error": "Code does not exist or has expired"})
    
    # remove the code from the database
    if code:
        db.delete(code)
        db.commit()

    # return true and a message if the code is valid
    return {
        "valid": True,
    }

#################################################################
## PartyList APIs ## 

""" PartyList Table APIs """

""" ** GET Methods: Partylist Table APIs ** """
@router.get("/partylist/all", tags=["Party List"])
def get_All_PartyList(db: Session = Depends(get_db)):
    try:
        partylists = db.query(PartyList).order_by(PartyList.PartyListId).all()

        # make a dictionary of partylists
        partylists = [partylist.to_dict(i+1) for i, partylist in enumerate(partylists)]

        # return the election name using the election id in the partylist dictionary
        for partylist in partylists:
            if partylist["ElectionId"]:
                election = db.query(Election).filter(Election.ElectionId == partylist["ElectionId"]).first()
                partylist["ElectionName"] = election.ElectionName if election else None
                partylist["ElectionType"] = election.ElectionType if election else None

        return {"partylists": partylists}
        
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all partylists from the database"})
    
@router.get("/partylist/approved/all", tags=["Party List"])
def get_All_Approved_PartyList(db: Session = Depends(get_db)):
    try:
        partylists = db.query(PartyList).filter(PartyList.Status == 'Approved').order_by(PartyList.PartyListId).all()
        return {"partylists": [partylist.to_dict(i+1) for i, partylist in enumerate(partylists)]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all approved partylists from the database"})


@router.get("/partylist/election/{id}/approved/all", tags=["Party List"])
def get_All_Approved_PartyList_By_Election_Id(id: int, db: Session = Depends(get_db)):
    try:
        partylists = db.query(PartyList).filter(PartyList.ElectionId == id, PartyList.Status == 'Approved').order_by(PartyList.PartyListId).all()
        return {"partylists": [partylist.to_dict(i+1) for i, partylist in enumerate(partylists)]}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all approved partylists from the database"})
    
@router.get("/partylist/{id}/candidates/all", tags=["Party List"])
def get_All_Candidates_By_PartyList_Id(id: int, db: Session = Depends(get_db)):
    try:
        # Get all candidates in the CoC table that are approved and are running under this partylist ordered by position
        partylist_candidates = db.query(CoC).join(CreatedElectionPosition, CreatedElectionPosition.ElectionId == CoC.ElectionId).filter(CoC.PartyListId == id, 
                                                                                                                                        CoC.Status == 'Approved').order_by(CreatedElectionPosition.CreatedElectionPositionId).all()
        
        partylist_candidates_dict = []
        # Include the student full name in student table by student number in the CoC table
        for i, coc in enumerate(partylist_candidates):
            student = db.query(Student).filter(Student.StudentNumber == coc.StudentNumber).first()
            partylist_candidates_dict.append(coc.to_dict(i+1))
            partylist_candidates_dict[i]["Student"] = student.to_dict() if student else None

        # Include the display photo URL from cloudinary in the CoC dictionary
        for coc in partylist_candidates_dict:
            try:
                if coc["DisplayPhoto"]:
                    response = resources_by_tag(coc["DisplayPhoto"])
                    coc["DisplayPhoto"] = response['resources'][0]['secure_url']
            except Exception as e:
                print(f"Error fetching DisplayPhoto from Cloudinary: {e}")
                coc["DisplayPhoto"] = ""

        return {"candidates": partylist_candidates_dict}

    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all candidates from the database"})
    
@router.get("/partylist/{id}", tags=["Party List"])
def get_PartyList_By_Id(id: int, db: Session = Depends(get_db)):
    try:
        partylist = db.query(PartyList).get(id)

        if not partylist:
            return JSONResponse(status_code=404, content={"detail": "Partylist not found"})
        
        # Include image URL from cloudinary
        try:
            if partylist.ImageAttachment:
                response = resources_by_tag(partylist.ImageAttachment)
                partylist.ImageAttachment = response['resources'][0]['secure_url']
        except Exception as e:
            print(f"Error fetching ImageAttachment from Cloudinary: {e}")
            partylist.ImageAttachment = ""

        return {"partylist": partylist.to_dict()}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching partylist from the database"})
    
# check if partylist is not yet claimed by name
@router.get("/partylist/is-taken/{name}", tags=["Party List"])
def get_PartyList_By_Name(name: str, db: Session = Depends(get_db)):
    try:
        # Ignore case
        partylist = db.query(PartyList).filter(func.lower(PartyList.PartyListName) == func.lower(name)).first()

        if not partylist:
            return False

        return True
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching partylist from the database"})

# get partylists by election id
@router.get("/partylist/election/{election_id}", tags=["Party List"])
def get_PartyList_By_Election_Id(election_id: int, db: Session = Depends(get_db)):
    try:
        partylists = db.query(PartyList).filter(PartyList.ElectionId == election_id).order_by(PartyList.PartyListId).all()

        # make a dictionary of partylists
        partylists = [partylist.to_dict(i+1) for i, partylist in enumerate(partylists)]

        # return the election name using the election id in the partylist dictionary
        for partylist in partylists:
            if partylist["ElectionId"]:
                election = db.query(Election).filter(Election.ElectionId == partylist["ElectionId"]).first()
                partylist["ElectionName"] = election.ElectionName if election else None
                partylist["ElectionType"] = election.ElectionType if election else None

        return {"partylists": partylists}
        
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all partylists from the database"})


""" ** POST Methods: All about Partylist Table APIs ** """

@router.post("/partylist/submit", tags=["Party List"])
async def save_PartyList(election_id: int = Form(...), party_name: str = Form(...), 
                         email_address: str = Form(...), cellphone_number: str = Form(...), 
                         description: str = Form(...), mission: str = Form(...),
                         vision: str = Form(...), platforms: str = Form(...),
                         image_attachment: Optional[str] = Form(None), image_file_name: Optional[str] = Form(None),
                         video_attachment: Optional[str] = Form(None),
                         db: Session = Depends(get_db)):
    
    # Check if current datetime is within the filing period of the election
    election = db.query(Election).filter(Election.ElectionId == election_id).first()

    if election.CoCFilingStart > datetime.now() or election.CoCFilingEnd < datetime.now():
        return JSONResponse(status_code=400, content={"error": "Filing period for this election has ended."})
    
    new_partylist = PartyList(ElectionId=election_id,
                            PartyListName=party_name, 
                            EmailAddress=email_address,
                            CellphoneNumber=cellphone_number, 
                            Description=description,
                            Mission=mission,
                            Vision=vision,
                            Platforms=platforms,
                            ImageAttachment='' if image_attachment else None,  # Initialize with an empty string
                            VideoAttachment=video_attachment,
                            Status='Pending',
                            created_at=datetime.now(), 
                            updated_at=datetime.now())
    db.add(new_partylist)
    db.commit()

    if image_attachment:
        # Remove the prefix of the base64 string and keep only the data
        base64_data = image_attachment.split(',')[1]
        
        # Use the ID of the new partylist as the subfolder name under 'Partylists'            
        folder_name = f"Partylists/partylist_{new_partylist.PartyListId}"

        # Upload file to Cloudinary with the folder name in the public ID
        response = cloudinary.uploader.upload("data:image/jpeg;base64," + base64_data, public_id=f"{folder_name}/{image_file_name}", tags=[f'partylist_{new_partylist.PartyListId}'])

        # Store the tag in the ImageAttachment column
        new_partylist.ImageAttachment = f'partylist_{new_partylist.PartyListId}'
        db.commit()

    return {
        "id": new_partylist.PartyListId,
        "party_name": new_partylist.PartyListName,
        "email_address": new_partylist.EmailAddress,
        "cellphone_number": new_partylist.CellphoneNumber,
        "description": new_partylist.Description,
        "mission": new_partylist.Mission,
        "vision": new_partylist.Vision,
        "platforms": new_partylist.Platforms,
        "image_attachment": new_partylist.ImageAttachment,
        "video_attachment": new_partylist.VideoAttachment,
    }

# Create a queue
queue_email_partylist_status = asyncio.Queue()

# Define a worker function
async def email_partylist_status_wroker():
    while True:
        # Get a task from the queue
        task = await queue_email_partylist_status.get()

        # Process the task
        party_email, status, partylist_name, election_name = task
        send_partylist_status_email(party_email, status, partylist_name, election_name)

        # Indicate that the task is done
        queue_email_partylist_status.task_done()

asyncio.create_task(email_partylist_status_wroker())

@router.put("/partylist/{id}/accept", tags=["Party List"])
async def accept_PartyList(id: int, db: Session = Depends(get_db)):
    try:
        partylist = db.query(PartyList).get(id)

        if not partylist:
            return JSONResponse(status_code=404, content={"detail": "Partylist not found"})

        partylist.Status = 'Approved'
        partylist.updated_at = datetime.now()

        db.commit()

        # Get the election from the Election table using the election id in the CoC table
        election = db.query(Election).filter(Election.ElectionId == partylist.ElectionId).first()

        await queue_email_partylist_status.put((partylist.EmailAddress, 'Approved', partylist.PartyListName, election.ElectionName))

        return {"detail": "Partylist id " + str(id) + " was successfully approved"}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while approving partylist in the table PartyList"})
    
@router.put("/partylist/{id}/reject", tags=["Party List"])
async def reject_PartyList(id: int, db: Session = Depends(get_db)):
    try:
        partylist = db.query(PartyList).get(id)

        if not partylist:
            return JSONResponse(status_code=404, content={"detail": "Partylist not found"})

        partylist.Status = 'Rejected'
        partylist.updated_at = datetime.now()

        db.commit()

        # Get the election from the Election table using the election id in the CoC table
        election = db.query(Election).filter(Election.ElectionId == partylist.ElectionId).first()

        await queue_email_partylist_status.put((partylist.EmailAddress, 'Rejected', partylist.PartyListName, election.ElectionName))

        return {"detail": "Partylist id " + str(id) + " was successfully rejected"}
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while rejecting partylist in the table PartyList"})
    
#################################################################
## Candidates APIs ## 

""" Candidates Table APIs """
class Rating(BaseModel):
    candidate_student_number: str
    rating: int = Field(0)

class RatingList(BaseModel):
    election_id: int
    rater_student_number: str
    ratings: List[Rating]

""" ** GET Methods: Candidates Table APIs ** """
@router.get("/candidates/all", tags=["Candidates"])
def get_All_Candidates(db: Session = Depends(get_db)):
    try:
        candidates = db.query(Candidates).order_by(Candidates.CandidateId).all()

        # Get the student row from student table using the student number in the candidate
        candidates_with_student = []
        for i, candidate in enumerate(candidates):
            student = db.query(Student).filter(Student.StudentNumber == candidate.StudentNumber).first()
            candidate_dict = candidate.to_dict(i+1)
            candidate_dict["Student"] = student.to_dict() if student else {}

            # Get the party list name from partylist table using the partylist id in the candidate
            if candidate.PartyListId:
                partylist = db.query(PartyList).filter(PartyList.PartyListId == candidate.PartyListId).first()
                candidate_dict["PartyListName"] = partylist.PartyListName if partylist else ""

            # Get the motto from coc table using the student number in the candidate
            if candidate.StudentNumber:
                coc = db.query(CoC).filter(CoC.StudentNumber == candidate.StudentNumber, CoC.ElectionId == candidate.ElectionId).first()
                candidate_dict["Motto"] = coc.Motto if coc else ""

            # Get the display photo from cloudinary using the candidate.displayphoto resources by tag in cloudinary
            try:
                display_photo = resources_by_tag(candidate.DisplayPhoto)
                candidate_dict["DisplayPhoto"] = display_photo["resources"][0]["secure_url"] if display_photo else ""
            except Exception as e:
                print(f"Error fetching DisplayPhoto from Cloudinary: {e}")
                candidate_dict["DisplayPhoto"] = ""
            
            candidates_with_student.append(candidate_dict)

        return {"candidates": candidates_with_student}

    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all candidates from the database"})
    
@router.get("/candidates/election/{id}/all", tags=["Candidates"])
def get_All_Candidates_By_Election_Id(id: int, db: Session = Depends(get_db)):
    try:
        candidates = db.query(Candidates).filter(Candidates.ElectionId == id).order_by(Candidates.CandidateId).all()

        # Get the student row from student table using the student number in the candidate
        candidates_with_student = []
        for i, candidate in enumerate(candidates):
            student = db.query(Student).filter(Student.StudentNumber == candidate.StudentNumber).first()
            candidate_dict = candidate.to_dict(i+1)
            candidate_dict["Student"] = student.to_dict() if student else {}

            # Get the party list name from partylist table using the partylist id in the candidate
            if candidate.PartyListId:
                partylist = db.query(PartyList).filter(PartyList.PartyListId == candidate.PartyListId).first()
                candidate_dict["PartyListName"] = partylist.PartyListName if partylist else ""

            # Get the motto from coc table using the student number in the candidate
            if candidate.StudentNumber:
                coc = db.query(CoC).filter(CoC.StudentNumber == candidate.StudentNumber, CoC.ElectionId == candidate.ElectionId).first()
                candidate_dict["Motto"] = coc.Motto if coc else ""

            # Get the display photo from cloudinary using the candidate.displayphoto resources by tag in cloudinary
            try:
                display_photo = resources_by_tag(candidate.DisplayPhoto)
                candidate_dict["DisplayPhoto"] = display_photo["resources"][0]["secure_url"] if display_photo else ""
            except Exception as e:
                print(f"Error fetching DisplayPhoto from Cloudinary: {e}")
                candidate_dict["DisplayPhoto"] = ""
            
            candidates_with_student.append(candidate_dict)

        return {"candidates": candidates_with_student}

    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all candidates from the database"})
    
@router.get("/candidates/election/per-position/{id}/all", tags=["Candidates"])
def get_All_Candidates_By_Election_Id_Per_Position(id: int, db: Session = Depends(get_db)):
    try:
        # Get the candidates and order by CreatedElectionPositionId
        candidates = db.query(Candidates).join(
            CreatedElectionPosition, 
            and_(
                Candidates.SelectedPositionName == CreatedElectionPosition.PositionName,
                Candidates.ElectionId == id
            )
        ).order_by(CreatedElectionPosition.CreatedElectionPositionId).all()

        # Get the student row from student table using the student number in the candidate
        candidates_grouped_by_position = {}
        for i, candidate in enumerate(candidates):
            student = db.query(Student).filter(Student.StudentNumber == candidate.StudentNumber).first()
            candidate_dict = candidate.to_dict(i+1)
            candidate_dict["Student"] = student.to_dict() if student else {}

            # Get the party list name from partylist table using the partylist id in the candidate
            if candidate.PartyListId:
                partylist = db.query(PartyList).filter(PartyList.PartyListId == candidate.PartyListId).first()
                candidate_dict["PartyListName"] = partylist.PartyListName if partylist else ""

            # Get the motto from coc table using the student number in the candidate
            if candidate.StudentNumber:
                coc = db.query(CoC).filter(CoC.StudentNumber == candidate.StudentNumber, CoC.ElectionId == candidate.ElectionId).first()
                candidate_dict["Motto"] = coc.Motto if coc else ""

            # Get the display photo from cloudinary using the candidate.displayphoto resources by tag in cloudinary
            try:
                display_photo = resources_by_tag(candidate.DisplayPhoto)
                candidate_dict["DisplayPhoto"] = display_photo["resources"][0]["secure_url"] if display_photo else ""
            except Exception as e:
                print(f"Error fetching DisplayPhoto from Cloudinary: {e}")
                candidate_dict["DisplayPhoto"] = ""

            # Group by SelectedPositionName
            position_name = candidate.SelectedPositionName

            # Get the PositionQuantity from CreatedElectionPosition table
            created_election_position = db.query(CreatedElectionPosition).filter(and_(CreatedElectionPosition.ElectionId == id, CreatedElectionPosition.PositionName == position_name)).first()
            candidate_dict["PositionQuantity"] = created_election_position.PositionQuantity 

            if position_name not in candidates_grouped_by_position:
                candidates_grouped_by_position[position_name] = []
                

            candidates_grouped_by_position[position_name].append(candidate_dict)

        return {"candidates": candidates_grouped_by_position}

    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all candidates from the database"})

""" ** POST Methods: All about Candidates Table APIs ** """
@router.post("/candidates/ratings/submit", tags=["Candidates"])
def save_Candidate_Ratings(rating_list: RatingList, db: Session = Depends(get_db)):

    # Check if campaign period has not yet ended
    election = db.query(Election).filter(Election.ElectionId == rating_list.election_id).first()

    # check for ended campaign period only 
    if election.CampaignEnd < datetime.now():
        return JSONResponse(status_code=400, content={"error": "Rating/Campaign period for this election has ended."})

    # Check if the student has already rated this election
    existing_rating = db.query(RatingsTracker).filter(RatingsTracker.StudentNumber == rating_list.rater_student_number, RatingsTracker.ElectionId == rating_list.election_id).first()

    if existing_rating:
        return JSONResponse(status_code=400, content={"error": "You have already rated this election"})

    for rating in rating_list.ratings:
        # Check if the student exists in the database
        student = db.query(Student).filter(Student.StudentNumber == rating.candidate_student_number).first()

        if not student:
            return JSONResponse(status_code=404, content={"error": "Student number does not exist"})

        # Check if the election exists in the database
        election = db.query(Election).filter(Election.ElectionId == rating_list.election_id).first()

        if not election:
            return JSONResponse(status_code=404, content={"error": "Election does not exist"})

        # Update the ratings of the candidate in the Candidates table
        candidate = db.query(Candidates).filter(Candidates.StudentNumber == rating.candidate_student_number, Candidates.ElectionId == rating_list.election_id).first()

        if not candidate:
            return JSONResponse(status_code=404, content={"error": "Candidate does not exist"})

        # Increment the number of ratings of the candidate by ratings received
        candidate.Rating += rating.rating

        if rating.rating > 0:
            candidate.TimesRated += 1
            
        candidate.updated_at = datetime.now()

        db.commit()

    # Add a new record in the RatingsTracker table
    new_rating = RatingsTracker(StudentNumber=rating_list.rater_student_number,
                                        ElectionId=rating_list.election_id,
                                        created_at=datetime.now(),
                                        updated_at=datetime.now())

    db.add(new_rating)
    db.commit()

    return {"response": "success"}

#################################################################
## VotingsTracker APIs ## 

class Votes(BaseModel):
    candidate_student_number: str

class VotesList(BaseModel):
    election_id: int
    voter_student_number: str
    votes: List[Votes]

""" VotingsTracker Table APIs """

""" ** GET Methods: VotingsTracker Table APIs ** """

@router.get("/votings/election/{id}/{position_name}/results", tags=["Votings"])
def get_Results_By_Election_Id_And_Position_Name(id: int, position_name: str, db: Session = Depends(get_db)):
    try:
        # Rank the candidates by votes received
        candidates = db.query(Candidates).filter(Candidates.ElectionId == id, Candidates.SelectedPositionName == position_name).order_by(Candidates.Votes.desc()).all()

        # Calculate the total number of votes
        total_votes = sum(candidate.Votes for candidate in candidates)

        # Calculate the ranking, votes, and percentage of votes for each candidate
        results = []
        for i, candidate in enumerate(candidates):
            # Get the first name middle name if it exist and last name of candidate by studentnumber from student table
            student = db.query(Student).filter(Student.StudentNumber == candidate.StudentNumber).first()
            full_name = student.FirstName + " " + student.MiddleName + " " + student.LastName if student.MiddleName else student.FirstName + " " + student.LastName

            # Get the candidate photo from cloudinary using the candidate.displayphoto resources by tag in cloudinary
            try:
                display_photo = resources_by_tag(candidate.DisplayPhoto)
                display_photo_url = display_photo["resources"][0]["secure_url"] if display_photo else ""
            except Exception as e:
                print(f"Error fetching DisplayPhoto from Cloudinary: {e}")
                display_photo_url = ""

            results.append({
                'rank': i + 1,
                'candidate_student_number': candidate.StudentNumber,
                'full_name': full_name,
                'display_photo': display_photo_url,
                'votes': candidate.Votes,
                'percentage': (candidate.Votes / total_votes) * 100 if total_votes > 0 else 0,
            })

        return results
    except:
        return JSONResponse(status_code=500, content={"detail": "Error while fetching all candidates from the database"})

""" ** POST Methods: All about VotingsTracker Table APIs ** """

@router.post("/votings/submit", tags=["Votings"])
def save_Votes(votes_list: VotesList, db: Session = Depends(get_db)):
    # Check if voting period has not yet ended
    election = db.query(Election).filter(Election.ElectionId == votes_list.election_id).first()

    # check for ended voting period only 
    if election.VotingEnd < datetime.now():
        return JSONResponse(status_code=400, content={"error": "Voting period for this election has ended."})

    # Check if the student has already voted this election
    existing_vote = db.query(VotingsTracker).filter(VotingsTracker.StudentNumber == votes_list.voter_student_number, VotingsTracker.ElectionId == votes_list.election_id).first()

    if existing_vote:
        return JSONResponse(status_code=400, content={"error": "You have already voted for this election."})
    
    election_analytics = db.query(ElectionAnalytics).filter(ElectionAnalytics.ElectionId == votes_list.election_id).first()

    for vote in votes_list.votes:
        if vote.candidate_student_number == 'abstain':

            # +1 the abstaincount in ElectionAnalytics table
            election_analytics.AbstainCount += 1
            election_analytics.updated_at = datetime.now()

            db.commit()
            continue

        # Check if the student exists in the database
        student = db.query(Student).filter(Student.StudentNumber == vote.candidate_student_number).first()

        if not student:
            return JSONResponse(status_code=404, content={"error": "Student number does not exist"})

        # Check if the election exists in the database
        election = db.query(Election).filter(Election.ElectionId == votes_list.election_id).first()

        if not election:
            return JSONResponse(status_code=404, content={"error": "Election does not exist"})

        # Update the votes of the candidate in the Candidates table
        candidate = db.query(Candidates).filter(Candidates.StudentNumber == vote.candidate_student_number, Candidates.ElectionId == votes_list.election_id).first()

        if not candidate:
            return JSONResponse(status_code=404, content={"error": "Candidate does not exist"})

        # Increment the number of votes of the candidate by votes received
        candidate.Votes += 1
        candidate.updated_at = datetime.now()

        # +1 the vote count in ElectionAnalytics table
        election_analytics.VotesCount += 1
        election_analytics.updated_at = datetime.now()

        db.commit()

    # Add a new record in the VotingsTracker table
    new_vote = VotingsTracker(StudentNumber=votes_list.voter_student_number,
                                        ElectionId=votes_list.election_id,
                                        created_at=datetime.now(),
                                        updated_at=datetime.now())

    db.add(new_vote)
    db.commit()

    return {"response": "success"}

#################################################################
## ElectionWinners APIs ## 

""" ElectionWinners Table APIs """

def gather_winners_by_election_id(election_id: int):
    db = SessionLocal()  # create a new session
    election = db.query(Election).filter(Election.ElectionId == election_id).first()

    # Check if winners for this election have already been added
    existing_winners = db.query(ElectionWinners).filter(ElectionWinners.ElectionId == election_id).first()
    if existing_winners is not None:
        print("Winners for this election have already been added.")
        return
    
    if datetime.now() > election.VotingEnd:
        # Gather all candidates
        all_candidates = db.query(Candidates).filter(Candidates.ElectionId == election.ElectionId).all()

        # Count the number of candidates for each position
        candidate_counts = defaultdict(int)
        for candidate in all_candidates:
            candidate_counts[candidate.SelectedPositionName] += 1

        # Get the PositionQuantity for each position in the current election
        position_quantities = {position.PositionName: int(position.PositionQuantity) for position in db.query(CreatedElectionPosition).filter(CreatedElectionPosition.ElectionId == election.ElectionId)}

        # Initialize a dictionary to store the candidates with the highest votes for each position
        candidates_with_highest_votes = defaultdict(list)
        for candidate in all_candidates:
            # Check if we have already selected the required number of candidates for this position
            if len(candidates_with_highest_votes[candidate.SelectedPositionName]) < position_quantities[candidate.SelectedPositionName]:
                candidates_with_highest_votes[candidate.SelectedPositionName].append(candidate)

        # Get the organization based on the election id
        organization = db.query(StudentOrganization).filter_by(StudentOrganizationId=election.StudentOrganizationId).first()
        eligible_voters = db.query(Student).filter_by(Course=organization.OrganizationMemberRequirements).count()

        # Store the winners in the ElectionWinners table
        for position, candidates in candidates_with_highest_votes.items():
            # If there's exactly one candidate for this position, check if the candidate has achieved the required vote threshold
            if candidate_counts[position] == 1:
                # Calculate the vote threshold
                vote_threshold = (eligible_voters // 2) + 1  # 50% students + 1 vote constraint

                if candidates[0].Votes >= vote_threshold:
                    winner = ElectionWinners(ElectionId=election.ElectionId, 
                                            StudentNumber=candidates[0].StudentNumber, 
                                            SelectedPositionName=position,
                                            Votes=candidates[0].Votes,
                                            created_at=datetime.now(),
                                            updated_at=datetime.now())
                    db.add(winner)
            else:  # There's more than one candidate for this position
                # The candidate with the highest votes wins
                winner = ElectionWinners(ElectionId=election.ElectionId, 
                                        StudentNumber=candidates[0].StudentNumber, 
                                        SelectedPositionName=position,
                                        Votes=candidates[0].Votes,
                                        created_at=datetime.now(),
                                        updated_at=datetime.now())
                db.add(winner)

        db.commit()

""" ** GET Methods: ElectionWinners Table APIs ** """
    
@router.get("/votings/get-winners/{election_id}", tags=["ElectionWinners"])
def get_Winners_By_Election_Id(election_id: int, db: Session = Depends(get_db)):
    election = db.query(Election).filter(Election.ElectionId == election_id).first()

    winners = db.query(ElectionWinners).join(
        CreatedElectionPosition, 
        and_(
            ElectionWinners.SelectedPositionName == CreatedElectionPosition.PositionName,
            ElectionWinners.ElectionId == election_id
        )
    ).order_by(CreatedElectionPosition.CreatedElectionPositionId).all()    

    winners_dict = []

    # Get the winner candidate details from the Candidates table
    for i, winner in enumerate(winners):
        candidate = db.query(Candidates).filter(Candidates.StudentNumber == winner.StudentNumber, Candidates.ElectionId == election_id).first()
        student = db.query(Student).filter(Student.StudentNumber == winner.StudentNumber).first()
        
        full_name = student.FirstName + " " + student.MiddleName + " " + student.LastName if student.MiddleName else student.FirstName + " " + student.LastName
        candidate_partylist = db.query(PartyList).filter(PartyList.PartyListId == candidate.PartyListId).first()

        if candidate_partylist:
            candidate_partylist_name = candidate_partylist.PartyListName
        else:
            candidate_partylist_name = "Independent"

        # Get the candidate photo from cloudinary using the candidate.displayphoto resources by tag in cloudinary
        try:
            display_photo = resources_by_tag(candidate.DisplayPhoto)
            display_photo_url = display_photo["resources"][0]["secure_url"] if display_photo else ""
        except Exception as e:
            print(f"Error fetching DisplayPhoto from Cloudinary: {e}")
            display_photo_url = ""

        winners_dict.append({
            "full_name": full_name,
            "votes": winner.Votes,
            "position": winner.SelectedPositionName,
            "partylist": candidate_partylist_name,
            "display_photo": display_photo_url if display_photo_url else "",
        })

    return {"winners": winners_dict}
        

""" ** POST Methods: All about ElectionWinners Table APIs ** """


#################################################################
## RatingsTracker APIs ## 

""" RatingsTracker Table APIs """

""" ** GET Methods: RatingsTracker Table APIs ** """

""" ** POST Methods: All about RatingsTracker Table APIs ** """

#################################################################
app.include_router(router)