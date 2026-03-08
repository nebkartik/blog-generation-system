import uvicorn
from fastapi import FastAPI,Request
import os
from dotenv import load_dotenv
from src.graphs.graphbuilder import GraphBuilder
from src.llms.groqllm import GroqLLM

load_dotenv()

app = FastAPI()

os.environ['LANGSMITH_API_KEY'] = os.getenv('LANGSMITH_API_KEY')

@app.post('/blogs')
async def blogs_generation(request:Request):
    data = await request.json()
    topic = data.get("topic","")
    language = data.get("language","")
    llm = GroqLLM().get_llm()
    graph = GraphBuilder(llm)
    if topic:
     graph = graph.set_graph_function(usecase="topic")
     state = graph.invoke({'topic':topic,
                           'current_language':language})
    
    return {'data':state}

if __name__=="__main__":
   uvicorn.run("app:app",host="0.0.0.0",port=8000,reload=True)