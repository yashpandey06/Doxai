from fastapi import FastAPI, File, UploadFile
from PyPDF2 import PdfReader
import requests
import tempfile
import os

app = FastAPI()
API_TOKEN=os.environ.get('API_TOKEN')
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.get("/")
def read_root():
    return {"message": "Hello, Homei !!"}

@app.post("/summarise-pdf")
async def read_summarise_pdf(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
            temp_pdf.write(await file.read())
            temp_pdf_name = temp_pdf.name

        try:
            with open(temp_pdf_name, "rb") as pdf_file:
                reader = PdfReader(pdf_file)
                
                number_of_pages = len(reader.pages)
                if number_of_pages > 3:
                    return {"error": "Number of pages are more than 3."}
                
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                output = query({"inputs": text})
                print(output)
                return output
        finally:
            
            os.unlink(temp_pdf_name)
    else:
        return {"error": "Uploaded file is not a PDF."}
