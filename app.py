import io
import os
import tempfile
import time

import streamlit as st
import pandas as pd
import numpy as np
import cv2
from PIL import Image

from detector import ObjectDetector
from utils.image_info import get_image_information
from utils.summary import create_detection_summary


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="HADI Object Detector",
    layout="wide"
)


# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.title("HADI Object Detector")

st.sidebar.markdown("---")

st.sidebar.subheader("Detection Settings")

confidence_threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.1,
    max_value=0.9,
    value=0.35,
    step=0.05,
    help="Isse kam confidence wale objects ignore kar diye jayenge."
)

st.sidebar.markdown("---")

st.sidebar.subheader("Supported Formats")
st.sidebar.write("Image: JPG, JPEG, JFIF, PNG, BMP, WEBP, TIFF")
st.sidebar.write("Video: MP4, MOV, AVI, MKV")

st.sidebar.markdown("---")

st.sidebar.subheader("Model")
st.sidebar.write("YOLOv8 Nano (ultralytics)")

st.sidebar.markdown("---")

st.sidebar.subheader("About")
st.sidebar.write(
    "Object detection system for images, webcam snapshots and "
    "video files, built with YOLOv8 and Streamlit."
)


# -------------------------------------------------
# Main Heading
# -------------------------------------------------

st.title("HADI Object Detector")

st.write(
    "Upload an image, capture a photo from your webcam, or upload a video "
    "to detect real-world objects using the YOLOv8 deep learning model."
)

st.divider()


# -------------------------------------------------
# Load Model (cached so it only loads once per session)
# -------------------------------------------------

@st.cache_resource
def load_detector(threshold):
    return ObjectDetector(confidence_threshold=threshold)


try:
    detector = load_detector(confidence_threshold)
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()


# -------------------------------------------------
# Shared helper: renders the detection results block
# (metric, summary table, details table) for a given
# list of detections. Used by all three tabs so the
# output looks consistent everywhere.
# -------------------------------------------------

def render_detection_results(detections):

    total_objects = len(detections)

    st.metric(label="Total Objects Detected", value=total_objects)

    if total_objects == 0:
        st.warning(
            "No objects were detected. Try lowering the confidence "
            "threshold from the sidebar and run detection again."
        )
        return

    st.subheader("Detection Summary")

    summary = create_detection_summary(detections)
    summary_df = pd.DataFrame(summary.items(), columns=["Object", "Count"])
    st.table(summary_df)

    st.subheader("Detection Details")

    details_df = pd.DataFrame(detections)
    st.dataframe(details_df, width="stretch", hide_index=True)


# -------------------------------------------------
# Tabs: Image / Webcam / Video
# -------------------------------------------------

image_tab, webcam_tab, video_tab = st.tabs(["Image", "Webcam", "Video"])


# ==================================================
# TAB 1 — Image Upload
# ==================================================

with image_tab:

    uploaded_file = st.file_uploader(
        "Select an Image",
        type=["jpg", "jpeg", "jfif", "png", "bmp", "webp", "tiff"],
        key="image_uploader"
    )

    if uploaded_file is not None:

        try:
            image = Image.open(uploaded_file).convert("RGB")
        except Exception:
            st.error("This file is not a valid image. Please try another one.")
            st.stop()

        image_array = np.array(image)
        info = get_image_information(uploaded_file)

        left_col, right_col = st.columns(2)

        with left_col:
            st.subheader("Original Image")
            st.image(image, width="stretch")

            st.subheader("Image Information")
            info_df = pd.DataFrame(info.items(), columns=["Property", "Value"])
            st.table(info_df)

        with right_col:
            st.subheader("Detection Result")

            if st.button("Detect Objects", width="stretch", type="primary", key="image_detect_btn"):

                with st.spinner("Detecting objects..."):
                    result_image, detections = detector.detect_image(image_array)

                st.image(result_image, width="stretch")

                result_pil = Image.fromarray(result_image)
                buffer = io.BytesIO()
                result_pil.save(buffer, format="PNG")

                st.download_button(
                    label="Download Result Image",
                    data=buffer.getvalue(),
                    file_name=f"detected_{uploaded_file.name.rsplit('.', 1)[0]}.png",
                    mime="image/png",
                    width="stretch",
                )

                st.divider()
                render_detection_results(detections)

    else:
        st.info("Please upload an image to begin.")


