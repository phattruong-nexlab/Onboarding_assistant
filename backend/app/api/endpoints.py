import os
import aiofiles
from fastapi import APIRouter, HTTPException
from app.models.schemas import ScanRequest, ScanReport, UpdateReadmeRequest, UpdateReadmeResponse
from app.services.analyzer import analyze_codebase_async, count_source_files
from app.services.gemini_client import update_readme_async

router = APIRouter()

@router.post("/scan", response_model=ScanReport)
async def scan_repository(request: ScanRequest):
    repo_path = request.repo_path
    readme_path = os.path.join(repo_path, "README.md")

    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        raise HTTPException(status_code=400, detail="Invalid repository path.")

    current_readme = ""
    if os.path.exists(readme_path):
        try:
            async with aiofiles.open(readme_path, "r", encoding="utf-8") as f:
                current_readme = await f.read()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read README: {str(e)}")

    codebase_summary = await analyze_codebase_async(repo_path)
    total_files = count_source_files(repo_path)

    if not codebase_summary.strip():
        raise HTTPException(status_code=400, detail="No source code files found in the specified path.")

    try:
        generated_readme = await update_readme_async(codebase_summary, current_readme)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate README via Gemini: {str(e)}")

    details = []
    if not os.path.exists(readme_path):
        details.append("README.md does not exist yet and will be created on update.")
    else:
        details.append("README.md exists and has been used as base format/context.")
    details.append(f"Scanned source files: {total_files}")

    return ScanReport(
        repo_path=repo_path,
        readme_path=readme_path,
        total_files=total_files,
        current_readme=current_readme,
        generated_readme=generated_readme,
        details=details,
    )

@router.post("/update_readme", response_model=UpdateReadmeResponse)
async def api_update_readme(request: UpdateReadmeRequest):
    repo_path = request.repo_path
    generated_readme = request.generated_readme
    readme_path = os.path.join(repo_path, "README.md")
    
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        raise HTTPException(status_code=400, detail="Invalid repository path.")

    if not generated_readme.strip():
        raise HTTPException(status_code=400, detail="generated_readme cannot be empty.")

    try:
        async with aiofiles.open(readme_path, "w", encoding="utf-8") as f:
            await f.write(generated_readme)
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Failed to write new README: {str(e)}")

    return UpdateReadmeResponse(
        status="success",
        message="README.md updated successfully.",
        readme_path=readme_path,
        bytes_written=len(generated_readme.encode("utf-8")),
    )
