from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.ftk.utils import BaseRepository, Repository
from src.config.database_helper import database_helper
from src.ftk.models import FTK
from src.ftk.service import FTKParserService
from parsers.requestor import GetRequestor
from parsers.http_client import HTTPClientAioHttp
from parsers.parser import BeautifulSoupHTMLParser
from parsers.ftk import FTKParser


def get_ftk_repository(session: AsyncSession = Depends(database_helper.session_depends)) -> Repository:
    return BaseRepository(FTK, session)

async def get_result_ftk_parser_service(
        repo: Repository
) -> FTKParserService:
    async with HTTPClientAioHttp() as client:
        get_requestor = GetRequestor(client)
        parser = BeautifulSoupHTMLParser("https://www.f-tk.ru", get_requestor)
        ftk = FTKParser(get_requestor, parser)
        service = FTKParserService(ftk, repo)
        return await service.parsing()