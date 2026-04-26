import google.generativeai as genai
from app.core.config import settings

# Initialize Gemini Client
genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_doc_for_code(code: str) -> str:
    """
    Calls Gemini API to generate documentation for the provided code snippet.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"Act as a Senior Technical Writer. Analyze the following Python code and generate standard markdown documentation for it. Include purpose, arguments, return types, and usage examples.\n\n{code}"
    response = model.generate_content(prompt)
    return response.text
async def update_readme_async(codebase_summary: str, current_readme: str) -> str:
    """
    Calls Gemini API to generate an updated README.md file asynchronously based on the codebase.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"""
    Act as an experienced Senior Software Engineer and Technical Writer.
    Your task is to update the current README.md of the project based on the actual codebase files.
    Ensure standard formatting, clean architecture diagrams (if applicable), endpoint docs, and environment instructions are accurate.
    
    Current README.md Content:
    {current_readme}
    
    Codebase Summary:
    {codebase_summary}
    
    Output strictly the final Markdown content that will be saved into README.md without any extra conversational text.
    """
    response = await model.generate_content_async(prompt)
    new_doc = response.text
    if new_doc.startswith("```markdown"):
        new_doc = new_doc[11:]
    if new_doc.endswith("```"):
        new_doc = new_doc[:-3]
    return new_doc.strip()
