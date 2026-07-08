# report_generator.py
# Generate downloadable PDF reports

from fpdf import FPDF
from datetime import datetime


class ResumeReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(52, 152, 219)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'AI Resume Analysis Report', 0, 1, 'C', True)
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')
    
    def section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(52, 73, 94)
        self.set_fill_color(236, 240, 241)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.ln(2)
    
    def section_body(self, text):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        # Clean text to remove problematic characters
        clean = text.encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 7, clean)
        self.ln(3)
    
    def add_score_box(self, score):
        self.set_font('Arial', 'B', 24)
        if score >= 70:
            self.set_text_color(46, 204, 113)
        elif score >= 40:
            self.set_text_color(243, 156, 18)
        else:
            self.set_text_color(231, 76, 60)
        self.cell(0, 15, f'Match Score: {score:.2f}%', 0, 1, 'C')
        self.ln(5)
    
    def add_skills_list(self, title, skills, color):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(*color)
        self.cell(0, 8, title, 0, 1)
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        if skills:
            skills_text = ", ".join(sorted(skills))
            clean = skills_text.encode('latin-1', 'replace').decode('latin-1')
            self.multi_cell(0, 6, clean)
        else:
            self.cell(0, 6, "None detected", 0, 1)
        self.ln(3)


def generate_pdf_report(match_score, analysis, suggestions):
    """Generate a professional PDF report."""
    pdf = ResumeReport()
    pdf.add_page()
    
    # Score Section
    pdf.section_title('Overall Match Score')
    pdf.add_score_box(match_score)
    
    # Summary
    pdf.section_title('Analysis Summary')
    summary = (
        f"Total skills found in resume: {len(analysis['resume_skills'])}\n"
        f"Total skills required by job: {len(analysis['job_skills'])}\n"
        f"Matched skills: {len(analysis['matched_skills'])}\n"
        f"Missing skills: {len(analysis['missing_skills'])}\n"
        f"Extra skills (bonus): {len(analysis['extra_skills'])}"
    )
    pdf.section_body(summary)
    
    # Matched Skills
    pdf.section_title('Skills Analysis')
    pdf.add_skills_list('Matched Skills:', analysis['matched_skills'], (46, 204, 113))
    pdf.add_skills_list('Missing Skills:', analysis['missing_skills'], (231, 76, 60))
    pdf.add_skills_list('Extra Skills:', analysis['extra_skills'], (52, 152, 219))
    
    # Suggestions
      # Suggestions
    pdf.add_page()
    pdf.section_title('AI-Powered Suggestions')
    for i, suggestion in enumerate(suggestions, 1):
        clean_suggestion = ''.join(c for c in suggestion if ord(c) < 128)
        pdf.section_body(f"{i}. {clean_suggestion}")
    
    # Return PDF as bytes (fixed for compatibility)
    output = pdf.output(dest='S')
    if isinstance(output, str):
        return output.encode('latin-1')
    return bytes(output)