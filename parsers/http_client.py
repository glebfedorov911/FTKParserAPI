from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
import aiohttp
import os

from config.settings import config


class HTTPClient(ABC):


    @abstractmethod
    async def do_request(self, method: str, url: str, 
                         *, 
                         headers: dict = None, json: dict = None) -> str: ...

    @abstractmethod
    async def get_photo(self, ):
        ...

class Requestor:
    ...

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
    

    def __init__(self, html: str, base_url: str):
        self.soup = BeautifulSoup(html, "html.parser")
        self.base_url = base_url
        self.dir_with_image = config.ftk_parser_config.image_path

        if not os.path.exists(self.dir_with_image):
            os.mkdir(self.dir_with_image)

    def get_image_from_page(self, selector: str, index: int) -> str:
        image = self.soup.find_all(class_=selector)[index]

        src = image.get("src")
        if not src:
            raise ValueError("Incorrect selector, not found tag")
        image_name = src.split("/")[-1]
        self.image_path = f"{self.dir_with_image}/{image_name}"

        if not os.path.exists(self.image_path):
            with open(self.image_path, "wb") as file:
                file.write(...)

        return self.image_path


class HTTPClientAioHttp(HTTPClient):

    async def do_request(self, method: str, url: str, 
                         *, 
                         headers: dict = None, json: dict = None) -> str:
        """
        method = (POST, GET, PUT ...)
        url = address of page
        
        Method do request with aiohttp
        """
        return await self._make_request(method, url, 
                                        headers=headers, 
                                        json=json, 
                                        return_type="text")
    
    async def get_photo(self, url: str, *, headers: dict = None):
        """
        url = address of page
        
        Method get image content
        """
        return await self._make_request("GET", url, 
                                        headers=headers, 
                                        return_type="bytes")
            
    async def _make_request(self, method: str, url: str, *,
                            headers: dict = None,
                            json: dict = None,
                            return_type: str = "text"
                            ) -> str | bytes:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, headers=headers, json=json) as response:
                    response.raise_for_status()
                    if return_type == "text":
                        return await response.text()
                    elif return_type == "bytes":
                        return await response.read()
                    raise ValueError(f"Not found this return type {return_type}")
            except aiohttp.ClientError as e:
                print(f"Request failed: {e}")
                raise ValueError("Bad Request")
            
class GetRequestor(Requestor):
    

    def __init__(
            self,
            http_client: HTTPClient
    ) -> None:
        self.http_client = http_client

    async def get_html(self, url: str, *, json: dict = None, headers: dict = None) -> str:
        return await self.http_client.do_request("GET", url, headers=headers, json=json)
  
class RequestorFabric:

    def __init__(
            self,
            http_client: HTTPClient
    ) -> None:
        self.http_client = http_client


    def create_requestor(self, method: str) -> Requestor:
        if method.lower() == "get":
            return GetRequestor(self.http_client)
        if method.lower() == "post": ...
        if method.lower() == "put": ...
        if method.lower() == "patch": ...
        if method.lower() == "delete": ...
        raise ValueError(f"Not found requestor for method {method}")