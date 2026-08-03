from focus_timer.pomodoro import Phase, Settings, next_phase, phase_duration_minutes


def test_after_pomodoro_short_break():
    assert next_phase(Phase.WORK, 1, Settings()) is Phase.SHORT_BREAK


def test_after_fourth_pomodoro_long_break():
    assert next_phase(Phase.WORK, 4, Settings()) is Phase.LONG_BREAK


def test_after_short_break_goes_to_work():
    assert next_phase(Phase.SHORT_BREAK, 1, Settings()) is Phase.WORK


def test_after_long_break_goes_to_work():
    assert phase_duration_minutes(Phase.WORK, Settings()) == 25


