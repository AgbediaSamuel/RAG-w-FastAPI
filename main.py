from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, ValidationError
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
import uvicorn
from file_parser import FileParser, PDFParser

app = FastAPI()
load_dotenv()

class INPUT(BaseModel):
    input: str

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.get("/")
def read_root():
    return "Service is running"

@app.get("/greet/{name}")
def read_item(name: str):
    return {"message": name} 

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        location = os.path.join("uploads", file.filename)
        os.makedirs(os.path.dirname(location), exist_ok=True)

        with open(location, "wb") as current:
            current.write(await file.read()) 

        return {"info": "File saved", "filename": file.filename}

    except Exception as e:
        return {"message": f"Error Occurred: {str(e)}"}
    

@app.post("/ask/")
async def process_text():#input: INPUT): #fix this later
    if openai.api_key is None:
        return {"message": "OpenAI API Key is not set"}
    try:
        client = OpenAI()
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of the United States"}] #input.input}], #fix this later
    )
        return response.choices[0].message.content
    except Exception as e:
        return {"message": f"Error Occurred: {str(e)}"}
    
@app.get("/parsecheck")
def parse_check():
    parser = FileParser()
    return parser.parse("testfile.txt")

@app.get("/pdfparsecheck")
def pdf_parse_check():
    parser = PDFParser()
    return parser.parse("testfile.pdf")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)