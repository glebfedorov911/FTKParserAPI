from parsers.requestor import GetRequestor
from parsers.http_client import HTTPClientAioHttp
from parsers.parser import BeautifulSoupHTMLParser



async def amain():
    async with HTTPClientAioHttp() as client:
        get_requestor = GetRequestor(client)
        html = await get_requestor.get_html("https://www.f-tk.ru/catalog/spetsodezhda/")
        parser = BeautifulSoupHTMLParser(html, "https://www.f-tk.ru", get_requestor)
        await parser.get_image_from_page("product__feature-icon", 0)

def main():
    import asyncio
    return asyncio.run(amain())

if __name__ == "__main__":
    main()