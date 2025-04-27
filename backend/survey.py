from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.base import Base

class Survey(Base):
    __tablename__ = "surveys"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_path = Column(String, nullable=False)
    processed_path = Column(String, nullable=True)
    status = Column(String, default="uploaded")  # uploaded, processing, completed, failed
    progress = Column(Float, default=0.0)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Metadata
    num_questions = Column(Integer, nullable=True)
    num_options = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<Survey {self.id}: {self.filename}>"
