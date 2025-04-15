from abc import ABC, abstractmethod

import aiohttp

from bs4 import BeautifulSoup


class HTTPClient(ABC):


    @abstractmethod
    async def do_request(self, method: str, url: str, 
                         *, 
                         headers: dict = None, json: dict = None) -> str: ...

class Requestor(ABC):


    @abstractmethod
    async def get_html(self, url: str, *, json: dict = None, headers: dict = None) -> str:
        ...

class HTMLParser(ABC):
    

    @abstractmethod
    def get_image_from_page(self, html: str, selector: str) -> str:
        ...

    @abstractmethod
    def save_table_to_json(self, html: str, selector: str) -> str:
        ...
    
    @abstractmethod
    def get_tag_by_tag(self, html: str, selector: str) -> str:
        ...

class BeautifulSoupHTMLParser(HTMLParser):
    
    ...            

class HTTPClientAioHttp(HTTPClient):


    async def do_request(self, method: str, url: str, 
                         *, 
                         headers: dict = None, json: dict = None) -> str:
        """
        method = (POST, GET, PUT ...)
        url = address of page
        
        Method do request with aiohttp
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, headers=headers, json=json) as response:
                    response.raise_for_status()
                    return await response.text()
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
    
class PostRequestor(Requestor):
    

    def __init__(
            self,
            http_client: HTTPClient
    ) -> None:
        self.http_client = http_client

    async def get_html(self, url: str, *, json: dict = None, headers: dict = None) -> str:
        return await self.http_client.do_request("POST", url, headers=headers, json=json)
    
class PutRequestor(Requestor):
    

    def __init__(
            self,
            http_client: HTTPClient
    ) -> None:
        self.http_client = http_client

    async def get_html(self, url: str, *, json: dict = None, headers: dict = None) -> str:
        return await self.http_client.do_request("PUT", url, headers=headers, json=json)

class PatchRequestor(Requestor):
    

    def __init__(
            self,
            http_client: HTTPClient
    ) -> None:
        self.http_client = http_client

    async def get_html(self, url: str, *, json: dict = None, headers: dict = None) -> str:
        return await self.http_client.do_request("PATCH", url, headers=headers, json=json)
    
class DeleteRequestor(Requestor):
    

    def __init__(
            self,
            http_client: HTTPClient
    ) -> None:
        self.http_client = http_client

    async def get_html(self, url: str, *, json: dict = None, headers: dict = None) -> str:
        return await self.http_client.do_request("DELETE", url, headers=headers, json=json)

class RequestorFabric:

    def __init__(
            self,
            http_client: HTTPClient
    ) -> None:
        self.http_client = http_client


    def create_requestor(self, method: str) -> Requestor:
        if method.lower() == "get":
            return GetRequestor(self.http_client)
        if method.lower() == "post":
            return PostRequestor(self.http_client)
        if method.lower() == "put":
            return PutRequestor(self.http_client)
        if method.lower() == "patch":
            return PatchRequestor(self.http_client)
        if method.lower() == "delete":
            return DeleteRequestor(self.http_client)
        raise ValueError(f"Not found requestor for method {method}")