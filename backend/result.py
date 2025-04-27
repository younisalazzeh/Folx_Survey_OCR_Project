from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Result(Base):
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    data = Column(JSON, nullable=False)  # Structured survey data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    survey = relationship("Survey", backref="results")
    
    def __repr__(self):
        return f"<Result {self.id} for Survey {self.survey_id}>"
