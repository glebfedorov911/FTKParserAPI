from fastapi import FastAPI, status

from src.ftk.router import router as ftk_router


app = FastAPI()
app.include_router(ftk_router)

@app.get("/")
async def hello(name: str = "World"):
    return {
        "message": f"Hello, {name}!",
        "status": status.HTTP_200_OK
    }