import os
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.survey import Survey
from app.schemas.survey import SurveyResponse
from app.core.config import settings
from app.services.ocr.preprocessing import preprocess_image

router = APIRouter()

@router.post("/upload", response_model=SurveyResponse)
async def upload_survey_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Create survey record
    survey = Survey(
        filename=file.filename,
        original_path=file_path,
        status="uploaded"
    )
    db.add(survey)
    db.commit()
    db.refresh(survey)
    
    # Start processing in background
    background_tasks.add_task(
        process_survey_image,
        survey_id=survey.id,
        file_path=file_path,
        db=db
    )
    
    return {
        "id": survey.id,
        "status": survey.status,
        "progress": survey.progress,
        "message": "Upload successful, processing started"
    }

async def process_survey_image(survey_id: int, file_path: str, db: Session):
    """Background task to process the uploaded survey image"""
    try:
        # Update status to processing
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "processing"
        survey.progress = 10.0
        db.commit()
        
        # Process image
        await preprocess_image(file_path, survey_id, db)
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = str(e)
        db.commit()
