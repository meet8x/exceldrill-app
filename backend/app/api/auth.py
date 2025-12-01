import random
import string
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from backend.app.api import deps
from backend.app.core import security
from backend.app.models.user import User
from backend.app.services.email_service import EmailService

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str | None = None
    is_active: bool
    is_paid: bool
    is_verified: bool
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

@router.post("/register", response_model=UserResponse)
def register(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
) -> Any:
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    otp = generate_otp()
    
    user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_verified=False,
        otp=otp
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Send OTP Email in Background
    email_service = EmailService()
    subject = "Verify your email - Exceldrill AI"
    html_content = f"""
    <html>
        <body>
            <h2>Verify your email</h2>
            <p>Your verification code is: <strong>{otp}</strong></p>
            <p>Please enter this code to complete your registration.</p>
        </body>
    </html>
    """
    background_tasks.add_task(email_service.send_email, user.email, subject, html_content)
        
    return user

@router.post("/verify-otp")
def verify_otp(
    request: VerifyOtpRequest,
    db: Session = Depends(deps.get_db),
) -> Any:
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.otp != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
        
    user.is_verified = True
    user.otp = None # Clear OTP after successful verification
    db.commit()
    
    return {"message": "Email verified successfully"}

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Email not verified. Please verify your email first.",
        )
        
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return current_user

class GoogleAuthRequest(BaseModel):
    credential: str

@router.post("/google", response_model=Token)
def google_auth(
    request: GoogleAuthRequest,
    db: Session = Depends(deps.get_db),
) -> Any:
    import requests
    
    # 1. Verify Google Token
    try:
        # Verify using Google's tokeninfo endpoint
        google_response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={request.credential}")
        if google_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid Google token")
            
        google_data = google_response.json()
        
        # Verify Audience (Client ID)
        if google_data['aud'] != security.settings.GOOGLE_CLIENT_ID:
             raise HTTPException(status_code=400, detail="Invalid token audience")
             
        email = google_data['email']
        name = google_data.get('name')
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google authentication failed: {str(e)}")

    # 2. Check if user exists
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        # 3. Register new user
        # Generate a random password since they use Google to login
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        user = User(
            email=email,
            hashed_password=security.get_password_hash(random_password),
            full_name=name,
            is_verified=True, # Google emails are verified
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # If user exists but wasn't verified (e.g. started normal signup but didn't finish), verify them now
        if not user.is_verified:
            user.is_verified = True
            db.commit()

    # 4. Create Access Token
    access_token_expires = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
