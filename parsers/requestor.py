from parsers.http_client import HTTPClient

import aiohttp


class Requestor:

    def __init__(
            self,
            http_client: HTTPClient
    ) -> None:
        self.http_client = http_client

    async def _get_by_return_type(self, return_type: str, /, **kwargs) -> aiohttp.ClientResponse:
        response = await self.http_client.do_request(**kwargs)
        match return_type:
            case "text":
                return await response.text()
            case "bytes":
                return await response.read()
            case _:
                raise ValueError(f"Not found type {return_type}")

class GetRequestor(Requestor):


    def __init__(
            self,
            http_client: HTTPClient
    ) -> None:
        super().__init__(http_client=http_client)

    async def get_html(self, url: str, *, json: dict = None, headers: dict = None) -> str:
        return await self._get_by_return_type("text", method="GET", url=url, json=json, headers=headers)

    async def get_photo(self, url: str, *, json: dict = None, headers: dict = None) -> None:
        return await self._get_by_return_type("bytes", method="GET", url=url, json=json, headers=headers)