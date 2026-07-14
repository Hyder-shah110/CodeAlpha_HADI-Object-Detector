"""
detector.py
-----------
YOLOv8 model ko load karta hai aur image par object detection
perform karta hai.
"""

import os
import cv2
from ultralytics import YOLO


# Model file ka path (is file ke folder ke andar models/yolov8n.pt)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "yolov8n.pt")


class ObjectDetector:

    def __init__(self, confidence_threshold: float = 0.35):
        """
        Parameters
        ----------
        confidence_threshold : float
            Kitne confidence se kam detections ko ignore karna hai.
            (0.35 matlab 35% se kam confident detections nahi dikhengi)
        """

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file nahi mili: {MODEL_PATH}\n"
                "Yaqeen karein ke 'yolov8n.pt' models/ folder ke andar hai."
            )

        self.model = YOLO(MODEL_PATH)
        self.confidence_threshold = confidence_threshold

    def detect_image(self, image):
        """
        Ek single image (ya ek video frame) par detection chalata hai.
        Isi function ko image upload, webcam snapshot aur video frames
        teeno ke liye use kiya jata hai.

        Parameters
        ----------
        image : numpy.ndarray
            RGB image array (jaise PIL se numpy mein convert ki gayi ho).

        Returns
        -------
        annotated_image : numpy.ndarray
            Boxes ke sath annotated image (RGB format mein, Streamlit ke liye).
        detections : list[dict]
            Har detected object ki details.
        """

        results = self.model(image, conf=self.confidence_threshold, verbose=False)

        # results[0].plot() OpenCV (BGR) format mein image return karta hai.
        # Streamlit ko RGB chahiye hoti hai, warna colors ulte dikhte hain.
        annotated_image_bgr = results[0].plot()
        annotated_image = cv2.cvtColor(annotated_image_bgr, cv2.COLOR_BGR2RGB)

        detections = []

        for index, box in enumerate(results[0].boxes, start=1):

            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]
            confidence = round(float(box.conf[0]) * 100, 2)

            x1, y1, x2, y2 = [round(float(v), 1) for v in box.xyxy[0]]

            detections.append({
                "No": index,
                "Object": class_name.title(),
                "Confidence (%)": confidence,
                "Box (x1, y1, x2, y2)": f"({x1}, {y1}, {x2}, {y2})",
            })

        return annotated_image, detections
