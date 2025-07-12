import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
  DATABASE_URL: str = os.getenv("DATABASE_URL")
  if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
  SECRET_KEY: str = os.getenv("SECRET_KEY")
  if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set.")
  ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
  ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
  DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
  EMAIL_HOST: str = os.getenv("EMAIL_HOST")
  if not EMAIL_HOST:
    raise ValueError("EMAIL_HOST environment variable is not set.")
  EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", "587"))
  if not EMAIL_PORT:
    raise ValueError("EMAIL_PORT environment variable is not set.")
  EMAIL_USER: str = os.getenv("EMAIL_USER")
  if not EMAIL_USER:
    raise ValueError("EMAIL_USER environment variable is not set.")
  EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
  if not EMAIL_PASSWORD:
    raise ValueError("EMAIL_PASSWORD environment variable is not set.")
  EMAIL_FROM: str = os.getenv("EMAIL_FROM")
  if not EMAIL_FROM:
    raise ValueError("EMAIL_FROM environment variable is not set.")
  FRONTEND_URL: str = os.getenv("FRONTEND_URL")
  if not FRONTEND_URL:
    raise ValueError("FRONTEND_URL environment variable is not set.")


Settings = Settings()
