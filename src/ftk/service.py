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
                        icons=self._edit_icons(self._replace_all_spec_symbols_in_parsed_data(product["signs"])),
                        characteristics=self._replace_all_spec_symbols_in_parsed_data(product["characteristics"])
                    )
                except Exception as e:
                    print(e)
        actually_show_data = await self.repo.get_all(actually=True)       
        return {
            "data": actually_show_data,
            "count": len(actually_show_data)
        }

    @staticmethod
    def _edit_icons(icons: list):
        icons_collection = {}
        for icon in icons:
            icon = icon.split(" ")
            if len(icon) > 1:
                key, value = icon[0], " ".join(icon[1:])
            else:
                key, value = "Остальное", icon[0]
            if key not in icons_collection:
                icons_collection[key] = []
            icons_collection[key].append(value)
        return icons_collection

    def _replace_all_spec_symbols_in_parsed_data(self, field):
        replaced_field = field
        if isinstance(field, list):
            replaced_field = [
                self._replace_spec(f)
                for f in field
            ]
        if isinstance(field, dict):
            replaced_field = {
                self._replace_spec_key(key): self._replace_all_spec_symbols_in_parsed_data(value)
                for key, value in field.items()
            }
        return replaced_field

    @staticmethod
    def _replace_spec(field):
        return (field.strip()
                .replace("\t", "")
                .replace("\n", "")
                .replace(":", "")
                .replace("\\", "")
                .replace(",", "")
                .replace(";", "")
                .replace(".", "")
                .replace("-", " ")
                .replace("_", " ")
                .replace("(", "")
                .replace(")", "")
                .replace("/", "")
                )

    @staticmethod
    def _replace_spec_key(field):
        translit_dict = {
            'А': 'A', 'а': 'a',
            'Б': 'B', 'б': 'b',
            'В': 'V', 'в': 'v',
            'Г': 'G', 'г': 'g',
            'Д': 'D', 'д': 'd',
            'Е': 'E', 'е': 'e',
            'Ё': 'E', 'ё': 'e',
            'Ж': 'Zh', 'ж': 'zh',
            'З': 'Z', 'з': 'z',
            'И': 'I', 'и': 'i',
            'Й': 'Y', 'й': 'y',
            'К': 'K', 'к': 'k',
            'Л': 'L', 'л': 'l',
            'М': 'M', 'м': 'm',
            'Н': 'N', 'н': 'n',
            'О': 'O', 'о': 'o',
            'П': 'P', 'п': 'p',
            'Р': 'R', 'р': 'r',
            'С': 'S', 'с': 's',
            'Т': 'T', 'т': 't',
            'У': 'U', 'у': 'u',
            'Ф': 'F', 'ф': 'f',
            'Х': 'Kh', 'х': 'kh',
            'Ц': 'Ts', 'ц': 'ts',
            'Ч': 'Ch', 'ч': 'ch',
            'Ш': 'Sh', 'ш': 'sh',
            'Щ': 'Shch', 'щ': 'shch',
            'Ъ': '', 'ъ': '',
            'Ы': 'Y', 'ы': 'y',
            'Ь': '', 'ь': '',
            'Э': 'E', 'э': 'e',
            'Ю': 'Yu', 'ю': 'yu',
            'Я': 'Ya', 'я': 'ya',
        }
        field = ''.join([translit_dict.get(c, c) for c in field])
        return (field.strip()
                .replace("\t", "")
                .replace("\n", "")
                .replace(":", "")
                .replace("\\", "")
                .replace(",", "")
                .replace(";", "")
                .replace(".", "")
                .replace("-", "")
                .replace("_", "")
                .replace("(", "")
                .replace(")", "")
                .replace("/", "")
                .replace(" ", "")
                )