from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import FileResponse
from openpyxl import Workbook

from app.repositories.history_repository import HistoryRepository

router = APIRouter(prefix="/api")
repository = HistoryRepository()


@router.get("/export/xlsx")
def export_xlsx() -> FileResponse:
    items = repository.list_last(limit=1000)

    wb = Workbook()
    ws = wb.active
    ws.title = "Bus counter history"
    ws.append(["ID", "Дата обработки", "Исходный файл", "Результат", "Количество автобусов"])

    for item in reversed(items):
        ws.append([
            item["id"],
            item["created_at"],
            item["source_file"],
            item["result_file"],
            item["bus_count"],
        ])

    file_name = f"bus_counter_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    file_path = f"reports/{file_name}"
    wb.save(file_path)

    return FileResponse(
        file_path,
        filename=file_name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
