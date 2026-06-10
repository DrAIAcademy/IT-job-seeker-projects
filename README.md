# IT Job Seeker Assistant

Streamlit + Gemini public app for IT job seekers.

## Files required for Streamlit Cloud
- `main.py`
- `requirements.txt`
- `pages/`
- `frontend/`
- `.streamlit/config.toml`

Do not upload `.env` or `.venv`.

## Streamlit Cloud Secrets
Add this in **App > Settings > Secrets**:

```toml
GOOGLE_API_KEY = "your_gemini_api_key_here"
GEMINI_MODEL = "gemini-1.5-flash"
```

## Run locally
```bash
pip install -r requirements.txt
streamlit run main.py
```
