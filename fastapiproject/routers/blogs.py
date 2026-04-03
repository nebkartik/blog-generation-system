from typing import List
from fastapi import Depends, APIRouter, status, Response, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model import Blog
from states import ShowBlog, BlogState
router = APIRouter(
prefix="/blogs",
tags=['Blogs']
)

# Dependency Injection
@router.get("/blogsretrieve",response_model=List[ShowBlog])
def retrieve_blogs(db=Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs
 


@router.post("/blogcontent")
def create_blog(request:BlogState,db=Depends(get_db)):
    new_blog = Blog(id=request.id,title=request.title,content=request.content,user_id=request.user_id)
    db.add(new_blog)
    db.commit()  
    db.refresh(new_blog)
    return new_blog




# Status Code Handling
@router.get("/retrieve/{id}",status_code=status.HTTP_200_OK,response_model=BlogState)
def retrieve(id:int,db:Session = Depends(get_db),resp:Response=None):
    blog = db.query(Blog).filter(Blog.id==id).first()
    if not blog:
        resp.status_code = 404
        return {"message": "Blog Not Found"} 
    return blog


# Blog Deletion
@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs'])
def delete_blog(id:int,db:Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id==id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with id {id} not found"
        )
    
    blog.delete(synchronize_session=False)
    db.commit()

    return 'done'

