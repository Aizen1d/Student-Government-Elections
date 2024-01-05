from database import engine, Base
from sqlalchemy.orm import sessionmaker, relationship

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
    Year = Column(String)
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
            "Year": self.Year,
            "Course": self.Course,
            "CurrentSemesterEnrolled": self.CurrentSemesterEnrolled,
            "YearEnrolled": self.YearEnrolled,
            "IsOfficer": self.IsOfficer,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class Election(Base):
    __tablename__ = "Election"
    
    ElectionId = Column(Integer, primary_key=True)
    ElectionName = Column(String)
    StudentOrganizationId = Column(Integer, ForeignKey('StudentOrganization.StudentOrganizationId'))
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
            "StudentOrganizationId": self.StudentOrganizationId,
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
    
class Certifications(Base):
    __tablename__ = "Certifications"
    
    CertificationId = Column(Integer, primary_key=True)
    Title = Column(String)
    ElectionId = Column(Integer, ForeignKey('Election.ElectionId'))
    Date = Column(Date)
    AdminSignatoryQuantity = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "CertificationId": self.CertificationId,
            "Title": self.Title,
            "ElectionId": self.ElectionId,
            "Date": self.Date.isoformat() if self.Date else None,
            "AdminSignatoryQuantity": self.AdminSignatoryQuantity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
class CreatedAdminSignatory(Base):
    __tablename__ = "CreatedAdminSignatory"
    
    CreatedAdminSignatoryId = Column(Integer, primary_key=True)
    CertificationId = Column(Integer, ForeignKey('Certifications.CertificationId'))
    SignatoryName = Column(String)
    SignatoryPosition = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "CreatedAdminSignatory": self.CreatedAdminSignatoryId,
            "CertificationId": self.CertificationId,
            "SignatoryName": self.SignatoryName,
            "SignatoryPosition": self.SignatoryPosition,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
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

class Code(Base):
    __tablename__ = "Code"

    CodeId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), ForeignKey('Student.StudentNumber'), unique=True)
    CodeValue = Column(Text)
    CodeType = Column(String)
    CodeExpirationDate = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "CodeId": self.CodeId,
            "StudentNumber": self.StudentNumber,
            "CodeValue": self.CodeValue,
            "CodeType": self.CodeType,
            "CodeExpirationDate": self.CodeExpirationDate.isoformat() if self.CodeExpirationDate else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class StudentPassword(Base):
    __tablename__ = "StudentPassword"

    StudentPasswordId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), ForeignKey('Student.StudentNumber'), unique=True)
    Password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "StudentPasswordId": self.StudentPasswordId,
            "StudentNumber": self.StudentNumber,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class InsertDataQueues(Base):
    __tablename__ = "InsertDataQueues"

    QueueId = Column(Integer, primary_key=True)
    QueueName = Column(String)
    ToEmailTotal = Column(Integer)
    EmailSent = Column(Integer)
    EmailFailed = Column(Integer)
    Status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "QueueId": self.QueueId,
            "QueueName": self.QueueName,
            "ToEmailTotal": self.ToEmailTotal,
            "EmailSent": self.EmailSent,
            "EmailFailed": self.EmailFailed,
            "Status": self.Status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class StudentOrganization(Base):
    __tablename__ = "StudentOrganization"
    
    StudentOrganizationId = Column(Integer, primary_key=True)
    OrganizationLogo = Column(String)
    OrganizationName = Column(String)
    OrganizationMemberRequirements = Column(String)
    AdviserImage = Column(String)
    AdviserName = Column(String)
    Vision = Column(String)
    Mission = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "StudentOrganizationId": self.StudentOrganizationId,
            "OrganizationLogo": self.OrganizationLogo,
            "OrganizationName": self.OrganizationName,
            "OrganizationMemberRequirements": self.OrganizationMemberRequirements,
            "AdviserImage": self.AdviserImage,
            "AdviserName": self.AdviserName,
            "Vision": self.Vision,
            "Mission": self.Mission,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class OrganizationOfficer(Base):
    __tablename__ = "OrganizationOfficer"

    OrganizationOfficerId = Column(Integer, primary_key=True)
    StudentOrganizationId = Column(Integer, ForeignKey('StudentOrganization.StudentOrganizationId'))
    StudentNumber = Column(String(15), unique=True)
    Image = Column(String)
    Position = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "OrganizationOfficerId": self.OrganizationOfficerId,
            "StudentOrganizationId": self.StudentOrganizationId,
            "StudentNumber": self.StudentNumber,
            "Image": self.Image,
            "Position": self.Position,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

