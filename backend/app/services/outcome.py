import re
from typing import Dict, List, Any, Tuple

def analyze_factual_features(text: str) -> Dict[str, bool]:
    """Parse text to detect key legal factual factors."""
    text_lower = text.lower()
    
    has_contract = any(x in text_lower for x in [
        "written agreement", "written contract", "signed agreement", "lease deed", 
        "lease agreement", "rent agreement", "sale deed", "partnership deed"
    ])
    
    has_notice = any(x in text_lower for x in [
        "legal notice", "notice", "demand notice", "eviction notice", "notice to vacate", "statutory notice"
    ])
    
    has_receipt = any(x in text_lower for x in [
        "receipt", "payment proof", "bank statement", "transaction statement", 
        "rent receipt", "invoice", "payment receipt", "bank transfer"
    ])
    
    has_evidence = any(x in text_lower for x in [
        "photograph", "photos", "witness", "email", "whatsapp", "video", 
        "recording", "forensic", "ip logs", "call records"
    ])
    
    return {
        "written_contract": has_contract,
        "notice_sent": has_notice,
        "receipt_exists": has_receipt,
        "evidence_present": has_evidence
    }

def predict_case_outcome(category: str, facts: str, overrides: Dict[str, bool] = None) -> Dict[str, Any]:
    """
    Predict legal outcome probabilities based on category and facts.
    Supports counterfactual overrides.
    """
    # Detect baseline features
    features = analyze_factual_features(facts)
    
    # Apply user counterfactual overrides if provided
    if overrides:
        features.update(overrides)
        
    prob_allowed = 50.0  # Baseline
    supporting_factors = []
    risk_factors = []
    missing_info = []
    
    # 1. Landlord/Tenant Disputes
    if "tenant" in category.lower() or "landlord" in category.lower() or "property" in category.lower():
        if features["written_contract"]:
            prob_allowed += 20
            supporting_factors.append("Written lease agreement is present, which clearly outlines terms and deposit obligations.")
        else:
            prob_allowed -= 15
            risk_factors.append("Oral tenancy agreement is difficult to substantiate in civil courts under the Transfer of Property Act.")
            missing_info.append("Copy of written lease/rent agreement or confirmation of lease terms.")
            
        if features["receipt_exists"]:
            prob_allowed += 15
            supporting_factors.append("Payment receipts or bank transfer proofs substantiate the deposit/rent transaction.")
        else:
            prob_allowed -= 15
            risk_factors.append("Lack of payment receipts makes verifying security deposit payout highly challenging.")
            missing_info.append("Bank statement showing security deposit debit or cash receipts.")
            
        if features["notice_sent"]:
            prob_allowed += 15
            supporting_factors.append("Eviction or vacation notice was formally sent to the opposite party.")
        else:
            prob_allowed -= 10
            risk_factors.append("Failure to send formal legal notice to return security deposit weakens immediate cause of action.")
            missing_info.append("Proof of legal notice served to the landlord requesting refund.")
            
        if features["evidence_present"]:
            prob_allowed += 10
            supporting_factors.append("Condition reports, photographs, or communications verify status of premises.")
        else:
            prob_allowed -= 5
            risk_factors.append("Absence of photos or move-out checklist allows opposite party to claim property damage.")
            missing_info.append("Photographs of the vacated property to disprove damage claims.")

    # 2. Cheque / Payment Disputes (Section 138 NI Act)
    elif "cheque" in category.lower() or "payment" in category.lower():
        # Notice is a MANDATORY STATUTORY CONDITION for Section 138
        if features["notice_sent"]:
            prob_allowed += 25
            supporting_factors.append("Statutory demand notice was sent within 30 days of cheque return memo.")
        else:
            # If notice is not sent, 138 complaint is legally incompetent
            prob_allowed = 5.0
            risk_factors.append("CRITICAL: Statutory legal notice was not sent to the drawer within 30 days. Section 138 NI Act complaint is legally inadmissible.")
            missing_info.append("Statutory 138 demand notice delivery tracking or copy.")
            
        if prob_allowed > 5:
            if features["written_contract"] or features["receipt_exists"]:
                prob_allowed += 20
                supporting_factors.append("Invoices, ledger records, or signed supply contracts prove a legally enforceable debt exists (Section 139 presumption).")
            else:
                prob_allowed -= 20
                risk_factors.append("Lack of underlying invoices makes rebutting the security cheque defence difficult.")
                missing_info.append("Invoices, loan agreement, or ledger book showing legally enforceable debt.")
                
            if features["evidence_present"]:
                prob_allowed += 10
                supporting_factors.append("Original cheque return memo and written acknowledgements are available.")
            else:
                prob_allowed -= 10
                risk_factors.append("Absence of bank return memo or original cheque copy weakens secondary evidence filing.")
                missing_info.append("Original cheque return memo from the bank.")

    # 3. Cybercrime / Online Fraud
    elif "cyber" in category.lower() or "fraud" in category.lower() or "online" in category.lower():
        if features["evidence_present"]:
            prob_allowed += 25
            supporting_factors.append("Digital forensic evidence (IP logs, WhatsApp chats, email headers) links transaction to accused.")
        else:
            prob_allowed -= 20
            risk_factors.append("Lack of IP logs or bank-certified account statements prevents linking the suspect to the device.")
            missing_info.append("Certified server logs, email headers, or transaction history.")
            
        if features["receipt_exists"]:
            prob_allowed += 15
            supporting_factors.append("Bank transaction screenshots and wallet transactions verify the monetary loss.")
        else:
            prob_allowed -= 10
            risk_factors.append("No official bank statement proving unauthorized debit has been annexed.")
            missing_info.append("Official bank statement or card transaction logs.")
            
        if features["notice_sent"]:
            prob_allowed += 10
            supporting_factors.append("Immediate complaint was registered with the National Cyber Crime Portal or bank.")
        else:
            prob_allowed -= 15
            risk_factors.append("Delay in reporting to the Cyber Cell or bank limits chances of freezing the fraudulent account.")
            missing_info.append("Cyber cell complaint copy or portal acknowledgement.")

    # 4. Family Law / Maintenance
    elif "family" in category.lower() or "maintenance" in category.lower() or "domestic" in category.lower():
        if features["receipt_exists"]:
            prob_allowed += 20
            supporting_factors.append("Income proof of the husband (ITRs, pay slips) has been presented to justify maintenance amount.")
        else:
            prob_allowed -= 15
            risk_factors.append("Absence of husband's income proof makes fixing reasonable alimony/maintenance challenging.")
            missing_info.append("Husband's salary certificate, bank statement, or assets statement.")
            
        if features["evidence_present"]:
            prob_allowed += 20
            supporting_factors.append("Physical injury certificates, chat transcripts, or witness statements corroborate allegations of cruelty.")
        else:
            prob_allowed -= 10
            risk_factors.append("Lack of independent corroborative evidence makes allegations of abuse vulnerable to counter-claims.")
            missing_info.append("Medical certificates or witness testimonies of family disputes.")

    # 5. General fallback category (Civil/Criminal Law)
    else:
        if features["written_contract"]:
            prob_allowed += 15
            supporting_factors.append("Documentary agreement or record is present to support claims.")
        if features["evidence_present"]:
            prob_allowed += 15
            supporting_factors.append("Corroborating witness testimonies or physical evidence are present.")
        else:
            prob_allowed -= 10
            risk_factors.append("Lack of direct physical or documentary evidence hinders proving claims beyond reasonable doubt.")
            missing_info.append("Independent eyewitness statements or documentary files.")
        if features["receipt_exists"]:
            prob_allowed += 10
            supporting_factors.append("Financial records substantiate the underlying transaction.")

    # Ensure bounds [5%, 95%]
    prob_allowed = max(5.0, min(95.0, prob_allowed))
    prob_dismissed = 100.0 - prob_allowed
    
    # Calculate confidence score
    confidence_score = 50.0  # Baseline
    if features["written_contract"]:
        confidence_score += 10
    if features["evidence_present"]:
        confidence_score += 15
    if features["receipt_exists"]:
        confidence_score += 10
    if features["notice_sent"]:
        confidence_score += 10
        
    # Subtract confidence if there are missing details
    confidence_score -= (len(missing_info) * 8)
    confidence_score = max(35.0, min(95.0, confidence_score))
    
    # Determine outcomes terminology based on category
    outcome_label_allowed = "Allowed"
    outcome_label_dismissed = "Dismissed"
    
    if "criminal" in category.lower() or "cybercrime" in category.lower():
        outcome_label_allowed = "Conviction / Allowed"
        outcome_label_dismissed = "Acquittal / Dismissed"
    elif "cheque" in category.lower():
        outcome_label_allowed = "Convicted (Allowed)"
        outcome_label_dismissed = "Acquitted (Dismissed)"
    elif "family" in category.lower() and "maintenance" in category.lower():
        outcome_label_allowed = "Maintenance Granted"
        outcome_label_dismissed = "Maintenance Denied"
        
    return {
        "probabilities": [
            {"label": outcome_label_allowed, "probability": float(round(prob_allowed, 1))},
            {"label": outcome_label_dismissed, "probability": float(round(prob_dismissed, 1))}
        ],
        "confidence_score": float(round(confidence_score, 1)),
        "supporting_factors": supporting_factors,
        "risk_factors": risk_factors,
        "missing_information": missing_info,
        "factual_features": features,
        "explanation": f"The system estimates a {prob_allowed:.1f}% probability of outcome being {outcome_label_allowed} because "
                       f"{'written documents are available' if features['written_contract'] else 'there is a lack of formal written contracts'}. "
                       f"Additionally, the confidence level is {confidence_score:.1f}% based on completeness of fact inputs."
    }
