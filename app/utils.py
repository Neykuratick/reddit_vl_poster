from datetime import datetime, timezone, timedelta


def get_timestamp(hours_delta: int) -> float:
    post_time = datetime.now(tz=timezone.utc) + timedelta(hours=hours_delta, minutes=1)
    return post_time.timestamp()
