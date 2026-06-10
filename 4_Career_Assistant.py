import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

st.set_page_config(page_title="Career Assistant", page_icon="💬")

# ---------- Setup & helpers ----------
def get_api_key_and_model():
    load_dotenv()  # reads .env locally; Streamlit Cloud uses st.secrets
    try:
        cloud_key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        cloud_model = st.secrets.get("GEMINI_MODEL")
    except Exception:
        cloud_key = None
        cloud_model = None

    key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or cloud_key
    model_name = os.getenv("GEMINI_MODEL") or cloud_model or "gemini-1.5-flash"

    if not key:
        st.error("Missing GOOGLE_API_KEY. Add it in Streamlit Secrets or local .env file.")
        st.stop()
    return key, model_name

def get_model():
    api_key, model_name = get_api_key_and_model()
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.3,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 512,
    }

    # Optional system instruction for consistent tone
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        system_instruction=(
            "You are a concise, practical career assistant. "
            "Give step-by-step, actionable advice for students and job seekers. "
            "When useful, list 2–3 specific next steps or resources."
        ),
    )

def start_chat_from_history(model, msgs):
    # Convert Streamlit history (role: user/assistant, content: str) to Gemini chat history
    history = []
    for m in msgs:
        role = "user" if m["role"] == "user" else "model"
        history.append({"role": role, "parts": [m["content"]]})
    return model.start_chat(history=history)

# ---------- UI ----------
st.title("💬 Career Assistant (Gemini)")

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hi! Ask me about jobs, resumes, skills, or interview prep."
    }]

# show chat history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# input box
user_msg = st.chat_input("Type your question…")
if user_msg:
    # add user message
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    # get model & stream the reply
    model = get_model()
    chat = start_chat_from_history(model, st.session_state.messages[:-1])  # pass history excluding the last user msg
    with st.chat_message("assistant"):
        placeholder = st.empty()
        chunks = []
        try:
            for chunk in chat.send_message(user_msg, stream=True):
                if chunk.text:
                    chunks.append(chunk.text)
                    placeholder.markdown("".join(chunks))
        except Exception as e:
            st.error(f"Gemini error: {e}")
            st.stop()

        answer = "".join(chunks) if chunks else "Sorry, I couldn't generate a response."
        placeholder.markdown(answer)

    # add assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})


