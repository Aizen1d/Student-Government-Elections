from database import engine, Base
from sqlalchemy.orm import sessionmaker, relationship

from sqlalchemy import Column, Integer, Float, String, Date, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func

from cloudinary.api import resources_by_tag

Session = sessionmaker(bind=engine)
session = Session()

class Student(Base):
    __tablename__ = "SGEStudent"
    
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
    __tablename__ = "SGEElection"
    
    ElectionId = Column(Integer, primary_key=True)
    ElectionName = Column(String)
    StudentOrganizationId = Column(Integer, ForeignKey('SGEStudentOrganization.StudentOrganizationId'))
    ElectionStatus = Column(String)
    SchoolYear = Column(String)
    Semester = Column(String)
    CreatedBy = Column(String, ForeignKey('SGEStudent.StudentNumber'))

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
    __tablename__ = "SGECreatedElectionPosition"
    
    CreatedElectionPositionId = Column(Integer, primary_key=True)
    ElectionId = Column(Integer, ForeignKey('SGEElection.ElectionId'))
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
    __tablename__ = "SGESavedPosition"
    
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
    __tablename__ = "SGEAnnouncement"
    
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
    __tablename__ = "SGERules"
    
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
    __tablename__ = "SGEGuidelines"
    
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
    __tablename__ = "SGECertifications"
    
    CertificationId = Column(Integer, primary_key=True)
    Title = Column(String)
    ElectionId = Column(Integer, ForeignKey('SGEElection.ElectionId'))
    StudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber'))
    Date = Column(Date)
    AdminSignatoryQuantity = Column(String)
    AssetId = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "CertificationId": self.CertificationId,
            "Title": self.Title,
            "ElectionId": self.ElectionId,
            "StudentNumber": self.StudentNumber,
            "Date": self.Date.isoformat() if self.Date else None,
            "AdminSignatoryQuantity": self.AdminSignatoryQuantity,
            "AssetId": self.AssetId,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
class CreatedAdminSignatory(Base):
    __tablename__ = "SGECreatedAdminSignatory"
    
    CreatedAdminSignatoryId = Column(Integer, primary_key=True)
    CertificationId = Column(Integer, ForeignKey('SGECertifications.CertificationId'))
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

class Code(Base):
    __tablename__ = "SGECode"

    CodeId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber'), unique=True)
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
    
class InsertDataQueues(Base):
    __tablename__ = "SGEInsertDataQueues"

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
    __tablename__ = "SGEStudentOrganization"
    
    StudentOrganizationId = Column(Integer, primary_key=True)
    OrganizationLogo = Column(String)
    OrganizationName = Column(String)
    OrganizationMemberRequirements = Column(String)
    AdviserImage = Column(String)
    AdviserName = Column(String)
    Vision = Column(String, nullable=True)
    Mission = Column(String, nullable=True)
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
    __tablename__ = "SGEOrganizationOfficer"

    OrganizationOfficerId = Column(Integer, primary_key=True)
    StudentOrganizationId = Column(Integer, ForeignKey('SGEStudentOrganization.StudentOrganizationId'))
    StudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber'), unique=True)
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
    __tablename__ = "SGEOrganizationMember"

    OrganizationMemberId = Column(Integer, primary_key=True)
    StudentOrganizationId = Column(Integer, ForeignKey('SGEStudentOrganization.StudentOrganizationId'))
    StudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber'), unique=True)
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
    
class ElectionAppeals(Base):
    __tablename__ = "SGEElectionAppeals"

    ElectionAppealsId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber'))
    AppealDetails = Column(Text)
    AppealEmailSubject = Column(String, nullable=True)
    AppealResponse = Column(Text, nullable=True)
    AppealStatus = Column(String, default="Pending")
    AttachmentAssetId = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "ElectionAppealsId": self.ElectionAppealsId,
            "StudentNumber": self.StudentNumber,
            "AppealDetails": self.AppealDetails,
            "AppealEmailSubject": self.AppealEmailSubject,
            "AppealResponse": self.AppealResponse,
            "AppealStatus": self.AppealStatus,
            "AttachmentAssetId": self.AttachmentAssetId,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

