import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# --- Helper Functions ---
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

# --- Streamlit UI ---
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("🤖 AI Resume & Job Description Matcher")
st.subheader("Powered by TF-IDF & Cosine Similarity")

col1, col2 = st.columns(2)

with col1:
    st.header("1. Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type="pdf")

with col2:
    st.header("2. Job Description")
    job_description = st.text_area("Paste the Job Description here", height=200)

if st.button("Analyze Match"):
    if uploaded_file and job_description:
        with st.spinner('Analyzing...'):
            resume_text = extract_text_from_pdf(uploaded_file)
            cleaned_resume = clean_text(resume_text)
            cleaned_job = clean_text(job_description)
            
            documents = [cleaned_resume, cleaned_job]
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(documents)
            
            match_percentage = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
            
            st.divider()
            st.header("📊 Analysis Result")
            
            score_color = "green" if match_percentage > 70 else "orange" if match_percentage > 40 else "red"
            st.markdown(f"### Match Score: :{score_color}[{match_percentage:.2f}%]")
            st.progress(match_percentage / 100)

            resume_words = set(cleaned_resume.split())
            job_words = set(cleaned_job.split())
            
            tech_keywords = {'python', 'java', 'sql', 'react', 'machine', 'learning', 'data', 'cloud', 'aws', 'docker', 'statistics', 'analytical'}
            
            found_skills = tech_keywords.intersection(resume_words)
            missing_skills = tech_keywords.intersection(job_words) - resume_words

            c1, c2 = st.columns(2)
            with c1:
                st.success("✅ Skills Found in Resume")
                st.write(", ".join(found_skills) if found_skills else "None detected")
            
            with c2:
                st.warning("❌ Missing Key Skills")
                st.write(", ".join(missing_skills) if missing_skills else "None detected")

    else:
        st.error("Please upload a resume and provide a job description.")