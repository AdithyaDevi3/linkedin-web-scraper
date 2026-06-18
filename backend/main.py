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
    # `query` kept for backwards-compatibility. `prompt` can be used instead
    # If both provided, `prompt` takes precedence.
    query: str = ''
    prompt: str = ''
    limit: int = 5


@app.post('/search')
def search(req: SearchRequest):
    # Determine effective query: prefer prompt, then query
    effective = (req.prompt or req.query or '').strip()
    if not effective:
        raise HTTPException(status_code=400, detail='query or prompt required')
    results = search_linkedin_public_profiles(effective, limit=req.limit)
    return {'count': len(results), 'results': results}


@app.get('/')
def index():
    index_path = os.path.join(frontend_dir, 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail='frontend not found')
