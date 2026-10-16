from __future__ import annotations

import re


class MoneyFormatError(ValueError):
    pass


_MONEY_PATTERN = re.compile(r"^[0-9]+\.[0-9]{2}$")


def parse_money(value: str) -> int:
    if not isinstance(value, str) or not _MONEY_PATTERN.fullmatch(value):
        raise MoneyFormatError("Money must be a canonical non-negative string with two decimals")
    units, cents = value.split(".")
    return int(units) * 100 + int(cents)


def format_money(cents: int) -> str:
    _require_integer(cents)
    sign = "-" if cents < 0 else ""
    absolute = abs(cents)
    return f"{sign}{absolute // 100}.{absolute % 100:02d}"


def add_cents(*values: int) -> int:
    for value in values:
        _require_integer(value)
    return sum(values)


def subtract_cents(left: int, right: int) -> int:
    _require_integer(left)
    _require_integer(right)
    return left - right


def _require_integer(value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("Money calculations require integer cents")
