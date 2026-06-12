from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .scraper import search_linkedin_public_profiles

app = FastAPI()

# Serve frontend static files from ../frontend
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')
app.mount('/static', StaticFiles(directory=frontend_dir), name='static')


class SearchRequest(BaseModel):
    query: str
    limit: int = 5


@app.post('/search')
def search(req: SearchRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail='query required')
    results = search_linkedin_public_profiles(req.query, limit=req.limit)
    return {'count': len(results), 'results': results}


@app.get('/')
def index():
    index_path = os.path.join(frontend_dir, 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail='frontend not found')
