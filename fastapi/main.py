from fastapi import FastAPI, Depends, Response,status, HTTPException
import uvicorn
from states import BlogState, Users, ShowBlog
import database
from sqlalchemy.orm import Session
import model
from typing import List

database.Base.metadata.create_all(bind=database.engine)


fastapp = FastAPI()

def get_db():
    db = database.session()
    try:
        yield db
    finally:
        db.close()


@fastapp.get("/")
def home():
    return {"message": "Welcome to the Blog Generation System!"}

@fastapp.post("/blogcontent",tags=['Blogs'])
def create_blog(request:BlogState,db=Depends(get_db)):
    new_blog = model.Blog(id=request.id,title=request.title,content=request.content,user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

    # id = request.id
    # title = request.title
    # content = request.content
    # response = {
    #     "Blog ID": id,
    #     "Blog Title": title,
    #     "Blog Content": content
    # }
    return response

# Dependency Injection
@fastapp.get("/blogsretrieve",response_model=List[ShowBlog],tags=['Blogs'])
def retrieve_blogs(db=Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return blogs

# Status Code Handling
@fastapp.get("/retrieve/{id}",status_code=status.HTTP_200_OK,response_model=BlogState,tags=['Blogs'])
def retrieve(id:int,db:Session = Depends(get_db),resp:Response=None):
    blog = db.query(model.Blog).filter(model.Blog.id==id).first()
    if not blog:
        resp.status_code = 404
        return {"message": "Blog Not Found"} 
    return blog

# Blog Deletion
@fastapp.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs'])
def delete_blog(id:int,db:Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id==id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with id {id} not found"
        )
    
    blog.delete(synchronize_session=False)
    db.commit()

    return 'done'


# User Creation
@fastapp.post("/usercreate",tags=['Users'])
def user_create(request:Users,db:Session = Depends(get_db)):
    new_user = model.Users(**request.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# User Retrieval
@fastapp.get('/getuser',tags=['Users'])
def getuser(db:Session = Depends(get_db)):
    users = db.query(model.Users).all()
    return users

if __name__ == "__main__":
    uvicorn.run("main:fastapp",port=9000,reload=True)