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
                        product_name=self._replace_all_spec_symbols_in_parsed_data(product["title"]),
                        category=self._replace_all_spec_symbols_in_parsed_data(category),
                        url_to_product=product["url"],
                        icons=self._replace_all_spec_symbols_in_parsed_data(product["signs"]),
                        characteristics=self._replace_all_spec_symbols_in_parsed_data(product["characteristics"])
                    )
                except Exception as e:
                    print(e)
        actually_show_data = await self.repo.get_all(actually=True)       
        return {
            "data": actually_show_data,
            "count": len(actually_show_data)
        }

    def _replace_all_spec_symbols_in_parsed_data(self, field):
        replaced_field = field
        if isinstance(field, list):
            replaced_field = [
                self._replace_spec(f)
                for f in field
            ]
        if isinstance(field, dict):
            replaced_field = {
                self._replace_spec(key): self._replace_spec(value)
                for key, value in field.items()
            }
        return replaced_field

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
                .replace("(", "")
                .replace(")", "")
                .replace("/", " ")
                )