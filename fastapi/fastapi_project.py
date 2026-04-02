from fastapi import FastAPI, Request, Body
import uvicorn
from pydantic import BaseModel, Field
import json

app = FastAPI()

class Blog(BaseModel):
    title:str = Field(description="Blog Title")
    content:str = Field(description="Blog Content")


@app.post("/blog")
def create_blog(request:Blog):
    title = request.title
    content = request.content
    response = {
        "Blog Title": title,
        "Blog Content": content
    }
    return response


@app.get("/")
async def root():
    return {'message': "This is the app."}


@app.get("/index/{id}")
def index(id: int,limit: int):
    return {
        'index':{'id': id,
                 'Limit': limit
        }
    }


if __name__ == "__main__":
    uvicorn.run("fastapi_project:app",port=8001,reload=True)