from parsers.requestor import GetRequestor
from parsers.parser import HTMLParser

from fake_useragent import UserAgent



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
    
    def __init__(self, requestor: GetRequestor, parser: HTMLParser):
        self.requestor = requestor
        self.parser = parser

    @property
    def headers(self):
        ua = UserAgent()
        return {
            "User-Agent": ua.random
        }

    async def parse_data(self):
        for url in self.URLS:
            current_pagination = 1
            url = url.format(num_page=current_pagination)

            html = await self.requestor.get_html(url, headers=self.headers)
            current_page = 0
            last_pagination = await self.parser.get_data_from_tag(html, "pagination__item", -2)
            while current_pagination != last_pagination:
                while True:
                    try:
                        url_page_product = await self.parser.get_url_from_tag(html, "product__image-wrapper", current_page)
                    except IndexError:
                        break
                    html_inner = await self.requestor.get_html(url_page_product, headers=self.headers)
                    title = await self.parser.get_data_from_tag(html_inner, "content__title wrapper", 0)
                    json = await self.parser.save_table_to_json(html_inner, "info__specs-table", 0)
                    signs = []
                    sign_num = 0
                    while True:
                        try:
                            sign = await self.parser.get_data_from_tag(html_inner, "item__feature-label", sign_num)
                        except IndexError:
                            break
                        signs.append(sign)
                        sign_num += 1

                    print(title, json, signs)
                    current_page += 1

                current_pagination += 1
            break