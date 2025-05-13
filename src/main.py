from fastapi import FastAPI, status

from src.ftk.router import router as ftk_router
from src.ftk.tasks import call_ftk_parser_endpoint


app = FastAPI()
app.include_router(ftk_router)

@app.get("/")
async def hello(name: str = "World"):
    return {
        "message": f"Hello, {name}!",
        "status": status.HTTP_200_OK
    }

call_ftk_parser_endpoint.apply_async(countdown=60)