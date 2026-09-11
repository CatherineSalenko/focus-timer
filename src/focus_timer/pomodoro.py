from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class Phase(Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


@dataclass(frozen=True)
class Settings:
    work_minutes: int = 25
    short_break_minutes: int = 5
    long_break_minutes: int = 15
    pomodoros_until_long_break: int = 4


def phase_duration_minutes(phase: Phase, settings: Settings) -> int:
    if phase is Phase.WORK:
        return settings.work_minutes
    if phase is Phase.SHORT_BREAK:
        return settings.short_break_minutes
    return settings.long_break_minutes


def next_phase(current: Phase, completed_pomodoros: int, settings: Settings) -> Phase:
    if current is not Phase.WORK:
        return Phase.WORK
    if completed_pomodoros % settings.pomodoros_until_long_break == 0:
        return Phase.LONG_BREAK
    return Phase.SHORT_BREAK


def phase_end(started_at: datetime, phase: Phase, settings: Settings) -> datetime:
    minutes = phase_duration_minutes(phase, settings)
    return started_at + timedelta(minutes=minutes)


def time_left(ends_at: datetime, now: datetime) -> timedelta:
    return max(ends_at - now, timedelta(0))


def progress(started_at: datetime, ends_at: datetime, now: datetime) -> float:
    total = ends_at - started_at
    passed = now - started_at
    return min(max(passed / total, 0.0), 1.0)
