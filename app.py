# app.py
import streamlit as st
from lib.cv_parser import CVParser
from lib.ai_handler import AIHandler

st.set_page_config(layout="wide", page_title="CVScore AI")


def get_score_feedback(score):
    if score >= 90:
        return "Perfect Match 🔥"
    elif score >= 75:
        return "Great Candidate 🌟"
    elif score >= 60:
        return "Good Candidate 👍"
    elif score >= 45:
        return "Fair Candidate 🤔"
    elif score >= 25:
        return "Weak Fit 😔"
    else:
        return "Not a Fit 💀"

# --- UI Title ---
st.title("CVScore AI - Smart Resume Analyzer & Ranker")
st.markdown("This AI-powered tool analyzes, scores, and ranks uploaded resumes based on your job criteria.")

# --- Job Criteria Form ---
with st.container(border=True):
    st.subheader("1. Job Position & Criteria")
    
    col1, col2 = st.columns(2)
    with col1:
        job_title = st.text_input("Job Position / Department", placeholder="e.g., Senior Python Developer")
    
    job_description = st.text_area("Job Description", height=150, placeholder="Describe the responsibilities and general qualifications for the role here...")

    with st.expander("Advanced Settings (Refine the AI Analysis)"):
        must_haves = st.text_input("Must-Have Skills/Qualifications", placeholder="Comma-separated, e.g., 5 years of Python, Django, AWS")
        nice_to_haves = st.text_input("Nice-to-Have Skills/Qualifications", placeholder="Comma-separated, e.g., Docker, CI/CD, React")
        deal_breakers = st.text_input("Deal-Breakers", placeholder="Comma-separated, e.g., Frequent job changes")

# --- CV Upload Area ---
with st.container(border=True):
    st.subheader("2. Upload Candidate Resumes")
    uploaded_files = st.file_uploader(
        "Select one or more resume files (PDF, PNG, JPG)",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

# --- Analysis Button and Logic ---
if st.button("Analyze & Rank All Resumes", type="primary", use_container_width=True, disabled=(not uploaded_files or not job_title)):
    
    if not job_title:
        st.error("Please enter a 'Job Position' to begin.")
    elif not uploaded_files:
        st.error("Please upload at least one resume file.")
    else:
        job_details = {
            "title": job_title,
            "description": job_description,
            "must_haves": must_haves,
            "nice_to_haves": nice_to_haves,
            "deal_breakers": deal_breakers
        }
        
        all_results = []
        
        try:
            ai_handler = AIHandler()
        except ValueError as e:
            st.error(e)
            st.stop()
            
        progress_bar = st.progress(0, text="Initializing analysis...")

        for i, uploaded_file in enumerate(uploaded_files):
            progress_text = f"Analyzing '{uploaded_file.name}'... ({i+1}/{len(uploaded_files)})"
            progress_bar.progress((i + 1) / len(uploaded_files), text=progress_text)

            parser = CVParser(uploaded_file)
            cv_text = parser.get_raw_text()

            analysis_result = ai_handler.analyze_cv(cv_text, job_details)
            analysis_result['original_file_name'] = uploaded_file.name # Keep filename for reference
            all_results.append(analysis_result)

        progress_bar.empty()

        # --- Sort and Display Results ---
        st.subheader("🏆 Analysis Results & Candidate Ranking")
        st.info("Candidates are ranked from the highest score to the lowest.")
        
        sorted_results = sorted(all_results, key=lambda x: x.get('score', 0), reverse=True)
        
        if not sorted_results:
            st.warning("No valid results were generated.")
        else:
            for i, res in enumerate(sorted_results):
                candidate_name = res.get('candidate_name', res.get('original_file_name', 'Unknown'))
                score = res.get('score', 0)
                feedback = get_score_feedback(score)

                with st.container(border=True):
                    # Adım 1: İsim
                    st.header(f"#{i+1} - {candidate_name}")
                    
                    # Adım 2: Büyük Değerlendirme Metni
                    st.subheader(f"{feedback}")
                    
                    # Adım 3: Skor ve AI Özeti yan yana
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.metric(label="Compatibility Score", value=f"{score}/100")
                        
                    with col2:
                         st.markdown(f"**AI Summary:** *{res.get('summary', 'No summary generated.')}*")
                    
                    st.divider()

                    # Avantajlar ve Dezavantajlar
                    col3, col4 = st.columns(2)
                    with col3:
                        if res.get('advantages'):
                            st.success("**Key Advantages:**")
                            for adv in res['advantages']:
                                st.write(f"- {adv}")
                    with col4:
                        if res.get('disadvantages'):
                            st.error("**Disadvantages / Gaps:**")
                            for disadv in res['disadvantages']:
                                st.write(f"- {disadv}")
                    
                    # Mülakat Soruları
                    if res.get('interview_questions'):
                        st.divider()
                        st.info("**Suggested Interview Questions:**")
                        for q in res['interview_questions']:
                            st.write(f"❓ {q}")