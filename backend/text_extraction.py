import cv2
import pytesseract
import numpy as np
from sqlalchemy.orm import Session
from app.db.models.survey import Survey
from app.services.analysis.data_structuring import structure_data

async def extract_text(image_path: str, bubbles, survey_id: int, db: Session):
    """Extract text from the survey image"""
    try:
        # Update progress
        update_progress(survey_id, 70.0, db)
        
        # Read image
        image = cv2.imread(image_path)
        
        # Convert to grayscale if not already
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply OCR to the entire image
        text = pytesseract.image_to_string(gray)
        
        # Extract text regions near bubbles
        bubble_text_pairs = []
        
        # Sort bubbles by y-coordinate (top to bottom)
        sorted_bubbles = sorted(bubbles, key=lambda b: b["y"])
        
        # Group bubbles by proximity (likely same question)
        question_groups = group_bubbles_by_question(sorted_bubbles)
        
        # For each question group, extract the question text
        for group in question_groups:
            # Find the region above the first bubble in the group
            first_bubble = group[0]
            question_y = max(0, first_bubble["y"] - 50)  # Look 50 pixels above
            question_height = first_bubble["y"] - question_y
            
            if question_height > 0:
                # Extract question region
                question_region = gray[question_y:first_bubble["y"], :]
                question_text = pytesseract.image_to_string(question_region)
                
                # Add each bubble in the group with the question text
                for bubble in group:
                    bubble_text_pairs.append({
                        "question": question_text.strip(),
                        "x": bubble["x"],
                        "y": bubble["y"],
                        "filled": bubble["filled"]
                    })
        
        # Update progress
        update_progress(survey_id, 80.0, db)
        
        # Continue with data structuring
        await structure_data(bubble_text_pairs, survey_id, db)
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = f"Text extraction error: {str(e)}"
        db.commit()
        raise

def group_bubbles_by_question(bubbles, vertical_threshold=30):
    """Group bubbles that likely belong to the same question based on vertical proximity"""
    if not bubbles:
        return []
    
    groups = []
    current_group = [bubbles[0]]
    
    for i in range(1, len(bubbles)):
        current_bubble = bubbles[i]
        prev_bubble = bubbles[i-1]
        
        # If this bubble is close vertically to the previous one, add to current group
        if abs(current_bubble["y"] - prev_bubble["y"]) < vertical_threshold:
            current_group.append(current_bubble)
        else:
            # Start a new group
            groups.append(current_group)
            current_group = [current_bubble]
    
    # Add the last group
    if current_group:
        groups.append(current_group)
    
    return groups

def update_progress(survey_id: int, progress: float, db: Session):
    """Update the progress of survey processing"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    survey.progress = progress
    db.commit()
