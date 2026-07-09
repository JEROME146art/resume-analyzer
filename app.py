# app.py
# AI Resume & Job Description Matcher - Main Application

import streamlit as st
from analyzer import (
    extract_text_from_pdf,
    clean_text,
    calculate_match_score,
    analyze_skills,
    generate_suggestions,
    suggest_job_roles
)
from visualizer import (
    create_match_gauge,
    create_skills_pie_chart,
    create_category_bar_chart,
    create_wordcloud,
    create_comparison_chart
)
from report_generator import generate_pdf_report

# --- Page Config ---
st.set_page_config(
    page_title="AI Resume Analyzer Pro | Built by Jerome",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/JEROME146art/resume-analyzer',
        'Report a bug': 'https://github.com/JEROME146art/resume-analyzer/issues',
        'About': """
        # AI Resume Analyzer Pro 🤖
        
        **Built with ❤️ by Jerome**
        
        An intelligent resume analysis tool powered by:
        - TF-IDF Vectorization
        - Cosine Similarity
        - NLP Skill Extraction
        
        **GitHub:** https://github.com/JEROME146art/resume-analyzer
        """
    }
)
# --- Header ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("# 🤖")
with col_title:
    st.markdown("# AI Resume Analyzer Pro")
    st.markdown("**Powered by TF-IDF, Cosine Similarity & NLP** | Built with ❤️ by **Jerome**")

st.markdown("---")

# Info banner

st.info("🚀 **New:** AI-powered job role suggestions based on your skills!")
# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.radio(
        "Analysis Mode",
        ["Single Resume Analysis", "Multiple Resume Comparison"]
    )
    st.markdown("---")
    st.markdown("### 📖 About")
    st.info(
        "This AI-powered tool analyzes resumes against job descriptions using:\n\n"
        "- **TF-IDF Vectorization**\n"
        "- **Cosine Similarity**\n"
        "- **NLP Skill Extraction**\n"
        "- **Category-based Analysis**"
    )

# ==========================================
# MODE 1: SINGLE RESUME ANALYSIS
# ==========================================
if mode == "Single Resume Analysis":
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📄 Upload Resume")
        uploaded_file = st.file_uploader("Choose PDF Resume", type="pdf", key="single")
    
    with col2:
        st.header("💼 Job Description")
        job_description = st.text_area("Paste job description here", height=250)
    
    if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
        if uploaded_file and job_description:
            with st.spinner('🔍 Analyzing... Please wait'):
                resume_text = extract_text_from_pdf(uploaded_file)
                match_score = calculate_match_score(resume_text, job_description)
                analysis = analyze_skills(resume_text, job_description)
                suggestions = generate_suggestions(analysis, match_score)
                
                st.markdown("---")
                st.header("📊 Analysis Results")
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Match Score", f"{match_score}%")
                m2.metric("Matched Skills", len(analysis['matched_skills']))
                m3.metric("Missing Skills", len(analysis['missing_skills']))
                m4.metric("Extra Skills", len(analysis['extra_skills']))
                
                st.plotly_chart(create_match_gauge(match_score), use_container_width=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.plotly_chart(
                        create_skills_pie_chart(
                            len(analysis['matched_skills']),
                            len(analysis['missing_skills'])
                        ),
                        use_container_width=True
                    )
                with c2:
                    if analysis['resume_skills']:
                        st.plotly_chart(
                            create_category_bar_chart(analysis['resume_skills']),
                            use_container_width=True
                        )
                
                st.subheader("☁️ Resume Word Cloud")
                if resume_text.strip():
                    fig = create_wordcloud(clean_text(resume_text))
                    st.pyplot(fig)
                
                st.subheader("🎯 Skills Breakdown")
                t1, t2, t3 = st.tabs(["✅ Matched", "❌ Missing", "⭐ Extra"])
                with t1:
                    if analysis['matched_skills']:
                        st.success(", ".join(sorted(analysis['matched_skills'])))
                    else:
                        st.warning("No matching skills detected")
                with t2:
                    if analysis['missing_skills']:
                        st.error(", ".join(sorted(analysis['missing_skills'])))
                    else:
                        st.success("No missing skills! Great job!")
                with t3:
                    if analysis['extra_skills']:
                        st.info(", ".join(sorted(analysis['extra_skills'])))
                    else:
                        st.write("No additional skills detected")
                
                st.subheader("🤖 AI Suggestions")
                for suggestion in suggestions:
                    st.markdown(f"- {suggestion}")
                                # --- Job Role Suggester ---
                st.markdown("---")
                st.subheader("🎯 Recommended Job Roles for You")
                suggested_roles = suggest_job_roles(analysis['resume_skills'])
                
                if suggested_roles:
                    st.markdown("Based on your skills, you're a good fit for these roles:")
                    
                    for i, role in enumerate(suggested_roles, 1):
                        with st.expander(f"#{i} {role['role']} — {role['match']}% match"):
                            st.progress(role['match'] / 100)
                            st.markdown(f"**Your matching skills for this role:**")
                            st.success(", ".join(sorted(role['matched_skills'])))
                else:
                    st.warning("Add more technical skills to get job role suggestions!")
                st.markdown("---")
                st.subheader("📥 Download Report")
                pdf_bytes = generate_pdf_report(match_score, analysis, suggestions)
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=pdf_bytes,
                    file_name="resume_analysis_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.error("⚠️ Please upload a resume AND provide a job description.")

# ==========================================
# MODE 2: MULTIPLE RESUME COMPARISON
# ==========================================
else:
    st.header("📊 Compare Multiple Resumes")
    st.markdown("Upload multiple resumes and rank them against a single job description.")
    
    job_description = st.text_area("💼 Job Description", height=200)
    uploaded_files = st.file_uploader(
        "📄 Upload Multiple PDF Resumes",
        type="pdf",
        accept_multiple_files=True
    )
    
    if st.button("🚀 Compare All Resumes", type="primary", use_container_width=True):
        if uploaded_files and job_description:
            with st.spinner('🔍 Analyzing all resumes...'):
                results = []
                for file in uploaded_files:
                    resume_text = extract_text_from_pdf(file)
                    score = calculate_match_score(resume_text, job_description)
                    analysis = analyze_skills(resume_text, job_description)
                    results.append({
                        'name': file.name,
                        'score': score,
                        'matched': len(analysis['matched_skills']),
                        'missing': len(analysis['missing_skills'])
                    })
                
                results.sort(key=lambda x: x['score'], reverse=True)
                
                st.markdown("---")
                st.header("🏆 Ranking Results")
                
                st.plotly_chart(create_comparison_chart(results), use_container_width=True)
                
                st.subheader("📋 Detailed Rankings")
                for i, r in enumerate(results, 1):
                    with st.expander(f"#{i} - {r['name']} — Score: {r['score']:.2f}%"):
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Match Score", f"{r['score']:.2f}%")
                        c2.metric("Matched Skills", r['matched'])
                        c3.metric("Missing Skills", r['missing'])
        else:
            st.error("⚠️ Please upload resumes AND provide a job description.")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Built with ❤️ using Streamlit | AI Resume Analyzer Pro"
    "</div>",
    unsafe_allow_html=True
)