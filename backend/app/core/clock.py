from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Protocol
from zoneinfo import ZoneInfo


class Clock(Protocol):
    def now_utc(self) -> datetime: ...

    def today_argentina(self) -> date: ...


class SystemClock:
    def now_utc(self) -> datetime:
        return datetime.now(timezone.utc)

    def today_argentina(self) -> date:
        return self.now_utc().astimezone(ZoneInfo("America/Argentina/Buenos_Aires")).date()


class MutableClock:
    def __init__(self, current: datetime):
        if current.tzinfo is None:
            raise ValueError("MutableClock requires a timezone-aware instant")
        self._current = current.astimezone(timezone.utc)

    def now_utc(self) -> datetime:
        return self._current

    def today_argentina(self) -> date:
        return self._current.astimezone(ZoneInfo("America/Argentina/Buenos_Aires")).date()

    def advance(self, **kwargs: float) -> None:
        self._current += timedelta(**kwargs)
