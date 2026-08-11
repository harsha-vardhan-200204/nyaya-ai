import re
import httpx
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional

from app.config import settings
from app.models.legal import Judgment, LegalSection
from app.services.similarity import compute_similarity_scores

def verify_citation(db: Session, case_name: str) -> Dict[str, Any]:
    """Verify if a case citation exists in our database (Anti-Hallucination)."""
    clean_name = re.sub(r'\s*\(\d{4}\)\s*', '', case_name).strip()
    result = db.query(Judgment).filter(Judgment.case_name.ilike(f"%{clean_name}%")).first()
    
    if result:
        return {
            "verified": True,
            "case_id": result.id,
            "case_name": result.case_name,
            "court": result.court,
            "state": result.state,
            "date": result.judgment_date,
            "outcome": result.outcome,
            "source_url": result.source_url,
            "authority": f"Official {result.court} Record"
        }
    else:
        return {
            "verified": False,
            "case_name": case_name,
            "authority": "Secondary Source / Requires Verification"
        }

def retrieve_ground_truth(db: Session, query: str) -> Dict[str, Any]:
    """Retrieve relevant cases and acts/sections to feed into LLM or Demo Mode."""
    # Find matching sections
    sections = db.query(LegalSection).all()
    sections_text = [f"{s.act_name} Section {s.section_number}: {s.title} - {s.description}" for s in sections]
    sec_scores = compute_similarity_scores(query, sections_text)
    
    relevant_sections = []
    if len(sec_scores) > 0:
        sorted_sec_idx = np.argsort(sec_scores)[::-1]
        for idx in sorted_sec_idx[:3]:
            if sec_scores[idx] > 0.05:
                s = sections[idx]
                relevant_sections.append({
                    "act_name": s.act_name,
                    "section_number": s.section_number,
                    "title": s.title,
                    "description": s.description,
                    "score": float(sec_scores[idx]),
                    "domain": s.domain,
                    "source_url": s.source_url
                })

    # Find matching judgments
    judgments = db.query(Judgment).all()
    judg_text = [f"{j.case_name}: {j.facts}" for j in judgments]
    judg_scores = compute_similarity_scores(query, judg_text)
    
    relevant_judgments = []
    if len(judg_scores) > 0:
        sorted_judg_idx = np.argsort(judg_scores)[::-1]
        for idx in sorted_judg_idx[:3]:
            if judg_scores[idx] > 0.05:
                j = judgments[idx]
                relevant_judgments.append({
                    "id": j.id,
                    "case_name": j.case_name,
                    "court": j.court,
                    "outcome": j.outcome,
                    "facts": j.facts[:200] + "...",
                    "judgment_summary": j.judgment_summary,
                    "score": float(judg_scores[idx]),
                    "source_url": j.source_url,
                    "verified": j.verified
                })
                
    return {
        "sections": relevant_sections,
        "judgments": relevant_judgments
    }

import numpy as np # Import numpy inside the function or file

