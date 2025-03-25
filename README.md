# LLM Summarization API

This is a simple FastAPI-based project that provides a text summarization API using a Hugging Face language model.

## Overview

The API allows users to submit either a text input or a file (`.txt`, `.csv`, or `.json`) and returns a summary of the content using a pre-trained LLM.

- Built with FastAPI
- Uses Hugging Face Inference API
- Accepts both raw text and file uploads
- Returns clean JSON-formatted output

## Solution

The task allowed for summarization. Originally, the task suggested using meta-llama/Llama-3.1-8B-Instruct, but that model requires a Pro subscription on Hugging Face. To ensure the project is fully testable without a paid account, I used the free and capable facebook/bart-large-cnn summarization model instead.

## Startup

1. Clone the repository
   ```
   git clone https://github.com/JanisJIvdris/llm_sumarizer
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv env
   env\Scripts\activate
   pip install -r requirements.txt
   ```
3. Create a .env file in the root(I will send you the key)

   ```
   HUGGINGFACE_API_KEY=your_token_here
   MODEL_ENDPOINT=https://api-inference.huggingface.co/models/facebook/bart-large-cnn
   HOST=0.0.0.0
   PORT=8000
   ```

4. Start the server

   ```
   python main.py
   ```

## Use

Send a POST request to:
` http://localhost:8000/process
`
With either A text field (form-data) or A file (.txt, .csv, or .json) field named file.

The functionality can be tested using:

- Postman
- Command line:
  (example)
  ```
  curl -X POST http://localhost:8000/process \
      -F "text=The Twilight Zone is a classic anthology series..." \
      -F "task=summarize"
  ```

## Response Example

```
{
  "result": [
    {
      "summary_text": "The Twilight Zone is a classic anthology series..."
    }
  ]
}
```
