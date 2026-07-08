# analyzer.py
# Core AI logic for resume analysis

from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills_database import SKILLS_DATABASE, get_all_skills, get_skill_category
import re


def extract_text_from_pdf(file):
    """Extract text from uploaded PDF file."""
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text


def clean_text(text):
    """Clean and normalize text."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s+#]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def calculate_match_score(resume_text, job_text):
    """Calculate similarity score using TF-IDF + Cosine Similarity."""
    documents = [clean_text(resume_text), clean_text(job_text)]
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(documents)
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
    return round(score, 2)


def extract_skills(text):
    """Extract skills from text using the skills database."""
    text = clean_text(text)
    found_skills = set()
    all_skills = get_all_skills()
    
    for skill in all_skills:
        # Match whole word or phrase
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found_skills.add(skill)
    
    return found_skills


def analyze_skills(resume_text, job_text):
    """Compare skills between resume and job description."""
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)
    
    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills
    extra_skills = resume_skills - job_skills
    
    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills
    }


def categorize_skills(skills):
    """Group skills by category."""
    categorized = {}
    for skill in skills:
        category = get_skill_category(skill)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(skill)
    return categorized


def generate_suggestions(analysis, match_score):
    """Generate AI-powered suggestions for resume improvement."""
    suggestions = []
    
    if match_score < 40:
        suggestions.append("⚠️ Low match score. Consider tailoring your resume specifically for this role.")
    elif match_score < 70:
        suggestions.append("📈 Moderate match. Adding a few key skills could significantly improve your chances.")
    else:
        suggestions.append("✅ Great match! Your resume aligns well with this job.")
    
    missing = analysis["missing_skills"]
    if missing:
        top_missing = list(missing)[:5]
        suggestions.append(f"🎯 **Priority skills to add:** {', '.join(top_missing)}")
        
        # Category-based suggestions
        missing_categories = categorize_skills(missing)
        for category, skills in missing_categories.items():
            if len(skills) >= 2:
                suggestions.append(f"📚 Consider strengthening your **{category}** skills: {', '.join(skills[:3])}")
    
    if len(analysis["matched_skills"]) < 3:
        suggestions.append("💡 Highlight more relevant technical skills in your resume.")
    
    if analysis["extra_skills"]:
        suggestions.append(f"✨ You have {len(analysis['extra_skills'])} additional skills that could be valuable for other roles.")
    
    return suggestions