from abc import ABC, abstractmethod

import aiohttp


class HTTPClient(ABC):


    @abstractmethod
    async def do_request(self, method: str, url: str, 
                         *, 
                         headers: dict = None, json: dict = None) -> aiohttp.ClientResponse: ...


class HTTPClientAioHttp(HTTPClient):


    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def do_request(self, method: str, url: str, 
                         *, 
                         headers: dict = None, json: dict = None) -> aiohttp.ClientResponse:
        """
        method = (POST, GET, PUT ...)
        url = address of page
        
        Method do request with aiohttp
        """
        try:
            response = await self.session.request(method, url, headers=headers, json=json)
            response.raise_for_status()
            return response
        except aiohttp.ClientError as e:
            print(f"Request failed: {e}")
            raise ValueError("Bad Request")xz