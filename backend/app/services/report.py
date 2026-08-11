from fpdf import FPDF
import io
from typing import Dict, Any

class NyayaPDFReport(FPDF):
    def header(self):
        # Top banner decoration
        self.set_fill_color(16, 44, 87) # Deep Navy
        self.rect(0, 0, 210, 15, "F")
        
        # Header text
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, -5, "NYAYAAI – AI-POWERED LEGAL RESEARCH & ANALYSIS REPORT", 0, 0, "C")
        self.ln(12)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_fill_color(220, 220, 220)
        self.rect(0, 282, 210, 15, "F")
        
        self.set_text_color(50, 50, 50)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, "Disclaimer: AI-generated research summary. Verify with official sources. Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")

def generate_pdf_report(case_data: Dict[str, Any], analysis: Dict[str, Any], similarity: list, prediction: Dict[str, Any]) -> bytes:
    """Generate a clean case-analysis report in PDF format."""
    pdf = NyayaPDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # 1. REPORT TITLE BLOCK
    pdf.set_y(25)
    pdf.set_text_color(16, 44, 87) # Deep Navy
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 10, "CASE ANALYSIS REPORT", 0, 1, "C")
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(180, 140, 40) # Gold Accent
    pdf.cell(0, 6, "NYAYAAI LEGAL DECISION SUPPORT SYSTEM", 0, 1, "C")
    pdf.ln(5)
    
    # Draw horizontal rule
    pdf.set_draw_color(16, 44, 87)
    pdf.set_linewidth(1)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    # Meta table
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(35, 6, "Case ID:", 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(60, 6, str(case_data.get("id", "N/A")), 0, 0)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(35, 6, "Date Analyzed:", 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(60, 6, case_data.get("created_at", "Just Now"), 0, 1)

    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(35, 6, "Case Title:", 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(60, 6, case_data.get("title", "Case Summary"), 0, 0)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(35, 6, "Legal Category:", 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(60, 6, prediction.get("category", "General Civil"), 0, 1)
    
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(35, 6, "State Jurisdict:", 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(60, 6, analysis.get("location", "Not Specified"), 0, 0)
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(35, 6, "Disputed Amount:", 0, 0)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(60, 6, str(analysis.get("disputed_amount", "Not Specified")), 0, 1)
    pdf.ln(8)

    # 2. FACTS DESCRIPTION
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(16, 44, 87)
    pdf.cell(0, 8, "1. Fact Summary", 0, 1)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 5, case_data.get("description", ""))
    pdf.ln(5)

    # 3. IDENTIFIED LAWS (PROVISIONS)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(16, 44, 87)
    pdf.cell(0, 8, "2. Potentially Relevant Provisions", 0, 1)
    
    citations = analysis.get("citations", [])
    pdf.set_font("Helvetica", "", 10)
    if not citations:
        pdf.cell(0, 6, "No specific sections mentioned. Standard code provisions apply.", 0, 1)
    else:
        for cit in citations:
            pdf.cell(0, 6, f"- {cit} [Potentially Relevant]", 0, 1)
    pdf.ln(5)

    # 4. SIMILAR CASES
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(16, 44, 87)
    pdf.cell(0, 8, "3. Top Similar Judgments & Outcomes", 0, 1)
    
    if not similarity:
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 6, "No similar historical cases found in seed database.", 0, 1)
    else:
        for i, sc in enumerate(similarity[:3]):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.cell(0, 6, f"{i+1}. {sc['case_name']} (Similarity: {sc['similarity_score']}%)", 0, 1)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(30, 5, "   Court/State:", 0, 0)
            pdf.cell(100, 5, f"{sc['court']}, {sc['state']}", 0, 1)
            pdf.cell(30, 5, "   Outcome:", 0, 0)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(16, 44, 87)
            pdf.cell(100, 5, sc['outcome'], 0, 1)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(30, 5, "   Retrieved Because:", 0, 0)
            pdf.cell(150, 5, sc['why_similar'], 0, 1)
            pdf.ln(2)
    pdf.ln(3)

    # 5. HISTORICAL OUTCOME ASSESSMENT
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(16, 44, 87)
    pdf.cell(0, 8, "4. Outcome Prediction & Confidence Dials", 0, 1)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(40, 6, "Confidence Score:", 0, 0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(180, 140, 40)
    pdf.cell(30, 6, f"{prediction.get('confidence_score', 0)}%", 0, 1)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 6, "Estimated Probability Distributions:", 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    for prob in prediction.get("probabilities", []):
        pdf.cell(60, 6, f"- {prob['label']}:", 0, 0)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(30, 6, f"{prob['probability']}%", 0, 1)
        pdf.set_font("Helvetica", "", 10)
    pdf.ln(5)

    # 6. EXPLAINABILITY: SUPPORTING & RISK FACTORS
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(16, 44, 87)
    pdf.cell(0, 8, "5. Factual & Procedural Strengths", 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    sup_factors = prediction.get("supporting_factors", [])
    if not sup_factors:
        pdf.cell(0, 6, "No major positive evidence factors identified.", 0, 1)
    else:
        for factor in sup_factors:
            pdf.multi_cell(0, 5, f"   [+] {factor}")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(16, 44, 87)
    pdf.cell(0, 8, "6. Risk Factors & Vulnerabilities", 0, 1)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    risk_factors = prediction.get("risk_factors", [])
    if not risk_factors:
        pdf.cell(0, 6, "No major vulnerability risk factors identified.", 0, 1)
    else:
        for factor in risk_factors:
            pdf.multi_cell(0, 5, f"   [-] {factor}")
    pdf.ln(3)

    # 7. IMPORTANT LEGAL DISCLAIMER
    pdf.ln(5)
    pdf.set_fill_color(249, 244, 230) # Light beige disclaimer box
    pdf.set_draw_color(180, 140, 40)
    pdf.rect(10, pdf.get_y(), 190, 32, "FD")
    
    pdf.set_y(pdf.get_y() + 2)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(180, 140, 40)
    pdf.cell(0, 6, "   CRITICAL LEGAL SAFETY NOTICE & DISCLAIMER", 0, 1, "L")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(80, 80, 80)
    disclaimer_text = (
        "   NyayaAI provides AI-assisted legal research and educational information only. It is not a substitute "
        "for professional legal advice and does not guarantee any legal outcome. Users should verify information "
        "with current official legal sources and consult a qualified legal professional."
    )
    pdf.multi_cell(185, 4, disclaimer_text)
    
    # Return binary PDF stream
    return bytes(pdf.output())
