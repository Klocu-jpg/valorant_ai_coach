def get_round_phase(time_seconds: int | None) -> str:
    if time_seconds is None:
        return "unknown"
    if time_seconds > 90:
        return "early"  # Buy/early round
    elif 30 < time_seconds <= 90:
        return "mid"
    else:
        return "late"