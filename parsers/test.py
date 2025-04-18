from parsers.requestor import GetRequestor
from parsers.http_client import HTTPClientAioHttp
from parsers.parser import BeautifulSoupHTMLParser
from parsers.ftk import FTKParser



async def amain():
    async with HTTPClientAioHttp() as client:
        get_requestor = GetRequestor(client)
        parser = BeautifulSoupHTMLParser("https://www.f-tk.ru", get_requestor)
        ftk = FTKParser(get_requestor, parser)
        a = await ftk.parse_data()
        print(a)

def main():
    import asyncio
    return asyncio.run(amain())

if __name__ == "__main__":
    main()