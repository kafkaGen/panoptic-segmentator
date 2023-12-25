import asyncio
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from core import PanopticSegmentator  # type: ignore[attr-defined]
from settings import Config  # type: ignore[attr-defined]
from utils import encode_image, postprocess_video, process_image, process_video  # type: ignore[attr-defined]

app = FastAPI()
SUPPORTED_MODELS = list(Config.model_checkpoints.keys())


@app.post("/images/")  # type: ignore[misc]
async def images_batch_processing(images: list[UploadFile] = File(...), model_name: Optional[str] = "fpn_r50") -> JSONResponse:
    if not images:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No images provided in the batch.",
        )

    if model_name not in SUPPORTED_MODELS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model {model_name} not found. Available models: {SUPPORTED_MODELS}",
        )

    images = await asyncio.gather(*[process_image(image) for image in images])
    segmented_images = PanopticSegmentator(model_name=model_name)(images)
    segmented_images_bytes = [encode_image(image) for image in segmented_images]

    return JSONResponse(content={"segmented_images_bytes": segmented_images_bytes})


@app.post("/videos/")  # type: ignore[misc]
async def video_batch_processing(videos: list[UploadFile] = File(...), model_name: Optional[str] = "fpn_r50") -> JSONResponse:
    if not videos:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No videos provided in the batch.",
        )

    if model_name not in SUPPORTED_MODELS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model {model_name} not found. Available models: {SUPPORTED_MODELS}",
        )

    videos_metadata = await asyncio.gather(*[process_video(video) for video in videos])
    segmented_videos_metadata = [(PanopticSegmentator(model_name=model_name)(frames), fps, w, h) for frames, fps, w, h in videos_metadata]
    segmented_videos_bytes = [postprocess_video(*metadata) for metadata in segmented_videos_metadata]

    return JSONResponse(content={"segmented_videos_bytes": segmented_videos_bytes})
