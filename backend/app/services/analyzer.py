import ast
import os
import aiofiles
import asyncio

async def read_file_async(file_path: str) -> str:
    """Reads a file asynchronously."""
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
            return await file.read()
    except Exception as e:
        return f"# Error reading file {file_path}: {e}"

async def analyze_codebase_async(repo_path: str) -> str:
    """Asynchronously scans the repository and reads the content of code files."""
    file_paths = []
    
    # Traverse directory to find relevant files
    for root, dirs, files in os.walk(repo_path):
        # Ignore hidden/system folders and standard large environments
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('__pycache__', 'node_modules', 'venv', 'env')]
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.tsx', '.jsx', '.html', '.css', '.java', '.go')):
                file_paths.append(os.path.join(root, file))

    # Read all collected files concurrently
    contents = await asyncio.gather(*(read_file_async(fp) for fp in file_paths))
    
    code_summaries = []
    for fp, content in zip(file_paths, contents):
        # Truncate content to avoid exceeding context limits for large files
        code_summaries.append(f"--- File: {os.path.relpath(fp, repo_path)} ---\n{content[:3000]}\n")
        
    return "\n".join(code_summaries)

def count_source_files(repo_path: str) -> int:
    """Counts source files considered by the analyzer."""
    total = 0
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('__pycache__', 'node_modules', 'venv', 'env')]
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.tsx', '.jsx', '.html', '.css', '.java', '.go')):
                total += 1
    return total

def extract_functions(file_path: str):
    """
    Extracts function definitions from a given Python file using AST.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        node = ast.parse(file.read())
    
    functions = []
    for n in ast.walk(node):
        if isinstance(n, ast.FunctionDef):
            functions.append({
                "name": n.name,
                "docstring": ast.get_docstring(n)
            })
    return functions
