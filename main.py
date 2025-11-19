from fastapi import FastAPI, Form, UploadFile, File
from src.services.ocr_service import extract_text_from_documents

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/extract-text")
async def extract_text(files: list[UploadFile] = File(...), query: str = Form(...)):
    """Extract text from uploaded documents. Supported formats: PDF, JPEG, JPG, PNG.

    Args:
        files (list[UploadFile]): The uploaded files.
    Returns:
        summary (str): Extracted text summary.

        extracted_text (dict[str, str]): Full extracted text.
    """
    accepted_formats = ["application/pdf", "image/jpeg", "image/jpg", "image/png"]
    
    for file in files:
        if file.content_type not in accepted_formats:
            return {"error": f"Unsupported file format: {file.content_type}. Accepted formats are PDF, JPEG, JPG, PNG."}
    
    extracted_texts = {}
    for file in files:
        content = await file.read()
        with open(file.filename, "wb") as f:
            f.write(content)
        extracted_text = extract_text_from_documents(document_path=file.filename)
        extracted_texts[file.filename] = extracted_text

    return {
        "summary": "",
        "extracted_text": extracted_texts,
        "data": {
            "files_processed": [file.filename for file in files],
            "query": query
        }
    }