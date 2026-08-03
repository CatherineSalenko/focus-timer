from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/ping")
def ping():
    """Проверка, что сервер жив."""
    return {"pong": True}
