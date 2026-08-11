import re
from typing import Dict, List, Any

# Simple regex-based patterns for Indian legal entity extraction
DATE_PATTERNS = [
    r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',  # 12-08-2023, 1/1/24
    r'\b\d{4}-\d{2}-\d{2}\b',              # 2023-08-12
    r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*,?\s*\d{4}\b' # 12th August, 2023
]

MONEY_PATTERNS = [
    r'(?:Rs\.?|Rupees|INR)\s*([0-9,]+(?:\.\d{2})?)',  # Rs. 50,000, Rupees 10,000
    r'\b([0-9,]+)\s*(?:Rupees|INR|Lakhs|Crores)\b'
]

SECTION_PATTERNS = [
    r'(?:Section|Sec\.?)\s*([0-9A-Za-z/()]+)\s*(?:of\s+the\s+)?([A-Za-z0-9\s]+Act|[A-Za-z\s]+Code|IPC|CrPC|CPC|NI\s+Act)?',
    r'\b([0-9A-Za-z/()]+)\s*(?:of\s+)?(?:IPC|CrPC|CPC|NI\s+Act|IT\s+Act)\b'
]

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", 
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", 
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", 
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", 
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Puducherry"
]

def extract_entities(text: str) -> Dict[str, Any]:
    """
    Extract structured legal metadata from natural-language legal descriptions.
    """
    if not text:
        return {}

    # Extract dates
    dates = []
    for pattern in DATE_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            if m not in dates:
                dates.append(m)

    # Extract money / amounts
    money = []
    for pattern in MONEY_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            # Clean string amount to numbers
            clean_m = re.sub(r'[^\d.]', '', m if isinstance(m, str) else m[0])
            if clean_m and clean_m not in money:
                money.append(f"Rs. {int(float(clean_m)):,}")

    # Extract sections and acts
    citations = []
    for pattern in SECTION_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            sec_num = m[0]
            act_name = m[1].strip() if len(m) > 1 and m[1] else "Indian Penal Code" # Default IPC fallback
            
            # Standardize common acronyms
            if "ipc" in act_name.lower():
                act_name = "Indian Penal Code"
            elif "crpc" in act_name.lower():
                act_name = "Code of Criminal Procedure"
            elif "ni" in act_name.lower():
                act_name = "Negotiable Instruments Act"
            elif "contract" in act_name.lower():
                act_name = "Indian Contract Act"
            elif "property" in act_name.lower():
                act_name = "Transfer of Property Act"
            elif "it act" in act_name.lower() or "information technology" in act_name.lower():
                act_name = "Information Technology Act"
            elif "consumer" in act_name.lower():
                act_name = "Consumer Protection Act"
                
            citation_str = f"Section {sec_num} of {act_name}"
            if citation_str not in citations:
                citations.append(citation_str)

    # Extract location (states)
    states_found = []
    for state in INDIAN_STATES:
        if re.search(r'\b' + re.escape(state) + r'\b', text, re.IGNORECASE):
            states_found.append(state)

    # Simple party extraction (Petitioner / Respondent keywords)
    parties = {"plaintiff": "Tenant/Claimant", "defendant": "Landlord/Opposite Party"}
    landlord_keywords = ["landlord", "owner", "lessor", "builder", "opposite party", "bank", "respondent"]
    tenant_keywords = ["tenant", "lessee", "buyer", "complainant", "petitioner", "victim", "plaintiff"]
    
    found_tenant = False
    found_landlord = False
    for kw in tenant_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE):
            found_tenant = True
            break
    for kw in landlord_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE):
            found_landlord = True
            break
            
    # Compile a chronological timeline
    timeline = []
    sentences = text.split('.')
    for sen in sentences:
        sen_dates = []
        for pattern in DATE_PATTERNS:
            matches = re.findall(pattern, sen, re.IGNORECASE)
            for m in matches:
                if m not in sen_dates:
                    sen_dates.append(m)
        if sen_dates:
            timeline.append({
                "date": sen_dates[0],
                "event": sen.strip()
            })

    # Return structured features
    return {
        "dates": dates,
        "disputed_amount": money[0] if money else "Not Specified",
        "all_amounts": money,
        "citations": citations,
        "location": states_found[0] if states_found else "Not Specified",
        "all_locations": states_found,
        "parties": {
            "claimant": "Petitioner / Complainant" if found_tenant else "Claimant",
            "respondent": "Respondent / Accused" if found_landlord else "Opposite Party"
        },
        "timeline": sorted(timeline, key=lambda x: x["date"]) if timeline else [
            {"date": "Incident Date", "event": "Occurrence of dispute described by user."}
        ]
    }
