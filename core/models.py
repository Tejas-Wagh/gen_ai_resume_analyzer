from .database import Base
from sqlalchemy import Column,  Integer, String, ForeignKey, DateTime, Enum
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index = True)
    email = Column(String, index = True)
    password = Column(String, index=True)


class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index = True)
    resume_name = Column(String, index = True)
    analysis_result = Column(String, default="")
    user_id = Column(Integer, ForeignKey("users.id"))
    analysis_status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), default=datetime.now())

