import cv2
import numpy as np
from sqlalchemy.orm import Session
from app.db.models.survey import Survey
from app.services.ocr.text_extraction import extract_text

async def detect_bubbles(image_path: str, survey_id: int, db: Session):
    """Detect bubbles/checkboxes in the survey image"""
    try:
        # Update progress
        update_progress(survey_id, 40.0, db)
        
        # Read preprocessed image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Find contours
        contours, _ = cv2.findContours(
            gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter contours to find potential bubbles
        bubbles = []
        for contour in contours:
            # Calculate contour properties
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            # Filter by area and circularity
            if area > 100 and area < 1000:  # Adjust based on your bubble size
                # Calculate circularity
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                
                # Bubbles tend to be circular
                if circularity > 0.7:  # Adjust threshold as needed
                    x, y, w, h = cv2.boundingRect(contour)
                    bubbles.append({
                        "contour": contour,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h,
                        "area": area,
                        "filled": is_bubble_filled(gray, x, y, w, h)
                    })
        
        # Update progress
        update_progress(survey_id, 60.0, db)
        
        # Continue with text extraction
        await extract_text(image_path, bubbles, survey_id, db)
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = f"Bubble detection error: {str(e)}"
        db.commit()
        raise

def is_bubble_filled(image, x, y, w, h):
    """Determine if a bubble is filled based on pixel density"""
    # Extract the region of interest
    roi = image[y:y+h, x:x+w]
    
    # Count non-zero pixels (black pixels in the binary image)
    non_zero_count = cv2.countNonZero(roi)
    
    # Calculate the total area
    total_area = w * h
    
    # Calculate the fill ratio
    fill_ratio = non_zero_count / total_area
    
    # If the fill ratio is above a threshold, consider it filled
    return fill_ratio > 0.3  # Adjust threshold as needed

def update_progress(survey_id: int, progress: float, db: Session):
    """Update the progress of survey processing"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    survey.progress = progress
    db.commit()
