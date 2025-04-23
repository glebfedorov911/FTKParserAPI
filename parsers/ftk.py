import aiohttp.client_exceptions
from parsers.requestor import GetRequestor
from parsers.parser import HTMLParser

from fake_useragent import UserAgent
import aiohttp

import asyncio



class FTKParser:
    urls = [
        "https://www.f-tk.ru/catalog/spetsodezhda/?PAGEN_1={num_page}",
        "https://www.f-tk.ru/catalog/spetsobuv/?PAGEN_1={num_page}",
        "https://www.f-tk.ru/catalog/siz/?PAGEN_1={num_page}",
        "https://www.f-tk.ru/catalog/zashchita_ruk/?PAGEN_1={num_page}",
        "https://www.f-tk.ru/catalog/tekstil_myagkiy_inventar/?PAGEN_1={num_page}",
        "https://www.f-tk.ru/catalog/khoztovary_inventar_mebel/?PAGEN_1={num_page}",
        "https://www.f-tk.ru/catalog/logotipy_/?PAGEN_1={num_page}",
        "https://www.f-tk.ru/catalog/po_otraslyam_/?PAGEN_1={num_page}",
        "https://www.f-tk.ru/catalog/poligrafiya/?PAGEN_1={num_page}",
    ]
    
    def __init__(
            self, 
            requestor: GetRequestor, 
            parser: HTMLParser
        ):
        self.requestor = requestor
        self.parser = parser
        self.current_pagination = 1
        self.current_page = 0
        self.parsed_data = {}

    @property
    def headers(self):
        ua = UserAgent()
        return {
            "User-Agent": ua.random
        }

    async def parse_data(self) -> dict:

        for idx, url in enumerate(self.urls):
            self.current_pagination = 1

            try:
                url_formatted, html_with_products = await self._get_html_from_formatted_page(idx, url)
                last_pagination = await self._get_last_pagination_num(html_with_products)
                key_parsed_data = url_formatted.split("/")[-2]
            except (ValueError, aiohttp.ClientError) as e:
                print(f"do again because {e}")
                self.urls.append(url)


            while self.current_pagination <= last_pagination:
                self.current_page = 0
                try: 
                    url_formatted, html_with_products = await self._get_html_from_formatted_page(idx, url)
                    print(f"current: {self.current_pagination} | url: {url_formatted} | Получаем данные со страницы с продуктами")
                    results = await self._get_result_from_products(html_with_products)
                    print("Получаем данные со страниц с продуктами")
                    self._set_result(key_parsed_data, results)
                    print("Сохраняем данные")
                except aiohttp.ClientError as e:
                    print(f"do again because {e}")
                    self.current_pagination -= 1
                finally:
                    self.current_pagination += 1
                    
        return self.parsed_data

    async def _get_html_from_formatted_page(self, idx: int, url: str) -> tuple[str, str]:
        print(f"Парсим страницу {idx+1}/{len(self.urls)}")
        url_formatted = url.format(num_page=self.current_pagination)
        html_with_products = await self.requestor.get_html(url_formatted, headers=self.headers)
        print("Получили код страницы")
        return url_formatted, html_with_products

    async def _get_last_pagination_num(self, html: str):
        LAST_PAGINATION_INDEX = -2
        try:
            last_num = await self.parser.get_data_from_tag(html, "pagination__item", LAST_PAGINATION_INDEX)
            return int(last_num)
        except:
            return 1

    async def _get_result_from_products(self, html):
        results = []
        while True:
            try:
                try:
                    print("Получаем данные с продукта")
                    url_page_product = await self.parser.get_url_from_tag(html, "product__image-wrapper", self.current_page)
                    print(f"Получили данные: {url_page_product}")
                except IndexError as e:
                    print(f"ошибка {e}")
                    break
                except aiohttp.ClientError as e:
                    print(f"ошибка {e}")
                    continue

                html_with_one_product = await self.requestor.get_html(url_page_product, headers=self.headers)
                result = await self._get_data_from_page(url_page_product, html_with_one_product)
                print(f"result: {len(result)}")
                results.append(result)
                print("Сохраняем данные с продуктом в массив")
                await asyncio.sleep(1)
            except aiohttp.ClientError as e:
                print(f"do again because {e}")
                self.current_page -= 1
            finally:
                self.current_page += 1
        return results
    
    async def _get_data_from_page(self, url: str, html: str) -> tuple:
        title = await self.parser.get_data_from_tag(html, "content__title wrapper", 0)
        characteristics = await self.parser.save_table_to_json(html, "info__specs-table", 0)
        signs = await self._get_sings_from_page(html)
        return {
            "url": url,
            "title": title,
            "characteristics": characteristics,
            "signs": signs,
        }

    async def _get_sings_from_page(self, html: str) -> list:
        signs = []
        current_sign_num = 0
        while True:
            try:
                sign = await self.parser.get_data_from_tag(html, "item__feature-label", current_sign_num)
            except IndexError:
                break
            signs.append(sign)
            current_sign_num += 1
        return signs
    
    def _set_result(self, key: str, results: list):
        if key not in self.parsed_data:
            self.parsed_data[key] = []

        for result in results:
            self.parsed_data[key].append(result)