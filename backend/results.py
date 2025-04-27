from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.survey import Survey
from app.db.models.result import Result
from app.schemas.result import ResultResponse

router = APIRouter()

@router.get("/results/{survey_id}", response_model=ResultResponse)
async def get_survey_results(survey_id: int, db: Session = Depends(get_db)):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    
    if survey.status != "completed":
        raise HTTPException(
            status_code=400, 
            detail=f"Survey processing not completed. Current status: {survey.status}"
        )
    
    result = db.query(Result).filter(Result.survey_id == survey_id).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Results not found")
    
    return {
        "survey_id": survey_id,
        "data": result.data,
        "created_at": result.created_at
    }
