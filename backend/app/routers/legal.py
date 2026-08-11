from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.models.legal import LegalAct, LegalSection, Judgment, SavedCase
from app.models.auth import User
from app.schemas.legal import (
    LegalActResponse, LegalSectionResponse, JudgmentResponse,
    SavedCaseCreate, SavedCaseResponse
)
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/legal", tags=["legal"])

@router.get("/acts", response_model=List[LegalActResponse])
def get_acts(db: Session = Depends(get_db)):
    """Retrieve all statutory acts from the legal database."""
    return db.query(LegalAct).all()

@router.get("/sections", response_model=List[LegalSectionResponse])
def get_sections(domain: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieve legal sections, optionally filtered by domain."""
    query = db.query(LegalSection)
    if domain:
        query = query.filter(LegalSection.domain.ilike(f"%{domain}%"))
    return query.all()

@router.get("/judgments", response_model=List[JudgmentResponse])
def get_judgments(
    court: Optional[str] = None,
    state: Optional[str] = None,
    outcome: Optional[str] = None,
    case_type: Optional[str] = None,
    verified: Optional[bool] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Search and filter historical court judgments."""
    query = db.query(Judgment)
    
    if court:
        query = query.filter(Judgment.court.ilike(f"%{court}%"))
    if state:
        query = query.filter(Judgment.state.ilike(f"%{state}%"))
    if outcome:
        query = query.filter(Judgment.outcome == outcome)
    if case_type:
        query = query.filter(Judgment.case_type == case_type)
    if verified is not None:
        query = query.filter(Judgment.verified == verified)
    if q:
        query = query.filter(
            (Judgment.case_name.ilike(f"%{q}%")) |
            (Judgment.facts.ilike(f"%{q}%")) |
            (Judgment.judgment_summary.ilike(f"%{q}%"))
        )
        
    return query.all()

@router.get("/judgments/{id}", response_model=JudgmentResponse)
def get_judgment(id: int, db: Session = Depends(get_db)):
    """Retrieve details of a specific historical judgment by ID."""
    judg = db.query(Judgment).filter(Judgment.id == id).first()
    if not judg:
        raise HTTPException(status_code=404, detail="Judgment record not found")
    return judg

# Saved Cases Operations
@router.post("/saved-cases", response_model=SavedCaseResponse)
def save_case(req: SavedCaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Save/Bookmark a historical judgment for research (Lawyer/Client)."""
    # Check if case exists
    judg = db.query(Judgment).filter(Judgment.id == req.judgment_id).first()
    if not judg:
        raise HTTPException(status_code=404, detail="Judgment not found")
        
    # Check if already saved
    existing = db.query(SavedCase).filter(
        SavedCase.user_id == current_user.id,
        SavedCase.judgment_id == req.judgment_id
    ).first()
    if existing:
        return existing
        
    new_save = SavedCase(
        user_id=current_user.id,
        judgment_id=req.judgment_id
    )
    db.add(new_save)
    db.commit()
    db.refresh(new_save)
    return new_save

@router.get("/saved-cases", response_model=List[SavedCaseResponse])
def get_saved_cases(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all cases saved/bookmarked by the logged-in user."""
    return db.query(SavedCase).filter(SavedCase.user_id == current_user.id).all()

@router.delete("/saved-cases/{id}")
def delete_saved_case(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Remove a saved case link."""
    saved = db.query(SavedCase).filter(SavedCase.id == id, SavedCase.user_id == current_user.id).first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved case bookmark not found")
        
    db.delete(saved)
    db.commit()
    return {"detail": "Saved case bookmark removed"}
