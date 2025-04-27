import cv2
import numpy as np
import os
from sqlalchemy.orm import Session
from app.db.models.survey import Survey
from app.core.config import settings
from app.services.ocr.bubble_detection import detect_bubbles

async def preprocess_image(file_path: str, survey_id: int, db: Session):
    """Preprocess the survey image for OCR"""
    try:
        # Update progress
        update_progress(survey_id, 20.0, db)
        
        # Read image
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(f"Could not read image at {file_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Create processed directory if it doesn't exist
        os.makedirs(settings.PROCESSED_DIR, exist_ok=True)
        
        # Save preprocessed image
        processed_filename = os.path.basename(file_path)
        processed_path = os.path.join(settings.PROCESSED_DIR, f"preprocessed_{processed_filename}")
        cv2.imwrite(processed_path, thresh)
        
        # Update survey record
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.processed_path = processed_path
        survey.progress = 30.0
        db.commit()
        
        # Continue with bubble detection
        await detect_bubbles(processed_path, survey_id, db)
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = f"Preprocessing error: {str(e)}"
        db.commit()
        raise

def update_progress(survey_id: int, progress: float, db: Session):
    """Update the progress of survey processing"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    survey.progress = progress
    db.commit()
