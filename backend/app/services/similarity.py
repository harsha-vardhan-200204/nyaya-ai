import os
import numpy as np
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Optional

from app.models.legal import Judgment

# Global sentence-transformer setup (optional fallback)
MODEL_NAME = "all-MiniLM-L6-v2"
encoder_model = None

try:
    from sentence_transformers import SentenceTransformer
    encoder_model = SentenceTransformer(MODEL_NAME)
    print("SentenceTransformers model loaded successfully.")
except Exception as e:
    print(f"SentenceTransformers load skipped or failed: {str(e)}. Using TF-IDF cosine similarity fallback.")

def compute_similarity_scores(query: str, corpus: List[str]) -> np.ndarray:
    """Compute similarity scores between a query and a corpus of texts."""
    if not corpus:
        return np.array([])
        
    global encoder_model
    if encoder_model is not None:
        try:
            query_emb = encoder_model.encode([query])
            corpus_embs = encoder_model.encode(corpus)
            return cosine_similarity(query_emb, corpus_embs)[0]
        except Exception as e:
            print(f"Error during SentenceTransformers encoding: {str(e)}. Falling back to TF-IDF.")
            
    # TF-IDF Fallback
    vectorizer = TfidfVectorizer(stop_words='english', token_pattern=r'\b[a-zA-Z0-9_]{2,}\b')
    all_docs = [query] + corpus
    tfidf_matrix = vectorizer.fit_transform(all_docs)
    
    # Calculate cosine similarity between the query (index 0) and the rest
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    return scores[0]

def get_similar_cases(db: Session, text: str, top_k: int = 3, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Search the database for judgments similar to the user case.
    Applies filters (court, state, year, outcome) and returns ranked matches.
    """
    query = db.query(Judgment)
    
    # Apply filters if provided
    if filters:
        if filters.get("court"):
            query = query.filter(Judgment.court.ilike(f"%{filters['court']}%"))
        if filters.get("state"):
            query = query.filter(Judgment.state.ilike(f"%{filters['state']}%"))
        if filters.get("outcome"):
            query = query.filter(Judgment.outcome == filters["outcome"])
        if filters.get("case_type"):
            query = query.filter(Judgment.case_type == filters["case_type"])
            
    judgments = query.all()
    if not judgments:
        return []
        
    corpus = [j.facts for j in judgments]
    scores = compute_similarity_scores(text, corpus)
    
    results = []
    for idx, score in enumerate(scores):
        j = judgments[idx]
        
        # Determine why it is similar
        reason = []
        if j.case_type and j.case_type.lower() in text.lower():
            reason.append("Similar legal domain")
        
        # Check matching sections
        matching_secs = []
        if j.sections:
            for sec in j.sections.split(';'):
                if sec.strip() and sec.strip() in text:
                    matching_secs.append(sec.strip())
        if matching_secs:
            reason.append(f"Shares relevant provision: Section {', '.join(matching_secs)}")
            
        # Core similarity reason
        if score > 0.4:
            reason.append("High factual overlap in key disputes")
        elif score > 0.2:
            reason.append("Moderate similarity in dispute circumstances")
        else:
            reason.append("Retrieved via domain correlation")
            
        results.append({
            "id": j.id,
            "case_name": j.case_name,
            "court": j.court,
            "state": j.state,
            "judgment_date": j.judgment_date,
            "facts": j.facts,
            "outcome": j.outcome,
            "acts": j.acts,
            "sections": j.sections,
            "judgment_summary": j.judgment_summary,
            "similarity_score": float(round(score * 100, 2)),
            "why_similar": " and ".join(reason) if reason else "General domain similarity",
            "verified": j.verified,
            "source_url": j.source_url
        })
        
    # Sort by similarity score descending
    results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)
    return results[:top_k]
