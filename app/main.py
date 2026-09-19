from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as image_router
from app.api.report_routes import router as report_router
from app.core.config import STATIC_DIR, WEB_DIR

app = FastAPI(title="Bus Stop Counter")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(image_router)
app.include_router(report_router)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")
