import os
import tempfile
from io import BytesIO

import cv2
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

from core.panoptic_segmentator import PanopticSegmentator
from settings import Config  # type: ignore[attr-defined]


def settup_layout() -> None:
    st.set_page_config(page_title="Panoptic Segmentator", layout="wide")
    st.sidebar.write(
        """
        # Welcome to Panoptic Segmentator project
        """
    )
    st.sidebar.markdown("---")
    st.sidebar.write(
        """
        Here you can perform panoptic segmentation on your images and videos.
        For dipper understanding of the implementation, please visit [Github repository](https://github.com/kafkaGen/panoptic_segmentator).
        Also, there you can find FastAPI version of this project that provide bulk operations for images.
        """
    )
    st.sidebar.markdown("---")
    linkedin, telegram = st.sidebar.columns(2)
    linkedin.write("[LinkedIn](https://www.linkedin.com/in/kafkagen/)")
    telegram.write("[Telegram](https://t.me/boen_dia)")

    st.write("# Panoptic Segmentator")


def app() -> None:
    settup_layout()

    sbox_parts = st.columns(8)
    model_name = sbox_parts[0].selectbox("Choose model:", Config.model_checkpoints.keys())
    panoptic_segmentator = PanopticSegmentator(model_name)
    uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False)
    camera_live = st.button("Use Webcam")

    if camera_live:
        switch_page("live webcam")
    elif uploaded_file is not None:
        left_column, right_column = st.columns(2)
        if uploaded_file.type.split("/")[0] == "image":
            left_column.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

            input_image = np.array(Image.open(uploaded_file))
            segmented_image = panoptic_segmentator(input_image)[0]
            segmented_image = Image.fromarray(segmented_image)
            buf = BytesIO()
            segmented_image.save(buf, format=uploaded_file.type.split("/")[1].upper())
            segmented_file = buf.getvalue()

            right_column.image(segmented_image, caption="Segmented Image", use_column_width=True)
            left_column.download_button("Download segmentation", data=segmented_file, file_name=uploaded_file.name)

        elif uploaded_file.type.split("/")[0] == "video":
            left_column.video(uploaded_file)

            with st.spinner("Wait for it..."):
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(uploaded_file.read())
                vf = cv2.VideoCapture(tfile.name)
                fps = vf.get(cv2.CAP_PROP_FPS)
                width = int(vf.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(vf.get(cv2.CAP_PROP_FRAME_HEIGHT))

                frames = []
                while vf.isOpened():
                    ret, frame = vf.read()
                    if ret is False:
                        break
                    frames.append(frame)
                segmented_frames = panoptic_segmentator(frames)

                out = cv2.VideoWriter(Config.segmented_video_output, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
                for frame in segmented_frames:
                    frame = cv2.resize(frame, (width, height))
                    out.write(frame.astype(np.uint8))
                out.release()
            with open(Config.segmented_video_output, "rb") as video_file:
                video_bytes = video_file.read()
            os.system(f"ffmpeg -y -i {Config.segmented_video_output} -vcodec libx264 tmp.{Config.segmented_video_output.split('.')[-1]}")
            os.system(f"mv tmp.{Config.segmented_video_output.split('.')[-1]} {Config.segmented_video_output}")
            right_column.video(Config.segmented_video_output)
            left_column.download_button("Download segmentation", data=video_bytes, file_name=uploaded_file.name)

        else:
            st.error("File type not supported", icon="🚨")


if __name__ == "__main__":
    app()
