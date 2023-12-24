# Panoptic Segmentator

<div id="header" align="center">
  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/>
</div>

## Introduction

<div id="header" align="center">
  <img src="demo.gif"/>
</div>

Welcome to PanopticSegmentator, a cutting-edge web application that empowers users to perform panoptic segmentation on images, videos, and even live webcam feeds. Panoptic segmentation goes beyond traditional semantic segmentation by not only classifying objects in an image but also distinguishing between stuff (e.g., background) and things (e.g., objects).

## Installation and Usage

To run the web application, you have two options:

### Option 1: Local Installation with Conda

1. Install necessary dependencies:
    ```bash
    apt-get install ffmpeg libsm6 libxext6 ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx
    ```

2. Clone the repository:
    ```bash
    git clone https://github.com/kafkaGen/panoptic-segmentator
    ```

3. Create and activate a Conda environment:
    ```bash
    conda env create -n <env_name> --file requirements.yaml
    conda activate <env_name>
    ```

4. Install Python requirements:
    ```bash
    pip install -r requirements.txt
    pip install -U openmim
    ```

5. Install additional packages:
    ```bash
    mim install mmengine "mmcv>=2.0.0" mmdet git+https://github.com/cocodataset/panopticapi.git
    ```

6. Download required models:
    ```bash
    python setup.py --download-models
    ```

7. Run the application using Streamlit and FastAPI:
    ```bash
    uvicorn core.api:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port 8501
    ```

### Option 2: Docker Installation

1. Build the Docker image locally:
    ```bash
    docker build -t panoptic-segmentator:latest .
    ```

    Or pull the Docker image from Docker Hub:
    ```bash
    docker pull olko123123123/panoptic-segmentator:latest && docker tag olko123123123/panoptic-segmentator:latest panoptic-segmentator:latest
    ```

2. Run the Docker container using the provided script:
    ```bash
    bash container-run.sh
    ```

    > **NOTE:** `container-run.sh` automatically determines whether your machine supports NVIDIA GPU and runs the Docker container accordingly on CPU or GPU.

### Access the Application Online

Alternatively, you can try the application online [here](http://54.242.166.254). Please note that this is an AWS EC2 free-tier instance, so be patient with its performance.

## REST API for batch inference
While the web application provides an intuitive interface for individual use, it may not be the most efficient solution for large-scale content processing. For such scenarios, the REST API implementation supports batch inference for both images and videos. Below are examples demonstrating how to make API calls for image and video batch inference.

### Image Batch Inference
To perform image batch inference, use the following Python code:

```python
import base64
import os
from io import BytesIO

import numpy as np
import requests
from PIL import Image

url = "<host>/images/?model_name=<model-name>"

file_list, open_files = [], []
for path in os.listdir(path_to_imgs):
    file_path = os.path.join(path_to_imgs, path)
    open_file = open(file_path, "rb")
    if ".jpg" in file_path:
        file_list.append(("images", (path, open_file, "image/jpeg")))
    else:
        file_list.append(("images", (path, open_file, "image/png")))
    open_files.append(open_file)

response = requests.post(url, files=file_list)
for fl in open_files:
    fl.close()
imgs = response.json()["segmented_images_bytes"]
imgs = [np.array(Image.open(BytesIO(base64.b64decode(img)))) for img in imgs]
```
### Video Batch Inference
For video batch inference, utilize the following Python code:
```python
import base64
import os
import tempfile

import cv2
import requests


url = "<host>/videos/?model_name=<model-name>"

file_list, open_files = [], []
for path in os.listdir(path_to_videos):
    file_path = os.path.join(path_to_videos, path)
    open_file = open(file_path, "rb")
    if ".mp4" in file_path:
        file_list.append(("videos", (path, open_file, "video/mp4")))
    open_files.append(open_file)


response = requests.post(url, files=file_list)
for fl in open_files:
    fl.close()
videos_encoded = response.json()["segmented_videos_bytes"]
for video in videos_encoded:
    video_decoded = base64.b64decode(video)

    temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    temp_file.write(video_decoded)
    temp_file_path = temp_file.name

    cap = cv2.VideoCapture(temp_file_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("Video", frame)
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    temp_file.close()
    os.remove(temp_file_path)
```
Feel free to adapt these examples to suit your specific use case and integrate them seamlessly into your workflow for efficient batch processing.

### todo
- test and push image to docker hub
- test job to ci/cd, pre-commit