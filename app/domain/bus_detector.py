from dataclasses import dataclass
from typing import List, Tuple

import cv2
import numpy as np
from ultralytics import YOLO

from app.core.config import BUS_CLASS_ID, CONFIDENCE, MODEL_NAME


@dataclass
class Detection:
    x1: int
    y1: int
    x2: int
    y2: int
    confidence: float


class BusDetector:

    def __init__(self) -> None:
        self.model = YOLO(MODEL_NAME)

    def detect(self, image: np.ndarray) -> Tuple[np.ndarray, List[Detection]]:
        results = self.model.predict(
            image,
            classes=[BUS_CLASS_ID],
            conf=CONFIDENCE,
            verbose=False,
        )

        detections: List[Detection] = []
        annotated = image.copy()

        if not results or results[0].boxes is None:
            return annotated, detections

        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int).tolist()
            confidence = float(box.conf[0].cpu().numpy())
            detections.append(Detection(x1, y1, x2, y2, confidence))

            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 180, 0), 3)
            cv2.putText(
                annotated,
                f"bus {confidence:.2f}",
                (x1, max(y1 - 8, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 180, 0),
                2,
                cv2.LINE_AA,
            )

        cv2.putText(
            annotated,
            f"Detected buses: {len(detections)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            3,
            cv2.LINE_AA,
        )
        return annotated, detections
