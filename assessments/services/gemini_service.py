import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# ✅ Pylance-safe imports
from google.generativeai import configure # type: ignore
from google.generativeai.generative_models import GenerativeModel


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

load_dotenv()

# ===============================
# LOGGING
# ===============================
logger = logging.getLogger(__name__)

# ===============================
# GEMINI CONFIG (SECURE & CLEAN)
# ===============================
configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"
model = GenerativeModel(MODEL_NAME)

PDF_DIR = "generated_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)


# ===============================
# PROMPT BUILDER
# ===============================
def build_prompt(data: dict) -> str:
    return f"""
You are a senior university examination paper setter.

Generate a FORMAL, PRINT-READY university examination paper.

Course Code: {data['courseCode']}
Subject: {data['subject']}
Topic: {data['topic']}

Follow CLOs and PLOs strictly.
"""


# ===============================
# GEMINI CALL
# ===============================
def generate_assessment(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text


# ===============================
# PDF GENERATOR
# ===============================
def create_pdf(text: str) -> str:
    filename = f"Assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(PDF_DIR, filename)

    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for line in text.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 6))

    doc.build(story)
    return filename


# ===============================
# MAIN SERVICE FUNCTION
# ===============================
def generate_assessment_pdf(data: dict) -> str:
    prompt = build_prompt(data)
    text = generate_assessment(prompt)
    return create_pdf(text)
