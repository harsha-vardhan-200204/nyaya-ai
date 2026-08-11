from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class CaseCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=10)
    incident_date: Optional[str] = None
    location: Optional[str] = None
    case_type: Optional[str] = None
    parties: Optional[str] = None
    facts: Optional[str] = None
    sections_cited: Optional[str] = None

class CaseResponse(BaseModel):
    id: int
    title: str
    description: str
    incident_date: Optional[str]
    location: Optional[str]
    case_type: Optional[str]
    parties: Optional[str]
    facts: Optional[str]
    sections_cited: Optional[str]
    status: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class LegalSectionResponse(BaseModel):
    id: int
    act_id: int
    section_number: str
    title: str
    description: str
    keywords: Optional[str]
    domain: Optional[str]
    active_status: str

    class Config:
        from_attributes = True

class LegalActResponse(BaseModel):
    id: int
    name: str
    year: int
    description: Optional[str]
    source_url: Optional[str]
    sections: List[LegalSectionResponse] = []

    class Config:
        from_attributes = True

class JudgmentResponse(BaseModel):
    id: int
    case_name: str
    court: str
    state: Optional[str]
    judgment_date: str
    acts: Optional[str]
    sections: Optional[str]
    keywords: Optional[str]
    facts: str
    legal_issue: Optional[str]
    arguments: Optional[str]
    evidence: Optional[str]
    judgment_summary: str
    outcome: str
    precedent: Optional[str]
    source_url: Optional[str]
    verified: bool

    class Config:
        from_attributes = True

class SavedCaseCreate(BaseModel):
    judgment_id: int

class SavedCaseResponse(BaseModel):
    id: int
    user_id: int
    judgment_id: int
    created_at: datetime
    judgment: JudgmentResponse

    class Config:
        from_attributes = True

# Custom response schemas for analytics and predictions
class SimilarCaseItem(BaseModel):
    id: int
    case_name: str
    court: str
    state: Optional[str]
    judgment_date: str
    facts: str
    outcome: str
    acts: Optional[str]
    sections: Optional[str]
    judgment_summary: str
    similarity_score: float
    why_similar: str
    verified: bool
    source_url: Optional[str]

class ProbabilityItem(BaseModel):
    label: str
    probability: float

class PredictionDetails(BaseModel):
    probabilities: List[ProbabilityItem]
    confidence_score: float
    supporting_factors: List[str]
    risk_factors: List[str]
    missing_information: List[str]
    explanation: str
    factual_features: Dict[str, bool]

class CaseTimelineItem(BaseModel):
    date: str
    event: str

class CaseNLPAnalysis(BaseModel):
    dates: List[str]
    disputed_amount: str
    all_amounts: List[str]
    citations: List[str]
    location: str
    all_locations: List[str]
    parties: Dict[str, str]
    timeline: List[CaseTimelineItem]

class CaseAnalysisResponse(BaseModel):
    case_id: int
    category: str
    nlp_analysis: CaseNLPAnalysis
    prediction: PredictionDetails
    similar_cases: List[SimilarCaseItem]

class CounterfactualRequest(BaseModel):
    written_contract: bool
    notice_sent: bool
    receipt_exists: bool
    evidence_present: bool
    category: str
    facts: str
