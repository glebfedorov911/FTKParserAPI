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
                try:
                    await self.repo.create(
                        product_name=self._replace_spec(product["title"]),
                        category=self._replace_spec(category),
                        url_to_product=product["url"],
                        icons=self._replace_spec(product["signs"]),
                        characteristics=self._replace_spec(product["characteristics"])
                    )
                except Exception as e:
                    print(e)
        actually_show_data = await self.repo.get_all(actually=True)       
        return {
            "data": actually_show_data,
            "count": len(actually_show_data)
        }

    @staticmethod
    def _replace_spec(field):
        return (field.strip()
                .replace("\t", " ")
                .replace("\n", " ")
                .replace(":", " ")
                .replace("\\", " ")
                .replace(",", " ")
                .replace(";", " ")
                .replace(".", " ")
                .replace("-", " ")
                .replace("_", " ")
                )