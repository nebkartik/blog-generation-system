from fastapi import APIRouter, Depends, HTTPException, status
from states import UserLoginState
from database import get_db
from sqlalchemy.orm import Session
from model import Users

router = APIRouter(
    prefix="/login",
    tags=['Login']
)

@router.post("/userlogin")
def user_login(request:UserLoginState,db: Session = Depends(get_db)):
    user = db.query(Users).filter(request.name == Users.name).first()
    if user:
        return {"message": "Login successful"}
    else:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")