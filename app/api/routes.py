from fastapi import APIRouter, File, HTTPException, UploadFile

from app.domain.bus_detector import BusDetector
from app.repositories.history_repository import HistoryRepository
from app.services.processing_service import ProcessingService

router = APIRouter(prefix="/api")

repository = HistoryRepository()
detector = BusDetector()
service = ProcessingService(detector=detector, repository=repository)


@router.post("/process")
async def process(file: UploadFile = File(...)) -> dict:
    try:
        return await service.process_image(file)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/history")
def history() -> dict:
    return {"items": repository.list_last(limit=20)}
