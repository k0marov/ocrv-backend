def format_duration(duration_sec: int) -> str:
    min = str(duration_sec//60).zfill(2)
    sec = str(duration_sec%60).zfill(2)
    return f'{min}:{sec}'