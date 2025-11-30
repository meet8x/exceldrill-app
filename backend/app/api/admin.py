from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, EmailStr

from backend.app.api import deps
from backend.app.models.user import User

router = APIRouter()

class UserListResponse(BaseModel):
    id: int
    email: str
    full_name: str | None
    is_active: bool
    is_paid: bool
    is_verified: bool
    plan_type: str | None
    plan_expiry: str | None
    
    class Config:
        orm_mode = True

class AdminStatsResponse(BaseModel):
    total_users: int
    verified_users: int
    premium_users: int
    active_users: int

class GrantPremiumRequest(BaseModel):
    user_id: int
    plan_type: str = "lifetime"

def get_current_admin(current_user: User = Depends(deps.get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_stats(
    db: Session = Depends(deps.get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    total_users = db.query(func.count(User.id)).scalar()
    verified_users = db.query(func.count(User.id)).filter(User.is_verified == True).scalar()
    premium_users = db.query(func.count(User.id)).filter(User.is_paid == True).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    
    return {
        "total_users": total_users,
        "verified_users": verified_users,
        "premium_users": premium_users,
        "active_users": active_users
    }

@router.get("/users", response_model=List[UserListResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/grant-premium")
def grant_premium(
    request: GrantPremiumRequest,
    db: Session = Depends(deps.get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_paid = True
    user.plan_type = request.plan_type
    user.plan_expiry = None  # Lifetime
    db.commit()
    
    return {"message": f"Premium access granted to {user.email}"}

@router.post("/revoke-premium")
def revoke_premium(
    user_id: int,
    db: Session = Depends(deps.get_db),
    admin: User = Depends(get_current_admin)
) -> Any:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_paid = False
    user.plan_type = None
    user.plan_expiry = None
    db.commit()
    
    return {"message": f"Premium access revoked from {user.email}"}
