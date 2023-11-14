from io import BytesIO

import numpy as np
import streamlit as st
from PIL import Image

from core.watermark_remover import WatermarkRemover

if __name__ == "__main__":
    watermark_remover = WatermarkRemover()

    st.set_page_config(layout="wide")
    st.sidebar.write(
        """
        # Welcome to Watermark Remover project
        """
    )
    st.sidebar.markdown("---")
    st.sidebar.write(
        """
        Here you can remove watermark of any types from your images and videos.
        For dipper understanding of the cleaning algorithm, please visit [Github repository](https://github.com/kafkaGen/watermark_remover).
        Also, there you can find FastAPI version of this project that provide bulk operations for images.
        """
    )
    st.sidebar.markdown("---")
    st.write(
        """
            # Watermark Remover
            Enter image or video file to remove watermark
            """
    )
    LinkedIn, Telegram = st.sidebar.columns(2)
    LinkedIn.write("[LinkedIn](https://www.linkedin.com/in/kafkagen/)")
    Telegram.write("[Telegram](https://t.me/boen_dia)")

    uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False)
    left_column, right_column = st.columns(2)

    if uploaded_file is not None:
        if uploaded_file.type.split("/")[0] == "image":
            left_column.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

            input_image = np.array(Image.open(uploaded_file))
            clean_image = watermark_remover(input_image)
            clean_image = Image.fromarray(clean_image)
            buf = BytesIO()
            clean_image.save(buf, format=uploaded_file.type.split("/")[1].upper())
            clean_file = buf.getvalue()

            right_column.image(clean_image, caption="Cleaned Image", use_column_width=True)
            left_column.download_button("Download clean file", data=clean_file, file_name=uploaded_file.name)

        elif uploaded_file.type.split("/")[0] == "video":
            # TODO add video support
            pass
        else:
            st.error("File type not supported", icon="🚨")
