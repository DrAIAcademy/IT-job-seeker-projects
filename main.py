"""
Main Streamlit application for IT Job Seeker App
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from frontend.pages import *
from frontend.components.sidebar import render_sidebar
from dotenv import load_dotenv

# Load environment variables locally. On Streamlit Cloud, use Settings > Secrets.
load_dotenv()

def get_secret_or_env(name, default=None):
    try:
        return st.secrets.get(name, os.getenv(name, default))
    except Exception:
        return os.getenv(name, default)

if get_secret_or_env("GOOGLE_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = get_secret_or_env("GOOGLE_API_KEY")
if get_secret_or_env("GEMINI_API_KEY") and not os.getenv("GEMINI_API_KEY"):
    os.environ["GEMINI_API_KEY"] = get_secret_or_env("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="IT Job Seeker Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/it-job-seeker-app',
        'Report a bug': "https://github.com/your-repo/it-job-seeker-app/issues",
        'About': "# IT Job Seeker Assistant\nAI-powered platform to help IT professionals find their dream jobs!"
    }
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .job-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .skill-tag {
        background: #f0f8ff;
        color: #1e3a8a;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.875rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Render sidebar
    render_sidebar()
    
    # Initialize session state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    
    if 'job_preferences' not in st.session_state:
        st.session_state.job_preferences = {}
        
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Main header
    st.title("🚀 IT Job Seeker Assistant")
    st.markdown("### AI-powered platform to accelerate your tech career")
    
    # Check API key
    if not (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")):
        st.error("⚠️ Gemini API key not found! Add GOOGLE_API_KEY in Streamlit Secrets or local .env file.")
        st.info("Get your API key from: https://ai.google.dev/")
        st.stop()
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>1000+</h3>
            <p>Job Opportunities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>50+</h3>
            <p>Tech Companies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>AI-Powered</h3>
            <p>Resume Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>24/7</h3>
            <p>Career Support</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature highlights
    st.markdown("## 🌟 Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔍 Intelligent Job Search
        - AI-powered job matching
        - Personalized recommendations
        - Real-time market insights
        - Salary analysis
        
        ### 📄 Resume Optimization
        - ATS compatibility check
        - Keyword optimization
        - Industry-specific suggestions
        - Format recommendations
        """)
    
    with col2:
        st.markdown("""
        ### 💬 Career Assistant
        - 24/7 AI career counselor
        - Interview preparation
        - Skill gap analysis
        - Career path guidance
        
        ### 📊 Analytics Dashboard
        - Application tracking
        - Success metrics
        - Market trends
        - Performance insights
        """)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("## 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Start Job Search", use_container_width=True):
            st.switch_page("pages/2_Job_Search.py")
    
    with col2:
        if st.button("📄 Analyze Resume", use_container_width=True):
            st.switch_page("pages/3_Resume_Analyzer.py")
    
    with col3:
        if st.button("💬 Get Career Advice", use_container_width=True):
            st.switch_page("pages/4_Career_Assistant.py")
    
    st.markdown("---")
    
    # Recent activity (placeholder)
    st.markdown("## 📈 Your Activity")
    
    tab1, tab2, tab3 = st.tabs(["Recent Searches", "Saved Jobs", "Applications"])
    
    with tab1:
        st.info("No recent searches. Start exploring jobs!")
    
    with tab2:
        st.info("No saved jobs yet. Find interesting opportunities and save them!")
    
    with tab3:
        st.info("No applications tracked. Use our application tracker to monitor your progress!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 2rem;'>
        <p>Built with ❤️ using Streamlit, LangChain, and Google Gemini AI</p>
        <p>© 2025 IT Job Seeker Assistant. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()