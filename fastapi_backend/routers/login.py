from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from security import token
from security.hashing import Hash

from sqlalchemy.orm import Session
from models import Users
from database import get_db

router = APIRouter(
    tags = ['로그인']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    `로그인 API`\n
    로그인하면 Token을 발행해줍니다.
    """
    user = db.query(Users).filter(Users.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invaild Credentials")
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"email": user.email, "auth": user.auth})
    return {
            "access_token": access_token,
            "token_type": "bearer",
            "uid": user.uid,
            "auth": user.auth
            }