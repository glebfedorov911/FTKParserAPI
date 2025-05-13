from fastapi import APIRouter, Depends, BackgroundTasks

from src.config.settings import settings
from src.ftk.dependencies import get_result_ftk_parser_service, get_ftk_repository
from src.ftk.service import FTKParserService
from src.ftk.utils import Repository


router = APIRouter(prefix=settings.url.prefix_ftk, tags=[settings.url.tag_ftk])

@router.get("/start_parser")
async def start_parser(
    background_tasks: BackgroundTasks,
    repo: Repository = Depends(get_ftk_repository)
):
    background_tasks.add_task(get_result_ftk_parser_service, repo)
    return {"message": "success starting"}

@router.get("/get_all")
async def get_all_data_from_parsing(
    repo: Repository = Depends(get_ftk_repository)
):
    data_to_show = await repo.get_all(actually=True)
    return {
        "count": len(data_to_show),
        "data": data_to_show
    }