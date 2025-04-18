from parsers.requestor import GetRequestor
from parsers.http_client import HTTPClientAioHttp
from parsers.parser import BeautifulSoupHTMLParser



async def amain():
    async with HTTPClientAioHttp() as client:
        get_requestor = GetRequestor(client)
        parser = BeautifulSoupHTMLParser()
        photo = await get_requestor.get_photo("https://www.f-tk.ru/upload/uf/c0e/lider-prodazh-_2_.svg")
        return photo

def main():
    import asyncio
    return asyncio.run(amain())

if __name__ == "__main__":
    with open("test.svg", 'wb') as f:
        f.write(main())