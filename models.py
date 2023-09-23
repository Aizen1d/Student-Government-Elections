from database import engine, Base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, Float, String, Date, DateTime, Boolean, Text
from sqlalchemy.sql import func

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

    def to_dict(self, row=None):
        return {
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
