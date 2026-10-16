import pytest

from app.domain.money import MoneyFormatError, add_cents, format_money, parse_money, subtract_cents


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("0.00", 0), ("1.05", 105), ("30000.00", 3_000_000), ("0002.10", 210)],
)
def test_parse_canonical_money_to_integer_cents(raw, expected):
    assert parse_money(raw) == expected


@pytest.mark.parametrize("raw", [1.1, 1, None, "1", "1.0", "1.001", "-1.00", " 1.00", "1,00"])
def test_parse_money_rejects_noncanonical_or_non_string_values(raw):
    with pytest.raises(MoneyFormatError):
        parse_money(raw)


@pytest.mark.parametrize(
    ("cents", "expected"),
    [(0, "0.00"), (105, "1.05"), (3_000_000, "30000.00"), (-20_000, "-200.00")],
)
def test_format_money_is_exact(cents, expected):
    assert format_money(cents) == expected


def test_integer_cent_arithmetic_is_exact():
    assert add_cents(10, 20, 30) == 60
    assert subtract_cents(100, 120) == -20


@pytest.mark.parametrize("value", [1.5, "100", None])
def test_arithmetic_rejects_non_integer_cents(value):
    with pytest.raises(TypeError):
        add_cents(10, value)
