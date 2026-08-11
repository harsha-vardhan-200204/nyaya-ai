from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from app.database import get_db
from app.models.legal import Case, Judgment, SavedCase
from app.models.auth import User
from app.schemas.legal import (
    CaseCreate, CaseResponse, CaseAnalysisResponse, 
    CounterfactualRequest, PredictionDetails, SimilarCaseItem
)
from app.routers.auth import get_current_user, RoleRequired
from app.services.nlp_engine import extract_entities
from app.services.classifier import classifier
from app.services.similarity import get_similar_cases
from app.services.outcome import predict_case_outcome
from app.services.report import generate_pdf_report

router = APIRouter(prefix="/api/cases", tags=["cases"])

@router.post("", response_model=CaseResponse)
def create_case(case_in: CaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Submit a new case for analysis (Client Role)."""
    # Extract entities briefly to fill structured metadata
    nlp_res = extract_entities(case_in.description)
    predicted_cats = classifier.predict(case_in.description)
    primary_cat = predicted_cats[0]["category"] if predicted_cats else "Civil Law"
    
    new_case = Case(
        title=case_in.title,
        description=case_in.description,
        incident_date=case_in.incident_date or (nlp_res.get("timeline")[0]["date"] if nlp_res.get("timeline") else None),
        location=case_in.location or nlp_res.get("location"),
        case_type=case_in.case_type or primary_cat,
        parties=case_in.parties or f"{nlp_res.get('parties', {}).get('claimant', 'Claimant')} v. {nlp_res.get('parties', {}).get('respondent', 'Opposite Party')}",
        facts=case_in.facts or case_in.description[:500],
        sections_cited=";".join(nlp_res.get("citations", [])),
        status="Analyzed",
        user_id=current_user.id
    )
    
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    return new_case

@router.get("", response_model=list[CaseResponse])
def list_cases(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all submitted cases for the logged-in user. Lawyers and Admins can see all cases."""
    if current_user.role in ["Lawyer", "Admin"]:
        return db.query(Case).all()
    return db.query(Case).filter(Case.user_id == current_user.id).all()

@router.get("/{id}", response_model=CaseResponse)
def get_case(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve details of a specific case by ID."""
    case = db.query(Case).filter(Case.id == id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    # Check permissions
    if current_user.role not in ["Lawyer", "Admin"] and case.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this case")
        
    return case

@router.post("/{id}/analyze", response_model=CaseAnalysisResponse)
def analyze_case(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Run the multi-stage AI legal analysis pipeline on a submitted case."""
    case = db.query(Case).filter(Case.id == id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    # Check permissions
    if current_user.role not in ["Lawyer", "Admin"] and case.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this case")
        
    # Stage 1: NLP Entity Extraction
    nlp_res = extract_entities(case.description)
    
    # Stage 2: Legal Domain Classification
    predicted_cats = classifier.predict(case.description)
    primary_cat = predicted_cats[0]["category"] if predicted_cats else "Civil Law"
    
    # Stage 3: Similar Case Retrieval
    similar_cases = get_similar_cases(db, case.description, top_k=3)
    
    # Stage 4: Outcome Prediction & XAI
    prediction = predict_case_outcome(primary_cat, case.description)
    
    return {
        "case_id": case.id,
        "category": primary_cat,
        "nlp_analysis": nlp_res,
        "prediction": prediction,
        "similar_cases": similar_cases
    }

@router.post("/counterfactual", response_model=PredictionDetails)
def simulate_counterfactual(req: CounterfactualRequest):
    """
    Run 'What If?' scenario simulation.
    Adjusts outcome probabilities dynamically based on toggled facts.
    """
    overrides = {
        "written_contract": req.written_contract,
        "notice_sent": req.notice_sent,
        "receipt_exists": req.receipt_exists,
        "evidence_present": req.evidence_present
    }
    prediction = predict_case_outcome(req.category, req.facts, overrides=overrides)
    return prediction

@router.get("/{id}/report")
def download_report(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Generate and download a professional PDF report of the case analysis."""
    case = db.query(Case).filter(Case.id == id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    if current_user.role not in ["Lawyer", "Admin"] and case.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this report")
        
    # Run pipeline to compile fresh report data
    nlp_res = extract_entities(case.description)
    predicted_cats = classifier.predict(case.description)
    primary_cat = predicted_cats[0]["category"] if predicted_cats else "Civil Law"
    similar_cases = get_similar_cases(db, case.description, top_k=3)
    prediction = predict_case_outcome(primary_cat, case.description)
    
    case_meta = {
        "id": case.id,
        "title": case.title,
        "description": case.description,
        "created_at": case.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Generate PDF binary
    pdf_bytes = generate_pdf_report(case_meta, nlp_res, similar_cases, prediction)
    
    # Return as Streamable Response
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=nyayaai_report_case_{id}.pdf"
        }
    )
