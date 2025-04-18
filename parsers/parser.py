from abc import ABC, abstractmethod
import os

from bs4 import BeautifulSoup

from config.settings import config
from parsers.requestor import GetRequestor


class HTMLParser(ABC):
    

    @abstractmethod
    async def get_image_from_page(self, html: str, selector: str, index: int) -> str:
        ...

    @abstractmethod
    async def get_data_from_tag(self, html: str, selector: str, index: int) -> str:
        ...

    @abstractmethod
    async def save_table_to_json(self, html: str, selector: str, index: int) -> str:
        ...

    @abstractmethod
    async def get_url_from_tag(self, html: str, selector: str, index: int) -> str:
        ...

class BeautifulSoupMixin:
    
    
    def __init__(self, html: str, base_url: str, requestor: GetRequestor) -> None:
        self.soup = BeautifulSoup(html, "html.parser")
        self.base_url = base_url
        self.requestor = requestor

    def _find_data_with_soup(self, selector: str, index: int):
        return self.soup.find_all(class_=selector)[index]
    
    def _double_slash_to_one(self, string: str) -> str:
        if "https://" not in string:
            return string
        string = string.replace("https://", "*").replace("//", "/").replace("*", "https://")
        return string

    @staticmethod
    def _clear_text_from_tag(tag) -> str:
        return tag.text.strip().replace("\n", "").replace("\t", "")

class BeautifulSoupGetPhoto(BeautifulSoupMixin):

    
    def __init__(self, html: str, base_url: str, requestor: GetRequestor) -> None:
        super().__init__(html, base_url, requestor)

    @property
    def dir_with_image(self):
        dir_with_image = config.ftk_parser_config.image_path
        if not os.path.exists(dir_with_image):
            os.makedirs(dir_with_image, exist_ok=True)
        return dir_with_image

    async def get_image_from_page(self, selector: str, index: int) -> str:
        image = self._find_data_with_soup(selector, index)

        src = self._get_src_from_tag(image)
        
        photo_url = self._create_photo_url(src)

        image_path = self._create_image_path_for_save_in_dir(src)

        return await self._save_image_if_not_exists_already(image_path, photo_url)
    
    def _get_src_from_tag(self, tag):
        src = tag.get("src") or tag.get("data-src")
        if not src:
            raise ValueError("Incorrect selector, not found tag")
        return src

    def _create_photo_url(self, src: str) -> str:
        return self.base_url + src 
    
    def _create_image_path_for_save_in_dir(self, src: str) -> str:
        image_name = src.split("/")[-1]
        return f"{self.dir_with_image}/{image_name}"

    async def _save_image_if_not_exists_already(self, image_path: str, photo_url: str) -> str:
        photo = await self.requestor.get_photo(photo_url)
        with open(image_path, 'wb') as file:
            file.write(photo)
        return image_path

class BeautifulSoupTableToJson(BeautifulSoupMixin):


    def __init__(self, html: str, base_url: str, requestor: GetRequestor) -> None:
        super().__init__(html, base_url, requestor)
        self.html = html

    async def save_table_to_json(self, other: "BeautifulSoupHTMLParser", selector: str, index: int) -> str:
        table = self._find_data_with_soup(selector, index)
        table_to_dict = {}

        ths = table.find_all("th")
        tds = table.find_all("td")
        for th, td in zip(ths, tds):
            data_from_td = ''
            if imgs := td.find_all("img"):
                data_from_td = await self._save_data_from_imgs(other, imgs)
            else:
                data_from_td = self._clear_text_from_tag(td)
            data_from_th = self._clear_text_from_tag(th)
            
            table_to_dict[data_from_th] = data_from_td

        return table_to_dict
    
    async def _save_data_from_imgs(self, other: "BeautifulSoupHTMLParser", imgs):
        img_urls = [img.get("data-tooltip") for img in imgs]
        if img_urls[0]:
            data_from_td = img_urls
        else:
            attr_class = imgs.pop(0).get("class")[0] #because only one maker product
            data_from_td = await other.get_image_from_page(self.html, attr_class, 0)
        return self._double_slash_to_one(data_from_td)

class BeautifulSoupGetUrl(BeautifulSoupMixin):


    def __init__(self, html: str, base_url: str, requestor: GetRequestor) -> None:
        super().__init__(html, base_url, requestor)

    def get_url_from_tag(self, selector: str, index: int) -> str:
        card = self.soup.find_all(class_=selector)[index]
        url = f"{self.base_url}/{card.get("href")}"
        return self._double_slash_to_one(url)

class BeautifulSoupGetText(BeautifulSoupMixin):


    def __init__(self, html: str, base_url: str, requestor: GetRequestor) -> None:
        super().__init__(html, base_url, requestor)

    def get_data_from_tag(self, selector: str, index: int) -> str:
        tag = self.soup.find_all(class_=selector)[index]
        return self._clear_text_from_tag(tag)

class BeautifulSoupHTMLParser(HTMLParser):
    

    def __init__(self, base_url: str, requestor: GetRequestor):
        self.base_url = base_url
        self.requestor = requestor

    async def get_image_from_page(self, html: str, selector: str, index: int) -> str:
        photo_parser = BeautifulSoupGetPhoto(html, self.base_url, self.requestor)
        return await photo_parser.get_image_from_page(selector, index) 
    
    async def get_data_from_tag(self, html: str, selector: str, index: int) -> str:
        tag_parser = BeautifulSoupGetText(html, self.base_url, self.requestor)
        return tag_parser.get_data_from_tag(selector, index)

    async def save_table_to_json(self, html: str, selector: str, index: int) -> str:
        table_parser = BeautifulSoupTableToJson(html, self.base_url, self.requestor)
        return await table_parser.save_table_to_json(self, selector, index)

    async def get_url_from_tag(self, html: str, selector: str, index: int) -> str:
        url_parser = BeautifulSoupGetUrl(html, self.base_url, self.requestor)
        return url_parser.get_url_from_tag(selector, index)