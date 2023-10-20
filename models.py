from database import engine, Base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, Float, String, Date, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func

from cloudinary.api import resources_by_tag

Session = sessionmaker(bind=engine)
session = Session()

class Student(Base):
    __tablename__ = "Student"
    
    StudentId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), unique=True)
    FirstName = Column(String)
    MiddleName = Column(String, nullable=True)
    LastName = Column(String)
    EmailAddress = Column(String, unique=True)
    BirthDate = Column(Date)
    Course = Column(String)
    CurrentSemesterEnrolled = Column(String)
    YearEnrolled = Column(String)
    IsOfficer = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "StudentId": self.StudentId,
            "StudentNumber": self.StudentNumber,
            "FirstName": self.FirstName,
            "MiddleName": self.MiddleName,
            "LastName": self.LastName,
            "EmailAddress": self.EmailAddress,
            "BirthDate": self.BirthDate.isoformat() if self.BirthDate else None,
            "Course": self.Course,
            "CurrentSemesterEnrolled": self.CurrentSemesterEnrolled,
            "YearEnrolled": self.YearEnrolled,
            "IsOfficer": self.IsOfficer,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class Organization(Base):
    __tablename__ = "Organization"
    
    OrganizationId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), unique=True)
    OfficerPositionId = Column(Integer, unique=True)
    OrganizationName = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "OrganizationId": self.OrganizationId,
            "StudentNumber": self.StudentNumber,
            "OfficerPositionId": self.OfficerPositionId,
            "OrganizationName": self.OrganizationName,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class Election(Base):
    __tablename__ = "Election"
    
    ElectionId = Column(Integer, primary_key=True)
    ElectionName = Column(String)
    ElectionType = Column(String)
    ElectionStatus = Column(String)
    SchoolYear = Column(String)
    Semester = Column(String)
    CreatedBy = Column(String)

    ElectionStart = Column(DateTime)
    ElectionEnd = Column(DateTime)
    CoCFilingStart = Column(DateTime)
    CoCFilingEnd = Column(DateTime)
    CampaignStart = Column(DateTime)
    CampaignEnd = Column(DateTime)
    VotingStart = Column(DateTime)
    VotingEnd = Column(DateTime)
    AppealStart = Column(DateTime)
    AppealEnd = Column(DateTime)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self, row=None):
        return {
            "ElectionId": self.ElectionId,
            "count": row,
            "ElectionName": self.ElectionName,
            "ElectionType": self.ElectionType,
            "ElectionStatus": self.ElectionStatus,
            "SchoolYear": self.SchoolYear,
            "Semester": self.Semester,
            "CreatedBy": self.CreatedBy,

            "ElectionStart": self.ElectionStart.isoformat() if self.ElectionStart else None,
            "ElectionEnd": self.ElectionEnd.isoformat() if self.ElectionEnd else None,
            "CoCFilingStart": self.CoCFilingStart.isoformat() if self.CoCFilingStart else None,
            "CoCFilingEnd": self.CoCFilingEnd.isoformat() if self.CoCFilingEnd else None,
            "CampaignStart": self.CampaignStart.isoformat() if self.CampaignStart else None,
            "CampaignEnd": self.CampaignEnd.isoformat() if self.CampaignEnd else None,
            "VotingStart": self.VotingStart.isoformat() if self.VotingStart else None,
            "VotingEnd": self.VotingEnd.isoformat() if self.VotingEnd else None,
            "AppealStart": self.AppealStart.isoformat() if self.AppealStart else None,
            "AppealEnd": self.AppealEnd.isoformat() if self.AppealEnd else None,
            
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class CreatedElectionPosition(Base):
    __tablename__ = "CreatedElectionPosition"
    
    CreatedElectionPositionId = Column(Integer, primary_key=True)
    ElectionId = Column(Integer)
    PositionName = Column(String)
    PositionQuantity = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self, row=None):
        return {
            "CreatedElectionPositionId": self.CreatedElectionPositionId,
            "count": row,
            "ElectionId": self.ElectionId,
            "PositionName": self.PositionName,
            "PositionQuantity": self.PositionQuantity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class SavedPosition(Base):
    __tablename__ = "SavedPosition"
    
    SavedPositionId = Column(Integer, primary_key=True)
    PositionName = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "SavedPositionId": self.SavedPositionId,
            "PositionName": self.PositionName,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class Announcement(Base):
    __tablename__ = "Announcement"
    
    AnnouncementId = Column(Integer, primary_key=True)
    AnnouncementType = Column(String)
    AnnouncementTitle = Column(String)
    AnnouncementBody = Column(Text)
    AttachmentType = Column(String)
    AttachmentImage = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self, row=None, include_images=False):
        data = {
            "AnnouncementId": self.AnnouncementId,
            "count": row,
            "type": "announcement",
            "AnnouncementType": self.AnnouncementType,
            "AnnouncementTitle": self.AnnouncementTitle,
            "AnnouncementBody": self.AnnouncementBody,
            "AttachmentType": self.AttachmentType,
            "AttachmentImage": self.AttachmentImage,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

        tag_name = self.AttachmentImage
        if tag_name and include_images:
            response = resources_by_tag(tag_name)
            data['images'] = [{"url": resource['secure_url'], "name": resource['public_id'].split('/')[-1]} for resource in response['resources']]
        else:
            data['images'] = []

        return data


class Rule(Base):
    __tablename__ = "Rules"
    
    RuleId = Column(Integer, primary_key=True)
    RuleTitle = Column(String)
    RuleBody = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self, row=None):
        return {
            "RuleId": self.RuleId,
            "count": row,
            "type": "rule",
            "RuleTitle": self.RuleTitle,
            "RuleBody": self.RuleBody,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class Guideline(Base):
    __tablename__ = "Guidelines"
    
    GuideId = Column(Integer, primary_key=True)
    GuidelineTitle = Column(String)
    GuidelineBody = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self, row=None):
        return {
            "GuideId": self.GuideId,
            "count": row,
            "type": "guideline",
            "GuidelineTitle": self.GuidelineTitle,
            "GuidelineBody": self.GuidelineBody,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class AzureToken(Base):
    __tablename__ = "AzureToken"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
    expires_at = Column(Float)
    token_updates = Column(Integer, default=0)  # New column to track token updates

    def to_dict(self):
        return {
            "id": self.id,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at,
            "token_updates": self.token_updates  # Include the new column in the dictionary
        }
