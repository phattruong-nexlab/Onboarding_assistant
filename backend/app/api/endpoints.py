import os
import logging
import tempfile
import uuid
import zipfile
import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.models.schemas import ScanReport, UpdateReadmeRequest, UpdateReadmeResponse
from app.services.analyzer import analyze_codebase_async, count_source_files
from app.services.gemini_client import update_readme_async

router = APIRouter()
logger = logging.getLogger(__name__)
UPLOAD_ROOT_DIR = os.path.join(tempfile.gettempdir(), "onboarding_assistant_uploads")


def _resolve_repo_root(extracted_base_path: str) -> str:
    entries = [
        name
        for name in os.listdir(extracted_base_path)
        if name != "__MACOSX"
    ]
    if len(entries) == 1:
        single_entry_path = os.path.join(extracted_base_path, entries[0])
        if os.path.isdir(single_entry_path):
            return single_entry_path
    return extracted_base_path


def _extract_zip_safely(zip_path: str, destination_dir: str) -> None:
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for member in zip_ref.infolist():
            normalized_path = os.path.normpath(member.filename)
            if os.path.isabs(normalized_path) or normalized_path.startswith(".."):
                raise HTTPException(status_code=400, detail="Invalid zip content.")
        zip_ref.extractall(destination_dir)

@router.post("/scan", response_model=ScanReport)
async def scan_repository(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are supported.")

    os.makedirs(UPLOAD_ROOT_DIR, exist_ok=True)
    scan_id = str(uuid.uuid4())
    scan_workspace_path = os.path.join(UPLOAD_ROOT_DIR, scan_id)
    zip_path = os.path.join(scan_workspace_path, "repository.zip")
    extracted_path = os.path.join(scan_workspace_path, "repo")

    try:
        os.makedirs(extracted_path, exist_ok=True)
        async with aiofiles.open(zip_path, "wb") as output_file:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                await output_file.write(chunk)

        _extract_zip_safely(zip_path, extracted_path)
        repo_path = _resolve_repo_root(extracted_path)
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid zip file.")
    except HTTPException:
        raise
    except Exception:
        logger.exception("Failed to receive or extract uploaded zip.")
        raise HTTPException(status_code=500, detail="Failed to process uploaded zip file.")
    finally:
        await file.close()

    readme_path = os.path.join(repo_path, "README.md")

    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        raise HTTPException(status_code=400, detail="Invalid repository path.")

    current_readme = ""
    if os.path.exists(readme_path):
        try:
            async with aiofiles.open(readme_path, "r", encoding="utf-8") as f:
                current_readme = await f.read()
        except Exception:
            logger.exception("Failed to read README at path %s", readme_path)
            raise HTTPException(status_code=500, detail="Failed to read README file.")

    codebase_summary = await analyze_codebase_async(repo_path)
    total_files = count_source_files(repo_path)

    if not codebase_summary.strip():
        raise HTTPException(status_code=400, detail="No source code files found in the specified path.")

    try:
        generated_readme = await update_readme_async(codebase_summary, current_readme)
    except Exception:
        logger.exception("Failed to generate README from code summary.")
        raise HTTPException(status_code=500, detail="Failed to generate README.")

    details = []
    if not os.path.exists(readme_path):
        details.append("README.md does not exist yet and will be created on update.")
    else:
        details.append("README.md exists and has been used as base format/context.")
    details.append(f"Scanned source files: {total_files}")
    details.append(f"Uploaded archive: {file.filename}")

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
    except Exception:
        logger.exception("Failed to write README at path %s", readme_path)
        raise HTTPException(status_code=500, detail="Failed to update README file.")

    return UpdateReadmeResponse(
        status="success",
        message="README.md updated successfully.",
        readme_path=readme_path,
        bytes_written=len(generated_readme.encode("utf-8")),
    )
