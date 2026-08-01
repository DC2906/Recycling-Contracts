"""
Streamlit Web Server Root Entrypoint for Cloud Deployment
(Streamlit Community Cloud, Render, Hugging Face Spaces, Railway, Heroku)
"""
import runpy
import os

if __name__ == "__main__":
    script_path = os.path.join(os.path.dirname(__file__), "execution", "02_dashboard.py")
    runpy.run_path(script_path, run_name="__main__")
