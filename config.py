import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "CareerAI"
DATABASE_NAME = "career_ai.db"

GEMINI_API_KEY = os.getenv("YOUR API KEY")