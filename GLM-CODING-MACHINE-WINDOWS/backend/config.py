import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "desktop")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL = os.getenv("MODEL", "gpt-5.6")
    WORKSPACE_ROOT = os.path.abspath(os.getenv("WORKSPACE_ROOT", "./workspace"))