#########################################################
""" Comelec Portal Table Models """
class Comelec(Base):
    __tablename__ = "SGEComelec"

    ComelecId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber'), unique=True)
    Password = Column(Text)
    Position = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class CoC(Base):
    __tablename__ = "SGECoC"

    CoCId = Column(Integer, primary_key=True)
    ElectionId = Column(Integer, ForeignKey('SGEElection.ElectionId'))
    StudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber'))
    VerificationCode = Column(String)
    Motto = Column(String, nullable=True)
    Platform = Column(Text)
    PoliticalAffiliation = Column(String)
    PartyListId = Column(Integer, ForeignKey('SGEPartyList.PartyListId'), nullable=True)
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
            "Platform": self.Platform,
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
    __tablename__ = "SGEPartyList"

    PartyListId = Column(Integer, primary_key=True)
    ElectionId = Column(Integer, ForeignKey('SGEElection.ElectionId'))
    PartyListName = Column(String)
    Description = Column(String)
    Platforms = Column(String)
    EmailAddress = Column(String)
    CellphoneNumber = Column(String)
    Vision = Column(String)
    Mission = Column(String)
    ImageAttachment = Column(String, nullable=True)
    VideoAttachment = Column(String, nullable=True)
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
    __tablename__ = "SGECandidates"

    CandidateId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber'))
    ElectionId = Column(Integer, ForeignKey('SGEElection.ElectionId'))
    PartyListId = Column(Integer, ForeignKey('SGEPartyList.PartyListId'), nullable=True)
    SelectedPositionName = Column(String)
    DisplayPhoto = Column(String)
    Votes = Column(Integer, default=0)
    TimesAbstained = Column(Integer, default=0)
    Rating = Column(Integer, default=0)
    TimesRated = Column(Integer, default=0)
    OneStar = Column(Integer, default=0)
    TwoStar = Column(Integer, default=0)
    ThreeStar = Column(Integer, default=0)
    FourStar = Column(Integer, default=0)
    FiveStar = Column(Integer, default=0)
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
            "TimesAbstained": self.TimesAbstained,
            "OneStar": self.OneStar,
            "TwoStar": self.TwoStar,
            "ThreeStar": self.ThreeStar,
            "FourStar": self.FourStar,
            "FiveStar": self.FiveStar,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class RatingsTracker(Base):
    __tablename__ = "SGERatingsTracker"

    RatingsTrackerId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber'), unique=True)
    ElectionId = Column(Integer, ForeignKey('SGEElection.ElectionId'))
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
    __tablename__ = "SGEVotingsTracker"

    VotingsTrackerId = Column(Integer, primary_key=True)
    VoterStudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber'))
    VotedCandidateId = Column(Integer, ForeignKey('SGECandidates.CandidateId'))
    CourseId = Column(Integer)
    ElectionId = Column(Integer, ForeignKey('SGEElection.ElectionId'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            "VotingsTrackerId": self.VotingsTrackerId,
            "VoterStudentNumber": self.VoterStudentNumber,
            "VotedCandidateId": self.VotedCandidateId,
            "CourseId": self.CourseId,
            "ElectionId": self.ElectionId,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
class ElectionAnalytics(Base):
    __tablename__ = "SGEElectionAnalytics"

    ElectionAnalyticsId = Column(Integer, primary_key=True)
    ElectionId = Column(Integer, ForeignKey('SGEElection.ElectionId'))
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
    __tablename__ = "SGEElectionWinners"

    ElectionWinnersId = Column(Integer, primary_key=True)
    ElectionId = Column(Integer, ForeignKey('SGEElection.ElectionId'))
    StudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber'))
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
    
class Eligibles(Base):
    __tablename__ = "SGEEligibles"

    EligibleId = Column(Integer, primary_key=True)
    StudentNumber = Column(String(15), ForeignKey('SGEStudent.StudentNumber')) # Not unique since a student can be eligible for multiple elections
    ElectionId = Column(Integer, ForeignKey('SGEElection.ElectionId'))
    IsVotedOrAbstained = Column(Boolean, default=False)
    VotingPassword = Column(Text)

    def to_dict(self):
        return {
            "EligibleId": self.EligibleId,
            "StudentNumber": self.StudentNumber,
            "ElectionId": self.ElectionId,
            "IsVotedOrAbstained": self.IsVotedOrAbstained,
            "VotingPassword": self.VotingPassword
        }