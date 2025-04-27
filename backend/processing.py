from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.survey import Survey
from app.schemas.survey import SurveyStatusResponse

router = APIRouter()

@router.get("/status/{survey_id}", response_model=SurveyStatusResponse)
async def get_processing_status(survey_id: int, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    return {
        "id": survey.id,
        "status": survey.status,
        "progress": survey.progress,
        "error": survey.error
    }
