from pydantic import BaseModel
from typing import List

class SearchResult(BaseModel):
    chunk: str
    doc_id: str

class SearchResponse(BaseModel):
    status: str
    query: str
    results: List[SearchResult]