# ==================================================
# TAB 2 — Webcam
# ==================================================

with webcam_tab:

    st.write(
        "Take a photo using your device camera. The browser will ask "
        "for camera permission the first time you use this."
    )

    camera_image = st.camera_input("Capture a photo", key="webcam_input")

    if camera_image is not None:

        image = Image.open(camera_image).convert("RGB")
        image_array = np.array(image)

        left_col, right_col = st.columns(2)

        with left_col:
            st.subheader("Captured Photo")
            st.image(image, width="stretch")

        with right_col:
            st.subheader("Detection Result")

            if st.button("Detect Objects", width="stretch", type="primary", key="webcam_detect_btn"):

                with st.spinner("Detecting objects..."):
                    result_image, detections = detector.detect_image(image_array)

                st.image(result_image, width="stretch")

                result_pil = Image.fromarray(result_image)
                buffer = io.BytesIO()
                result_pil.save(buffer, format="PNG")

                st.download_button(
                    label="Download Result Image",
                    data=buffer.getvalue(),
                    file_name="webcam_detection.png",
                    mime="image/png",
                    width="stretch",
                )

                st.divider()
                render_detection_results(detections)

    else:
        st.info("Click the camera button above to capture a photo.")


# ==================================================
# TAB 3 — Video Upload
# ==================================================

with video_tab:

    st.write(
        "Upload a video file. Every frame will be passed through the "
        "model and an annotated copy of the video will be generated."
    )

    frame_skip = st.slider(
        "Process every Nth frame (higher = faster, lower quality tracking)",
        min_value=1,
        max_value=10,
        value=2,
        help=(
            "Detection is only run on every Nth frame to keep processing "
            "time reasonable. Skipped frames reuse the last detected boxes."
        ),
        key="frame_skip_slider"
    )

    uploaded_video = st.file_uploader(
        "Select a Video",
        type=["mp4", "mov", "avi", "mkv"],
        key="video_uploader"
    )

    if uploaded_video is not None:

        st.video(uploaded_video)

        if st.button("Detect Objects in Video", width="stretch", type="primary", key="video_detect_btn"):

            # Uploaded video is saved to a temp file because OpenCV needs
            # a real file path, it cannot read directly from the upload buffer.
            input_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            with open(input_path, "wb") as f:
                f.write(uploaded_video.read())

            capture = cv2.VideoCapture(input_path)

            fps = capture.get(cv2.CAP_PROP_FPS) or 25
            width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            progress_bar = st.progress(0)
            status_text = st.empty()

            all_detections = []
            last_annotated_bgr = None
            frame_index = 0
            start_time = time.time()

            while True:
                success, frame_bgr = capture.read()
                if not success:
                    break

                if frame_index % frame_skip == 0:
                    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                    annotated_rgb, detections = detector.detect_image(frame_rgb)
                    last_annotated_bgr = cv2.cvtColor(annotated_rgb, cv2.COLOR_RGB2BGR)
                    all_detections.extend(detections)

                # If this frame was skipped, reuse the last annotated frame
                # so the output video still has one frame per input frame.
                writer.write(last_annotated_bgr if last_annotated_bgr is not None else frame_bgr)

                frame_index += 1

                if total_frames > 0:
                    progress_bar.progress(min(frame_index / total_frames, 1.0))
                status_text.text(f"Processing frame {frame_index} of {total_frames}")

            capture.release()
            writer.release()

            elapsed = round(time.time() - start_time, 1)
            status_text.text(f"Done. Processed {frame_index} frames in {elapsed} seconds.")

            st.subheader("Detection Result")

            with open(output_path, "rb") as f:
                result_video_bytes = f.read()

            st.video(result_video_bytes)

            st.download_button(
                label="Download Result Video",
                data=result_video_bytes,
                file_name=f"detected_{uploaded_video.name.rsplit('.', 1)[0]}.mp4",
                mime="video/mp4",
                width="stretch",
            )

            st.divider()
            render_detection_results(all_detections)

            # Clean up temp files
            os.remove(input_path)
            os.remove(output_path)

    else:
        st.info("Please upload a video to begin.")
