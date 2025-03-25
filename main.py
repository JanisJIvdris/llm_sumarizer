import os
import json
from typing import Optional, Dict, Any
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import requests
import uvicorn
from dotenv import load_dotenv

load_dotenv(override=True)

app = FastAPI()

API_KEY: Optional[str] = os.getenv('HUGGINGFACE_API_KEY')
MODEL_ENDPOINT: str = os.getenv(
    'MODEL_ENDPOINT',
    'https://api-inference.huggingface.co/models/facebook/bart-large-cnn'
)
HOST: str = os.getenv('HOST', '0.0.0.0')
PORT: int = int(os.getenv('PORT', 8000))

if not API_KEY:
    raise RuntimeError("Missing API key configuration.")

#Exceptions

class InputValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class FileProcessingError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)

class LLMProcessingError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)

#Input Valdiation

def validate_input(content: str) -> None:
    if not content:
        raise InputValidationError("Input cannot be empty.")
    if len(content) > 5000:
        raise InputValidationError("Input exceeds the maximum allowed length.")

#API Call

def call_llm_api(text: str, task: Optional[str] = 'summarize') -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": text}
    try:
        response = requests.post(MODEL_ENDPOINT, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise LLMProcessingError("LLM API processing failed.")

#Endpoint

@app.post("/process")
async def process_data(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    task: Optional[str] = Form('summarize')
) -> JSONResponse:
    try:
        if file:
            try:
                content = await file.read()
                filename = file.filename.lower()

                if filename.endswith('.csv'):
                    text_input = content.decode('utf-8')
                elif filename.endswith('.json'):
                    try:
                        parsed = json.loads(content.decode('utf-8'))
                        text_input = parsed.get('text', '') if isinstance(parsed, dict) else ''
                    except json.JSONDecodeError:
                        raise FileProcessingError("Invalid JSON format.")
                else:
                    text_input = content.decode('utf-8')

            except UnicodeDecodeError:
                raise FileProcessingError("Unable to decode file content.")

        elif text:
            text_input = text
        else:
            raise InputValidationError("No input provided.")

        validate_input(text_input)
        result = call_llm_api(text_input, task)
        return JSONResponse(content={"result": result})

    except (InputValidationError, FileProcessingError, LLMProcessingError) as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)