import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

settings = Settings()

