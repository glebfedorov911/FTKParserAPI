from parsers.requestor import GetRequestor
from parsers.parser import HTMLParser

from fake_useragent import UserAgent

import asyncio



class FTKParser:
    URLS = [
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

        for url in self.URLS:
            self.current_pagination = 1
            self.current_page = 0

            url = url.format(num_page=self.current_pagination)
            html_with_products = await self.requestor.get_html(url, headers=self.headers)
            last_pagination = await self._get_last_pagination_num(html_with_products)
            key_parsed_data = url.split("/")[-2]

            while self.current_pagination <= last_pagination:
                results = await self._get_result_from_products(html_with_products)
                self._set_result(key_parsed_data, results)
                self.current_pagination += 1

        return self.parsed_data

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
                url_page_product = await self.parser.get_url_from_tag(html, "product__image-wrapper", self.current_page)
            except IndexError:
                break

            html_with_one_product = await self.requestor.get_html(url_page_product, headers=self.headers)
            result = await self._get_data_from_page(html_with_one_product)
            results.append(result)
            await asyncio.sleep(1)

            self.current_page += 1
        return results
    
    async def _get_data_from_page(self, html: str) -> tuple:
        title = await self.parser.get_data_from_tag(html, "content__title wrapper", 0)
        characteristics = await self.parser.save_table_to_json(html, "info__specs-table", 0)
        signs = await self._get_sings_from_page(html)
        return {
            "title": title,
            "characteristics": characteristics,
            "signs": signs
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