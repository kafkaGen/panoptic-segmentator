import cv2
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from core.panoptic_segmentator import PanopticSegmentator


def live_webcanm() -> None:
    panotpic_segmentator = PanopticSegmentator()

    st.set_page_config(page_title="Panoptic Segmentator - Live", layout="wide")
    st.write("# Live Webcam Panoptic Segmentation ")
    st.warning("If you cannot see the video, please refresh the page.", icon="⚠️")
    back2app = st.button("Back")

    if back2app:
        switch_page("streamlit app")

    cap = cv2.VideoCapture(0)
    left_column, right_column = st.columns(2)
    left_frame_placeholder = left_column.empty()
    right_frame_placeholder = right_column.empty()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("Video Capture Ended")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        segmented_frame = panotpic_segmentator(frame)[0]
        left_frame_placeholder.image(frame, channels="RGB")
        right_frame_placeholder.image(segmented_frame, channels="RGB")
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


live_webcanm()
