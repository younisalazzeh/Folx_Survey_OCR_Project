import json
from sqlalchemy.orm import Session
from app.db.models.survey import Survey
from app.db.models.result import Result
from app.services.analysis.statistics import analyze_results

async def structure_data(bubble_text_pairs, survey_id: int, db: Session):
    """Structure the extracted data into a standardized format"""
    try:
        # Update progress
        update_progress(survey_id, 85.0, db)
        
        # Group by question
        questions = {}
        for pair in bubble_text_pairs:
            question_text = pair["question"]
            if question_text not in questions:
                questions[question_text] = []
            
            questions[question_text].append({
                "x": pair["x"],
                "y": pair["y"],
                "filled": pair["filled"]
            })
        
        # Convert to structured format
        structured_data = {
            "questions": []
        }
        
        for question_text, options in questions.items():
            # Sort options by x-coordinate (left to right)
            sorted_options = sorted(options, key=lambda o: o["x"])
            
            # Create question object
            question = {
                "text": question_text,
                "options": [{"x": opt["x"], "y": opt["y"]} for opt in sorted_options],
                "responses": [opt["filled"] for opt in sorted_options]
            }
            
            structured_data["questions"].append(question)
        
        # Update survey record with metadata
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.num_questions = len(structured_data["questions"])
        survey.num_options = sum(len(q["options"]) for q in structured_data["questions"])
        db.commit()
        
        # Update progress
        update_progress(survey_id, 90.0, db)
        
        # Continue with statistical analysis
        await analyze_results(structured_data, survey_id, db)
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = f"Data structuring error: {str(e)}"
        db.commit()
        raise

def update_progress(survey_id: int, progress: float, db: Session):
    """Update the progress of survey processing"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    survey.progress = progress
    db.commit()
