from pydantic import BaseModel, Field


class UserLoginState(BaseModel):
    name:str = Field(description="User Name")
    email:str = Field(description="User Email")

class UserState(BaseModel):
    id: int
    name:str = Field(description="User Name")
    email:str = Field(description="User Email")


class ShowBlog(BaseModel):
    id: int
    title:str = Field(description="Blog Title")
    content:str = Field(description="Blog Content")
    user_id: int = Field(description="User ID")
    user: UserState


class BlogState(BaseModel):
    id: int
    title:str = Field(description="Blog Title")
    content:str = Field(description="Blog Content")
    user_id: int = Field(description="User ID")
    # creator: Users
    model_config = {
    "from_attributes": True  # New V2 style
    }
    # class Config:
    #     orm_mode = True
