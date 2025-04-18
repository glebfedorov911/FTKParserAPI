from abc import ABC, abstractmethod
import os

from bs4 import BeautifulSoup

from config.settings import config
from parsers.requestor import GetRequestor


class HTMLParser(ABC):
    

    @abstractmethod
    def get_image_from_page(self, selector: str, index: int) -> str:
        ...

    @abstractmethod
    def save_table_to_json(self, selector: str, index: int) -> str:
        ...
    
    @abstractmethod
    def get_tag_by_tag(self, selector: str, index: int) -> str:
        ...

class BeautifulSoupHTMLParser(HTMLParser):
    

    def __init__(self, html: str, base_url: str, requestor: GetRequestor):
        self.soup = BeautifulSoup(html, "html.parser")
        self.base_url = base_url
        self.requestor = requestor

        self.dir_with_image = config.ftk_parser_config.image_path
        if not os.path.exists(self.dir_with_image):
            os.mkdir(self.dir_with_image)

    def get_image_from_page(self, selector: str, index: int) -> str:
        image = self.soup.find_all(class_=selector)[index]

        src = image.get("src")
        if not src:
            raise ValueError("Incorrect selector, not found tag")
        photo_url = self.base_url + src
        image_name = src.split("/")[-1]
        self.image_path = f"{self.dir_with_image}/{image_name}"

        if not os.path.exists(self.image_path):
            photo = self.requestor.get_photo(photo_url)
            with open(self.image_path, "wb") as file:
                file.write(photo)

        return self.image_path