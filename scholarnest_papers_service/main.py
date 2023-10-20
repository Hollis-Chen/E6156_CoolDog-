from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import uvicorn

app = FastAPI()

# Load the papers data
with open("data.json", "r") as file:
    papers = [json.loads(line) for line in file if line.strip()]

class Paper(BaseModel):
    paper_id: str
    title: str
    authors: List[dict]
    year: int
    journal: Optional[str]
    s2_url: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Paper Search Microservice"}

@app.get("/papers/{paper_id}", response_model=Paper)
def get_paper_by_id(paper_id: str):
    paper = next((p for p in papers if p['paper_id'] == paper_id), None)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@app.get("/papers/search/{keyword}", response_model=List[Paper])
def search_papers_by_keyword(keyword: str):
    matching_papers = [p for p in papers if keyword.lower() in p['title'].lower()]
    return matching_papers

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012)
