# import os
# import sys
# print(f"Current Directory: {os.getcwd()}")
# print(f"Python Search Path: {sys.path}")
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import uvicorn
import database 
from routers import blogs, users, login
from pydantic import BaseModel
from collections.abc import AsyncIterable
import json

database.Base.metadata.create_all(bind=database.engine)


fastapp = FastAPI()

get_db = database.get_db

fastapp.include_router(blogs.router)
fastapp.include_router(users.router)
fastapp.include_router(login.router)

@fastapp.get("/")
def home():
    return {"message": "Welcome to the Blog Generation System!"}



class Item(BaseModel):
    name: str
    description: str | None


items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]



# Streaming endpoint that yields items one by one
@fastapp.get("/items/stream")
async def stream_items() -> AsyncIterable[Item] :
    async def item_generator():
        for item in items:
           # 1. Convert to JSON string
            json_data = json.dumps(item.model_dump()) 
            # 2. Yield the chunk + a newline
            yield f"{json_data}\n"
            # 3. FORCE a pause so the buffer clears
            await asyncio.sleep(1)

    return StreamingResponse(item_generator(), media_type="application/x-ndjson")
 
if __name__ == "__main__":
    uvicorn.run("main:fastapp",port=9000,reload=True)