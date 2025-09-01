from pydantic import BaseModel
from typing import Optional, List


class ProjectInput(BaseModel):
    company_name: str
    project_name: str
    project_scope: str       # 2-line description
    tools: str               # comma-separated list or sentence
    duration: str
    deliverables: str


class RetrieveResponse(BaseModel):
    session_id: str
    chunks: List[str]


class DraftResponse(BaseModel):
    session_id: str
    draft: str
