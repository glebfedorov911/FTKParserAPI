from parsers.ftk import FTKParser
from src.ftk.utils import Repository


class FTKParserService:


    def __init__(
            self,
            ftk_parser: FTKParser,
            repo: Repository
    ):
        self.ftk_parser = ftk_parser
        self.repo = repo

    async def parsing(self):
        actually_show_data = await self.repo.get_all(actually=True)
        for data in actually_show_data:
            await self.repo.update(data.id, actually=False)

        results = await self.ftk_parser.parse_data()
        for category in results:
            for product in results[category]:
                await self.repo.create(
                    product_name=product["title"],
                    category=category,
                    url_to_product=product["url"],
                    icons=product["signs"],
                    characteristics=product["characteristics"]
                )
        actually_show_data = await self.repo.get_all(actually=True)       
        return {
            "data": actually_show_data,
            "count": len(actually_show_data)
        }