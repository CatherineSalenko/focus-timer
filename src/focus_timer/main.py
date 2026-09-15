from datetime import datetime, timezone

from fastapi import FastAPI

from focus_timer.pomodoro import Session, Settings, start_session

app = FastAPI()

current_session: Session | None = None


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/ping")
def ping():
    """Проверка, что сервер жив."""
    return {"pong": True}


@app.post("/api/session/start")
def start():
    """Начать новую сессию помодоро."""
    global current_session
    current_session = start_session(Settings(), datetime.now(timezone.utc))
    return current_session