class OrganizationMember(Base):
    __tablename__ = "OrganizationMember"

    OrganizationMemberId = Column(Integer, primary_key=True)
    StudentOrganizationId = Column(Integer, ForeignKey('StudentOrganization.StudentOrganizationId'))
    StudentNumber = Column(String(15), unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "OrganizationMemberId": self.OrganizationMemberId,
            "StudentOrganizationId": self.StudentOrganizationId,
            "StudentNumber": self.StudentNumber,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

#########################################################
""" Comelec Portal Table Models """

class CoC(Base):
    __tablename__ = "CoC"

    CoCId = Column(Integer, primary_key=True)
    ElectionId = Column(Integer, ForeignKey('Election.ElectionId'))
    StudentNumber = Column(String(15), ForeignKey('Student.StudentNumber'), unique=True)
    VerificationCode = Column(String)
    Motto = Column(String)
    PoliticalAffiliation = Column(String)
    PartyListId = Column(Integer, ForeignKey('PartyList.PartyListId'), nullable=True)
    SelectedPositionName = Column(String)
    DisplayPhoto = Column(String)
    CertificationOfGrades = Column(String)
    Status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self, row=None):
        return {
            "CoCId": self.CoCId,
            "count": row,
            "ElectionId": self.ElectionId,
            "StudentNumber": self.StudentNumber,
            "VerificationCode": self.VerificationCode,
            "Motto": self.Motto,
            "PoliticalAffiliation": self.PoliticalAffiliation,
            "PartyListId": self.PartyListId,
            "SelectedPositionName": self.SelectedPositionName,
            "DisplayPhoto": self.DisplayPhoto,
            "CertificationOfGrades": self.CertificationOfGrades,
            "Status": self.Status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class PartyList(Base):
    __tablename__ = "PartyList"

    PartyListId = Column(Integer, primary_key=True)
    ElectionId = Column(Integer, ForeignKey('Election.ElectionId'))
    PartyListName = Column(String)
    Description = Column(String)
    Platforms = Column(String)
    EmailAddress = Column(String)
    CellphoneNumber = Column(String)
    Vision = Column(String)
    Mission = Column(String)
    ImageAttachment = Column(String)
    VideoAttachment = Column(String)
    Status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self, row=None):
        return {
            "PartyListId": self.PartyListId,
            "count": row,
            "ElectionId": self.ElectionId,
            "PartyListName": self.PartyListName,
            "Description": self.Description,
            "Platforms": self.Platforms,
            "EmailAddress": self.EmailAddress,
            "CellphoneNumber": self.CellphoneNumber,
            "Vision": self.Vision,
            "Mission": self.Mission,
            "ImageAttachment": self.ImageAttachment,
            "VideoAttachment": self.VideoAttachment,
            "Status": self.Status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class Candidates(Base):
    __tablename__ = "Candidates"

    CandidateId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), ForeignKey('Student.StudentNumber'), unique=True)
    ElectionId = Column(Integer, ForeignKey('Election.ElectionId'))
    PartyListId = Column(Integer, ForeignKey('PartyList.PartyListId'), nullable=True)
    SelectedPositionName = Column(String)
    DisplayPhoto = Column(String)
    Rating = Column(Integer, default=0)
    TimesRated = Column(Integer, default=0)
    Votes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self, row=None):
        return {
            "CandidateId": self.CandidateId,
            "StudentNumber": self.StudentNumber,
            "ElectionId": self.ElectionId,
            "PartyListId": self.PartyListId,
            "SelectedPositionName": self.SelectedPositionName,
            "DisplayPhoto": self.DisplayPhoto,
            "Rating": self.Rating,
            "TimesRated": self.TimesRated,
            "Votes": self.Votes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class RatingsTracker(Base):
    __tablename__ = "RatingsTracker"

    RatingsTrackerId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), ForeignKey('Student.StudentNumber'), unique=True)
    ElectionId = Column(Integer, ForeignKey('Election.ElectionId'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "RatingsTrackerId": self.RatingsTrackerId,
            "StudentNumber": self.StudentNumber,
            "ElectionId": self.ElectionId,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class VotingsTracker(Base):
    __tablename__ = "VotingsTracker"

    VotingsTrackerId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), ForeignKey('Student.StudentNumber'), unique=True)
    ElectionId = Column(Integer, ForeignKey('Election.ElectionId'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "VotingsTrackerId": self.VotingsTrackerId,
            "StudentNumber": self.StudentNumber,
            "ElectionId": self.ElectionId,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class ElectionAnalytics(Base):
    __tablename__ = "ElectionAnalytics"

    ElectionAnalyticsId = Column(Integer, primary_key=True)
    ElectionId = Column(Integer, ForeignKey('Election.ElectionId'))
    AbstainCount = Column(Integer, default=0)
    VotesCount = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "ElectionAnalyticsId": self.ElectionAnalyticsId,
            "ElectionId": self.ElectionId,
            "AbstainCount": self.AbstainCount,
            "VotesCount": self.VotesCount,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class ElectionWinners(Base):
    __tablename__ = "ElectionWinners"

    ElectionWinnersId = Column(Integer, primary_key=True)
    ElectionId = Column(Integer, ForeignKey('Election.ElectionId'))
    StudentNumber = Column(String(15), ForeignKey('Student.StudentNumber'), unique=True)
    SelectedPositionName = Column(String)
    Votes = Column(Integer, default=0)
    IsTied = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "ElectionWinnersId": self.ElectionWinnersId,
            "ElectionId": self.ElectionId,
            "StudentNumber": self.StudentNumber,
            "SelectedPositionName": self.SelectedPositionName,
            "Votes": self.Votes,
            "IsTied": self.IsTied,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }