from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
# from newsapi import NewsApiClient
import os
import requests as rq


app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. You can replace "*" with a specific domain if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods. You can restrict to specific methods if needed.
    allow_headers=["*"],  # Allows all headers. You can restrict to specific headers if needed.
)

api_key = os.getenv("NEWS_API")

@app.post("/fetch")
async def fetch(req: Request):
    category = await req.body()
    category = category.decode("utf-8")
    
    url="https://newsapi.org/v2/everything?q="+category+"&apiKey="+api_key
    
    if category=="headlines":
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey="+api_key
    else:
        url = "https://newsapi.org/v2/everything?q="+category+"&apiKey="+api_key
        
    try:
        response = rq.get(url)
        r=response.json()
        return r
    
    except Exception as e:
        response = {"error":e}
        return response



# Testing / Ping to up the API access...
@app.get("/test")
def hello():
    try:
        return {"Success":"API is live."}
    except Exception as e:
        return {"Failed":str(e)}
