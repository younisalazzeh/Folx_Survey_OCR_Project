from sqlalchemy.orm import Session
from app.db.models.survey import Survey
from app.db.models.result import Result

async def analyze_results(structured_data, survey_id: int, db: Session):
    """Perform statistical analysis on the structured data"""
    try:
        # Update progress
        update_progress(survey_id, 95.0, db)
        
        # Add statistical analysis to the structured data
        for question in structured_data["questions"]:
            # Calculate response counts
            total_responses = len(question["responses"])
            filled_count = sum(1 for r in question["responses"] if r)
            
            # Add statistics to question
            question["statistics"] = {
                "total_options": total_responses,
                "selected_count": filled_count,
                "percentage": (filled_count / total_responses) * 100 if total_responses > 0 else 0
            }
        
        # Add overall statistics
        total_questions = len(structured_data["questions"])
        total_options = sum(len(q["options"]) for q in structured_data["questions"])
        total_selected = sum(sum(1 for r in q["responses"] if r) for q in structured_data["questions"])
        
        structured_data["statistics"] = {
            "total_questions": total_questions,
            "total_options": total_options,
            "total_selected": total_selected,
            "selection_rate": (total_selected / total_options) * 100 if total_options > 0 else 0
        }
        
        # Save results to database
        result = Result(
            survey_id=survey_id,
            data=structured_data
        )
        db.add(result)
        
        # Update survey status to completed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "completed"
        survey.progress = 100.0
        
        db.commit()
        
    except Exception as e:
        # Update status to failed
        survey = db.query(Survey).filter(Survey.id == survey_id).first()
        survey.status = "failed"
        survey.error = f"Statistical analysis error: {str(e)}"
        db.commit()
        raise

def update_progress(survey_id: int, progress: float, db: Session):
    """Update the progress of survey processing"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    survey.progress = progress
    db.commit()
