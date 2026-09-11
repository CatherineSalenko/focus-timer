from datetime import datetime, timedelta

from focus_timer.pomodoro import (
    Phase,
    Settings,
    next_phase,
    phase_duration_minutes,
    phase_end,
    progress,
    time_left,
)


def test_after_pomodoro_short_break():
    assert next_phase(Phase.WORK, 1, Settings()) is Phase.SHORT_BREAK


def test_after_fourth_pomodoro_long_break():
    assert next_phase(Phase.WORK, 4, Settings()) is Phase.LONG_BREAK


def test_after_short_break_goes_to_work():
    assert next_phase(Phase.SHORT_BREAK, 1, Settings()) is Phase.WORK


def test_work_phase_lasts_25_minutes():
    assert phase_duration_minutes(Phase.WORK, Settings()) == 25


def test_work_phase_ends_after_25_minutes():
    assert phase_end(datetime(2026, 9, 11, 12, 0),
                     Phase.WORK, Settings()) == datetime(2026, 9, 11, 12, 25)


def test_time_left():
    ends_at = datetime(2026, 9, 11, 12, 25)
    now = datetime(2026, 9, 11, 12, 10)
    assert time_left(ends_at, now) == timedelta(minutes=15)


def test_progress():
    started_at = datetime(2026, 9, 11, 12, 0)
    ends_at = datetime(2026, 9, 11, 12, 25)
    now = datetime(2026, 9, 11, 12, 10)
    assert progress(started_at, ends_at, now) == 10 / 25


def test_time_left_never_negative():
    ends_at = datetime(2026, 9, 11, 12, 25)
    now = datetime(2026, 9, 11, 12, 30)
    assert time_left(ends_at, now) == timedelta(0)


def test_progress_never_above_one():
    started_at = datetime(2026, 9, 11, 12, 0)
    ends_at = datetime(2026, 9, 11, 12, 25)
    now = datetime(2026, 9, 11, 12, 30)
    assert progress(started_at, ends_at, now) == 1.0
