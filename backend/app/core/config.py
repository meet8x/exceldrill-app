import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Exceldrill AI"
    
    # Security
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"
    
    # Payment (Razorpay)
    # Get these from https://dashboard.razorpay.com/app/keys
    RAZORPAY_KEY_ID: str = os.getenv("RAZORPAY_KEY_ID", "rzp_test_1DP5mmOlF5G5ag")
    RAZORPAY_KEY_SECRET: str = os.getenv("RAZORPAY_KEY_SECRET", "")
    
    # Email Settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "meettheanalyst@gmail.com"
    SMTP_PASSWORD: str = "ualr sjom xojb mncg"
    EMAILS_FROM_EMAIL: str = "meettheanalyst@gmail.com"
    EMAILS_FROM_NAME: str = "Exceldrill AI"
    
    # Google SSO
    GOOGLE_CLIENT_ID: str = "90600034364-o8r416gis9gqplo3ldt0a4tbpdonbm4q.apps.googleusercontent.com"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

# Validate Razorpay keys on startup
if not settings.RAZORPAY_KEY_SECRET or settings.RAZORPAY_KEY_SECRET == "":
    print("⚠️  WARNING: RAZORPAY_KEY_SECRET is not set!")
    print("⚠️  Payment functionality will NOT work until you set valid Razorpay credentials.")
    print("⚠️  Get your keys from: https://dashboard.razorpay.com/app/keys")
    print("⚠️  Set them in environment variables or .env file:")
    print("⚠️    RAZORPAY_KEY_ID=your_key_id")
    print("⚠️    RAZORPAY_KEY_SECRET=your_key_secret")
