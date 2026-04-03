# import os
# import sys
# print(f"Current Directory: {os.getcwd()}")
# print(f"Python Search Path: {sys.path}")
from fastapi import FastAPI
import uvicorn
import database 
from routers import blogs, users, login


database.Base.metadata.create_all(bind=database.engine)


fastapp = FastAPI()

get_db = database.get_db

fastapp.include_router(blogs.router)
fastapp.include_router(users.router)
fastapp.include_router(login.router)

@fastapp.get("/")
def home():
    return {"message": "Welcome to the Blog Generation System!"}


 
if __name__ == "__main__":
    uvicorn.run("main:fastapp",port=9000,reload=True)