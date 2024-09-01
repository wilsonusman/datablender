from fastapi import FastAPI, UploadFile, File, HTTPException, Form, WebSocket
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
import os
import uuid
import tempfile
from datetime import datetime, timezone
import json
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create a directory for output files
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


class Job(BaseModel):
    id: str
    filename: str
    status: str
    timestamp: str
    files_combined: int  # New field for number of files combined


jobs = []


# Global dictionary to store WebSocket connections
websocket_connections: Dict[str, WebSocket] = {}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    websocket_connections[client_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    finally:
        del websocket_connections[client_id]


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), tab_name: str = Form(...), client_id: str = Form(...)):
    combined_df = None
    files_combined = 0
    total_files = len(files)

    async def send_progress(progress: int):
        if client_id in websocket_connections:
            await websocket_connections[client_id].send_json({"progress": progress})

    with tempfile.TemporaryDirectory() as temp_dir:
        for index, file in enumerate(files):
            temp_file_path = os.path.join(temp_dir, file.filename)
            content = await file.read()
            with open(temp_file_path, "wb") as f:
                f.write(content)
            
            try:
                df = pd.read_excel(temp_file_path, sheet_name=tab_name)
                # Add 'Source File' column with the filename
                df['Source File'] = file.filename
                if combined_df is None:
                    combined_df = df
                else:
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                files_combined += 1
            except Exception as e:
                print(f"Error processing {file.filename}: {str(e)}")
            
            progress = int((index + 1) / total_files * 100)
            await send_progress(progress)
            await asyncio.sleep(0.1)  # Small delay to allow other tasks to run

    if combined_df is None or files_combined == 0:
        raise HTTPException(status_code=400, detail="No valid files were processed")

    # Use ISO format for timestamp
    timestamp = datetime.now(timezone.utc).isoformat()
    filename = f"combined_data_{timestamp.replace(':', '-')}.csv"
    file_path = os.path.join(OUTPUT_DIR, filename)

    # Save the combined DataFrame to a CSV file
    combined_df.to_csv(file_path, index=False)

    # Save job information
    job_id = str(uuid.uuid4())
    job = {
        "id": job_id,
        "filename": filename,
        "timestamp": timestamp,
        "files_combined": files_combined
    }
    jobs = load_jobs()
    jobs.append(job)
    save_jobs(jobs)

    return JSONResponse(content={"message": "Files combined successfully", "job_id": job_id})

# Helper functions to load and save jobs
def load_jobs():
    try:
        with open("jobs.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_jobs(jobs):
    with open("jobs.json", "w") as f:
        json.dump(jobs, f)

@app.get("/jobs")
async def get_jobs():
    return load_jobs()


@app.get("/download/{job_id}")
async def download_file(job_id: str):
    jobs = load_jobs()
    job = next((job for job in jobs if job["id"] == job_id), None)
    if job:
        file_path = os.path.join(OUTPUT_DIR, job["filename"])
        if os.path.exists(file_path):
            return FileResponse(file_path, media_type="text/csv", filename=job["filename"])
    raise HTTPException(status_code=404, detail="File not found")


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/get_tabs")
async def get_tabs(files: List[UploadFile] = File(...)):
    all_tabs = set()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in files:
            temp_file_path = os.path.join(temp_dir, file.filename)
            content = await file.read()
            with open(temp_file_path, "wb") as f:
                f.write(content)
            
            try:
                xls = pd.ExcelFile(temp_file_path)
                all_tabs.update(xls.sheet_names)
            except Exception as e:
                print(f"Error reading {file.filename}: {str(e)}")
    
    return {"tabs": list(all_tabs)}