async def generate_rag_response(db: Session, query: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """Generate source-grounded response using retrieved context."""
    context = retrieve_ground_truth(db, query)
    
    # Compile prompt content
    context_str = "RELEVANT STATUTORY PROVISIONS:\n"
    for s in context["sections"]:
        context_str += f"- Section {s['section_number']} of {s['act_name']} ({s['title']}): {s['description']}\n"
        
    context_str += "\nSIMILAR HISTORICAL CASE LAW:\n"
    for j in context["judgments"]:
        status = "Verified" if j["verified"] else "Unverified"
        context_str += f"- Case: {j['case_name']} [{status}]. Court: {j['court']}. Outcome: {j['outcome']}.\n  Summary: {j['judgment_summary']}\n"

    system_prompt = (
        "You are NyayaAI, an AI-powered legal research and case-analysis assistant for Indian Law.\n"
        "Instructions:\n"
        "1. Provide a source-grounded, professional response in markdown format based ONLY on the provided context.\n"
        "2. Never invent cases, citations, sections, or outcomes.\n"
        "3. Highlight citations with [Verified] or [Unverified] badges based on the context.\n"
        "4. Include a clear disclaimer stating: 'NyayaAI is an educational research tool and does not provide legal advice. Consult a professional.'\n"
        "5. Frame predictions as informational historical patterns, not guarantees."
    )

    full_prompt = f"{system_prompt}\n\nUser Question: {query}\n\nContext:\n{context_str}\n\nResponse:"

    # 1. LIVE GEMINI INTEGRATION
    if settings.LLM_PROVIDER == "gemini" and settings.GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {"parts": [{"text": full_prompt}]}
                ]
            }
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, headers=headers, timeout=15.0)
                if resp.status_code == 200:
                    data = resp.json()
                    answer = data["candidates"][0]["content"]["parts"][0]["text"]
                    return {
                        "response": answer,
                        "source": "Gemini RAG Engine",
                        "context": context
                    }
                else:
                    print(f"Gemini API returned error code {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"Error calling Gemini: {str(e)}")

    # 2. DEMO MODE OFFLINE GENERATOR (Grounded template)
    # If no key, build a beautifully formatted static response grounded in retrieved data.
    return generate_mock_rag_response(query, context)

def generate_mock_rag_response(query: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Formulate a beautiful offline RAG response using retrieved templates."""
    has_secs = len(context["sections"]) > 0
    has_judg = len(context["judgments"]) > 0
    
    response = "## Short Answer\n"
    if not has_secs and not has_judg:
        response += "No direct matches found in our database. Based on generic legal principles, this issue should be checked against civil and local statutory rules. Please consult a legal professional.\n\n"
    else:
        response += f"Based on your query, we retrieved {len(context['sections'])} relevant statutory provisions and {len(context['judgments'])} similar historical judgments. The issue appears to relate to **{context['sections'][0]['domain'] if has_secs else 'Indian Law'}**.\n\n"
        
    if has_secs:
        response += "## Potentially Relevant Laws\n"
        for s in context["sections"]:
            response += f"- **Section {s['section_number']} of the {s['act_name']}** ({s['title']})\n"
            response += f"  - *Provision Details:* {s['description']}\n"
            response += f"  - *Relevance:* This section regulates matters related to {s['domain'].lower()} disputes.\n"
            response += f"  - *Verification:* [Verified Source]({s['source_url']})\n\n"
            
    if has_judg:
        response += "## Similar Cases\n"
        for j in context["judgments"]:
            v_badge = "✅ [Verified Citation]" if j["verified"] else "⚠️ [Unverified Secondary Source]"
            response += f"- **{j['case_name']}** (Court: {j['court']}, Outcome: {j['outcome']})\n"
            response += f"  - *Summary:* {j['judgment_summary']}\n"
            response += f"  - *Verification:* {v_badge} - [Source URL]({j['source_url']})\n\n"
            
    response += "## Historical Outcome Pattern\n"
    if has_judg:
        outcomes = [j["outcome"] for j in context["judgments"]]
        allowed_count = sum(1 for o in outcomes if "Allowed" in o or "Convicted" in o or "Granted" in o)
        prob = int((allowed_count / len(outcomes)) * 100)
        response += f"Among the matching historical cases retrieved, {allowed_count} out of {len(outcomes)} had favorable outcomes for the petitioner. This indicates a baseline historical correlation pattern of roughly **{prob}% Favorable** outcomes, subject to specific evidence.\n\n"
    else:
        response += "Insufficient historical case patterns are present in the dataset to estimate a numeric outcome correlation.\n\n"

    response += "## Possible Next Steps\n"
    response += "1. Gather all written records, communications, and receipts related to the incident.\n"
    response += "2. Send a formal legal notice if not done already, as it sets the statutory timeline.\n"
    response += "3. Schedule a consultation with a qualified advocate specializing in this legal domain.\n\n"
    
    response += "## Sources\n"
    response += "1. India Code (Legislative Department, Ministry of Law and Justice)\n"
    response += "2. Supreme Court of India/High Court Case Status Portals\n\n"
    
    response += "## Disclaimer\n"
    response += "> [!IMPORTANT]\n"
    response += "> NyayaAI provides AI-assisted legal research and educational information only. It is not a substitute for professional legal advice and does not guarantee any legal outcome. Users should verify information with current official legal sources and consult a qualified legal professional."

    return {
        "response": response,
        "source": "NyayaAI Local RAG Engine (Demo Mode)",
        "context": context
    }
