import base64
import os
from io import BytesIO
from tempfile import NamedTemporaryFile

import cv2
import filetype
import numpy as np
from fastapi import HTTPException, UploadFile, status
from PIL import Image


async def process_image(image: UploadFile) -> np.array:
    if image.content_type not in ["image/png", "image/jpeg", "image/jpg"] or not filetype.is_image(image.file):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type received for {image.filename}",
        )
    image_bytes = await image.read()

    return np.array(Image.open(BytesIO(image_bytes)))


def encode_image(image: np.array) -> str:
    image = Image.fromarray(image.astype(np.uint8))
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")

    return base64.b64encode(image_bytes.getvalue()).decode("utf-8")


async def process_video(video: UploadFile) -> tuple[list[np.array], float, int, int]:
    if video.content_type != "video/mp4" and not filetype.is_video(video.file):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type received for {video.filename}",
        )

    video_content = await video.read()
    temp = NamedTemporaryFile(delete=False)
    with temp as f:
        f.write(video_content)
    video.file.close()

    cap = cv2.VideoCapture(temp.name)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()
    os.remove(temp.name)

    return frames, fps, width, height


def postprocess_video(frames: list[np.array], fps: float, width: int, height: int) -> str:
    temp_file = NamedTemporaryFile(suffix=".mp4", delete=False)
    temp_file_path = temp_file.name
    cap = cv2.VideoWriter(temp_file_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    for frame in frames:
        frame = cv2.resize(frame, (width, height))
        cap.write(frame.astype(np.uint8))
    cap.release()
    with open(temp_file_path, "rb") as f:
        f.seek(0)
        video_bytes = f.read()
    temp_file.close()
    os.remove(temp_file_path)

    return base64.b64encode(video_bytes).decode("utf-8")
