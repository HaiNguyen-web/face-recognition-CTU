from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from deepface import DeepFace
from deepface.models.face_detection import RetinaFace 
from fastapi.staticfiles import StaticFiles
from typing import List
import os
from PIL import Image
from deepface import DeepFace
import io
import numpy as np
import cv2
from fastapi.responses import JSONResponse


app = FastAPI()
IMAGEDIR = "./db_data/"
templates = Jinja2Templates(directory="templates")
os.makedirs(IMAGEDIR, exist_ok=True)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/db_data", StaticFiles(directory="db_data"), name="db_data")

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    # List all folders in the db_data directory
    folders = [f for f in os.listdir(IMAGEDIR) if os.path.isdir(os.path.join(IMAGEDIR, f))]
    return templates.TemplateResponse("index.html", {"request": request, "folders": folders, "show": None})

@app.post("/create-folder")
async def create_folder(request: Request, folder_name: str = Form(...)):
    folder_path = os.path.join(IMAGEDIR, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    folders = [f for f in os.listdir(IMAGEDIR) if os.path.isdir(os.path.join(IMAGEDIR, f))]
    return templates.TemplateResponse("index.html", {"request": request, "folders": folders, "show": None, "message": f"Folder '{folder_name}' created."})

@app.post("/upload-files")
async def create_upload_files(request: Request, folder_name: str = Form(...), files: List[UploadFile] = File(...)):
    folder_path = os.path.join(IMAGEDIR, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    show = []

    for file in files:
        contents = await file.read()

        # Ensure unique file naming
        base_name, ext = os.path.splitext(file.filename)
        counter = 1
        new_filename = file.filename
        while os.path.exists(os.path.join(folder_path, new_filename)):
            new_filename = f"{base_name}-{counter}{ext}"
            counter += 1

        # Load the image using PIL
        img = Image.open(io.BytesIO(contents))

        # Resize image for faster processing while keeping aspect ratio
        max_dimension = 800
        img.thumbnail((max_dimension, max_dimension))
        img_array = np.array(img)

        # Detect faces using DeepFace (RetinaFace model)
        try:
            detections = DeepFace.extract_faces(img_path=img_array, detector_backend="retinaface")
            for face in detections:
                facial_area = face["facial_area"]
                x, y, w, h = map(int, [facial_area["x"], facial_area["y"], facial_area["w"], facial_area["h"]])

                # Crop the face
                face_cropped = img_array[y:y + h, x:x + w]

                # Keep aspect ratio when resizing cropped face
                target_size = (150, 150)  # Kích thước mục tiêu
                original_height, original_width, _ = face_cropped.shape

                # Tính toán tỉ lệ resize
                resize_ratio = min(target_size[0] / original_height, target_size[1] / original_width)
                new_height = int(original_height * resize_ratio)
                new_width = int(original_width * resize_ratio)

                # Resize ảnh với tỉ lệ giữ nguyên
                face_resized = cv2.resize(face_cropped, (new_width, new_height), interpolation=cv2.INTER_AREA)

                # Save the resized face as an image
                face_img_pil = Image.fromarray(face_resized)
                face_img_pil.save(os.path.join(folder_path, new_filename))

                show.append(new_filename)
                break  # Stop after the first detected face
            else:
                # Save the original if no face detected
                with open(os.path.join(folder_path, new_filename), "wb") as f:
                    f.write(contents)
                show.append(new_filename)
        except Exception as e:
            print("Face detection error:", e)
            # Handle or log errors if DeepFace detection fails
            with open(os.path.join(folder_path, new_filename), "wb") as f:
                f.write(contents)
            show.append(new_filename)

    # Get folder list for display
    folders = [f for f in os.listdir(IMAGEDIR) if os.path.isdir(os.path.join(IMAGEDIR, f))]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "folders": folders,
        "show": show,
        "message": f"Files uploaded to '{folder_name}' successfully.",
        "folder_name": folder_name  # Truyền folder_name vào template
    })