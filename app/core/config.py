from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"
RESULT_DIR = STATIC_DIR / "results"
WEB_DIR = BASE_DIR / "web"
DB_PATH = BASE_DIR / "history.db"
MODEL_NAME = "yolov8n.pt"
BUS_CLASS_ID = 5  # COCO class id: bus
CONFIDENCE = 0.35

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)
