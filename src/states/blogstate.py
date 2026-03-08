from typing import TypedDict
from pydantic import BaseModel, Field

class Blog(BaseModel):
    title:str = Field(description="Blog Title")
    content:str = Field(description="Blog Content")

class BlogState(TypedDict):
    topic:str
    blog:Blog
    current_language:str
