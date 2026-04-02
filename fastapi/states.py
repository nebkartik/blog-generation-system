from pydantic import BaseModel, Field


class Users(BaseModel):
    id: int
    name:str = Field(description="User Name")
    email:str = Field(description="User Email")


class ShowBlog(BaseModel):
    id: int
    title:str = Field(description="Blog Title")
    content:str = Field(description="Blog Content")
    user_id: int = Field(description="User ID")
    user: Users


class BlogState(BaseModel):
    id: int
    title:str = Field(description="Blog Title")
    content:str = Field(description="Blog Content")
    user_id: int = Field(description="User ID")
    # creator: Users
    
    class Config:
        orm_mode = True
