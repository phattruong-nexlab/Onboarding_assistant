from pydantic import BaseModel
from typing import List

class ScanRequest(BaseModel):
    repo_path: str

class ScanReport(BaseModel):
    repo_path: str
    readme_path: str
    total_files: int
    current_readme: str
    generated_readme: str
    details: List[str]

class UpdateReadmeRequest(BaseModel):
    repo_path: str
    generated_readme: str

class UpdateReadmeResponse(BaseModel):
    status: str
    message: str
    readme_path: str
    bytes_written: int

class GenerateDocRequest(BaseModel):
    file_path: str
