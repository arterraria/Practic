from pathlib import Path
from uuid import uuid4

import cv2
import numpy as np
from fastapi import UploadFile

from app.core.config import RESULT_DIR, UPLOAD_DIR
from app.domain.bus_detector import BusDetector
from app.repositories.history_repository import HistoryRepository


class ProcessingService:

    def __init__(self, detector: BusDetector, repository: HistoryRepository) -> None:
        self.detector = detector
        self.repository = repository

    async def process_image(self, file: UploadFile) -> dict:
        content = await file.read()
        image_array = np.frombuffer(content, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Не удалось прочитать изображение. Загрузите JPG или PNG.")

        file_id = uuid4().hex
        source_name = f"{file_id}_source.jpg"
        result_name = f"{file_id}_result.jpg"

        source_path: Path = UPLOAD_DIR / source_name
        result_path: Path = RESULT_DIR / result_name

        cv2.imwrite(str(source_path), image)
        annotated, detections = self.detector.detect(image)
        cv2.imwrite(str(result_path), annotated)

        request_id = self.repository.add(
            source_file=f"/static/uploads/{source_name}",
            result_file=f"/static/results/{result_name}",
            bus_count=len(detections),
        )

        return {
            "id": request_id,
            "bus_count": len(detections),
            "result_url": f"/static/results/{result_name}",
            "detections": [d.__dict__ for d in detections],
        }
