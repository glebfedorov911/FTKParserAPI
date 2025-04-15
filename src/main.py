from fastapi import FastAPI, status


app = FastAPI()

@app.get("/")
async def hello(name: str = "World"):
    return {
        "message": f"Hello, {name}!",
        "status": status.HTTP_200_OK
    }