from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException

from focus_timer.pomodoro import (
    Session,
    Settings,
    phase_end,
    progress,
    start_session,
    time_left,
)

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


@app.get("/api/session")
def get_session():
    """Текущее состояние таймера."""
    if current_session is None:
        raise HTTPException(status_code=404, detail="Сессия не запущена")

    now = datetime.now(timezone.utc)
    ends_at = phase_end(
        current_session.started_at, current_session.phase, current_session.settings
    )
    return {
        "phase": current_session.phase,
        "completed_pomodoros": current_session.completed_pomodoros,
        "started_at": current_session.started_at,
        "ends_at": ends_at,
        "seconds_left": time_left(ends_at, now).total_seconds(),
        "progress": progress(current_session.started_at, ends_at, now),
    }
