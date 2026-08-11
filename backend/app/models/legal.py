import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    incident_date = Column(String, nullable=True)
    location = Column(String, nullable=True)
    case_type = Column(String, nullable=True)
    parties = Column(String, nullable=True)
    facts = Column(Text, nullable=True)
    sections_cited = Column(String, nullable=True)
    status = Column(String, default="Pending", nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="cases")

class LegalAct(Base):
    __tablename__ = "legal_acts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    source_url = Column(String, nullable=True)
    
    sections = relationship("LegalSection", back_populates="act", cascade="all, delete-orphan")

class LegalSection(Base):
    __tablename__ = "legal_sections"
    
    id = Column(Integer, primary_key=True, index=True)
    act_id = Column(Integer, ForeignKey("legal_acts.id", ondelete="CASCADE"), nullable=False)
    section_number = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    keywords = Column(String, nullable=True)
    domain = Column(String, index=True, nullable=True)
    active_status = Column(String, default="Active", nullable=False)
    
    act = relationship("LegalAct", back_populates="sections")

class Judgment(Base):
    __tablename__ = "judgments"
    
    id = Column(Integer, primary_key=True, index=True)
    case_name = Column(String, index=True, nullable=False)
    court = Column(String, nullable=False)
    state = Column(String, nullable=True)
    judgment_date = Column(String, nullable=False)
    case_type = Column(String, nullable=True)
    acts = Column(String, nullable=True)
    sections = Column(String, nullable=True)
    keywords = Column(String, nullable=True)
    facts = Column(Text, nullable=False)
    legal_issue = Column(Text, nullable=True)
    arguments = Column(Text, nullable=True)
    evidence = Column(Text, nullable=True)
    judgment_summary = Column(Text, nullable=False)
    outcome = Column(String, nullable=False)
    precedent = Column(Text, nullable=True)
    source_url = Column(String, nullable=True)
    verified = Column(Boolean, default=True, nullable=False)
    
    saved_by = relationship("SavedCase", back_populates="judgment", cascade="all, delete-orphan")

class SavedCase(Base):
    __tablename__ = "saved_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    judgment_id = Column(Integer, ForeignKey("judgments.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="saved_cases")
    judgment = relationship("Judgment", back_populates="saved_by")
