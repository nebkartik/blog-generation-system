from typing import List
from fastapi import Depends, APIRouter, status, Response, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model import Blog, Users
from states import ShowBlog, BlogState,UserState
router = APIRouter(
prefix="/users",
tags=['Users']
)


# User Creation
@router.post("/usercreate")
def user_create(request:UserState,db:Session = Depends(get_db)):
    new_user = Users(**request.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



# User Retrieval
@router.get('/getuser')
def getuser(db:Session = Depends(get_db)):
    users = db.query(Users).all()
    return users
