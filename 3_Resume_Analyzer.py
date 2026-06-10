import os, io
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from pypdf import PdfReader  # or pypdf

st.set_page_config(page_title="Resume Analyzer", page_icon="📄")

def get_model():
    load_dotenv()
    try:
        cloud_key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    except Exception:
        cloud_key = None
    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or cloud_key
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    if not key: 
        st.error("Missing GOOGLE_API_KEY (or GEMINI_API_KEY)"); st.stop()
    genai.configure(api_key=key)
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config={"temperature": 0.25, "max_output_tokens": 800},
        system_instruction=(
            "You analyze resumes and give focused, actionable feedback for ATS and interviews. "
            "Be specific: bullet points, quantify impact, and suggest 2–3 improvements."
        ),
    )

st.title("📄 Resume Analyzer")

up = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
role = st.text_input("Target role (optional)", "Data Analyst")

if st.button("Analyze") and up:
    # extract text
    text = ""
    reader = PdfReader(io.BytesIO(up.read()))
    for page in reader.pages:
        text += page.extract_text() or ""

    if not text.strip():
        st.error("Could not extract text from PDF. Try another file or a text-based PDF.")
        st.stop()

    model = get_model()
    prompt = f"Target role: {role}\n\nResume:\n{text[:15000]}"  # keep under context limits
    with st.spinner("Analyzing…"):
        resp = model.generate_content(prompt)
        st.markdown(resp.text)
